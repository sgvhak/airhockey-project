import math

import cv2
import pymunk

from .sim import AirHockeyTable
from .interface import PuckPredictor
from .calc import MovingAverage

def calculate_speed_angle(pos1, pos2, time1, time2):
    """
    :param pos1: x,y tuple position from time1
    :param pos2: x,y tuple position from time2
    :param time1: time stamp of pos1, units seconds
    :param time2: time stamp of pos2, units seconds
    """
    dy = pos2[1] - pos1[1]
    dx = pos2[0] - pos1[0]
    dt = (time2 - time1)# / cv2.getTickFrequency()

    angle = math.atan2(dy, dx)
    speed = math.sqrt(dx * dx + dy * dy) / dt if dt != 0 else 0

    return speed, angle

class Circle(object):

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def intersect(self, p1, p2):
        # Source: Watt, 3D Computer Graphics, Third Edition, p18-19
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        a = dx*dx + dy*dy
        b = 2*dx*(p1[0] - self.x) + 2*dy*(p1[1] - self.y)
        c = self.x*self.x + self.y*self.y + p1[0]*p1[0] + p1[1]*p1[1] + 2*(-self.x*p1[0] - self.y*p1[1]) - self.radius*self.radius

        disc = b*b - 4*a*c  # discriminant

        if disc > 0:
            disc_sqrt = math.sqrt(disc)  # fixme: better varname?
            t1 = (-b + disc_sqrt) / (2*a)
            t2 = (-b - disc_sqrt) / (2*a)

            # Minimum value is the closes, 
            # only values of t between 0 and 1 lie
            # on the circle
            t = min(t1, t2)
            if t >= 0 and t <= 1:
                x = p1[0] + t*dx
                y = p1[1] + t*dy

                return x,y

        return None

    def draw(self, frame, color=(255, 0, 0)):
        pos = (int(self.x), int(self.y))
        cv2.circle(frame, pos, int(self.radius), color, 2)

class TableSimPredictor(PuckPredictor):

    def __init__(self, width, height, num_steps=10, avg_size=10, defense_radius=40):
        """
        :param width: table width in (units?)
        :param height: table width in (units?)
        :param num_steps: frames per second in simulation
        :param avg_size: number of elements in moving average
        :param defense_radius: constraint circle for paddle movements in (units?) 
        """
        self.table = AirHockeyTable(width, height)
        self.num_steps = num_steps

        # Store current posistion and time 
        self.curr_pos = (0, 0)
        self.curr_time = 0

        # Cache predicted path for draw
        self.pred_path = []

        # Calculate angles and speeds as we get them so we
        # can keep a rolling sum 
        self.angles = MovingAverage(avg_size)
        self.speeds = MovingAverage(avg_size) 

        # Create defense circle located at center of right most goal
        self.defense_circle = Circle(self.table.width, self.table.height / 2, defense_radius)

    def add_puck_event(self, tick, coords, radius):

        last_pos = self.curr_pos
        last_time = self.curr_time

        self.curr_pos = coords
        self.curr_time = tick

        if tick == 0:
            speed, angle = (0, 0)
        else:
            speed, angle = calculate_speed_angle(last_pos, self.curr_pos, last_time, self.curr_time)

        self.speeds.add_value(speed)
        self.angles.add_value(angle)

    def predicted_path(self):

        # Add a puck to the space and apply a speed at the determined
        # angle
        puck = self.table.add_puck(position=self.curr_pos)

        # Convert angle, speed averages tor regular floats, pymunk
        # doesn't seem to like numpy floats
        angle = float(self.angles.average)
        speed = float(self.speeds.average)

        impulse = speed * pymunk.Vec2d(1, 0).rotated(angle)
        puck.body.apply_impulse(impulse)

        # Simulate several steps into the future
        future_pos = []
        future_vel = []
        dt = 1.0/self.num_steps
        for t in range(self.num_steps):
            self.table.space.step(dt)
            future_pos.append(tuple(puck.body.position))
            future_vel.append(tuple(puck.body.velocity)) 

        # Remove the puck once the simulation is over
        self.table.remove_puck(puck)

        self.pred_path = future_pos
        self.pred_vel = future_vel

        return future_pos, future_vel

    def intercept_point(self):
        future_pos, future_vel = self.predicted_path()

        i_point = None
        for path in zip(future_pos[:-1], future_pos[1:]):
            i_point = self.defense_circle.intersect(path[0], path[1])
            if i_point:
                break

        return i_point

    def draw(self, frame):
        'Draws table and puck future positions using last predicted paths'

        # Draw predicted path
        for path in zip(self.pred_path[:-1], self.pred_path[1:]):
            p1 = tuple([int(p) for p in path[0]])
            p2 = tuple([int(p) for p in path[1]])
            cv2.line(frame,p1,p2,(255,0,0),5)

        # Draw simulated universe walls
        for line in self.table.walls:
            linea = tuple([int(a) for a in line.a])
            lineb = tuple([int(b) for b in line.b])
            cv2.rectangle(frame, linea, lineb, (255,0,0))

        # Draw defense circle
        self.defense_circle.draw(frame, (255, 0, 0))
