import math

import cv2
import pymunk

from .sim import AirHockeyTable
from .interface import PuckPredictor

class TableSimPredictor(PuckPredictor):

    def __init__(self, threshold, width, height, max_pos=10):
        self.table = AirHockeyTable(width, height)
        self._threshold = threshold
        self.max_pos = max_pos

        # Prime with values
        self.positions = [(0,0)]
        self.times = [0]

    def threshold(self):
        return self._threshold

    def add_puck_event(self, tick, coords, radius):
        if len(self.positions) == self.max_pos:
            self.positions.pop(0)
            self.times.pop(0)

        self.positions.append(coords)
        self.times.append(tick)

    def predicted_path(self):

        # Create an average speed and angle from last N positions and times
        angle = 0
        speed = 0
        for pos_idx in range(1, len(self.positions)):
            del_y = self.positions[pos_idx][1] - self.positions[pos_idx-1][1]
            del_x = self.positions[pos_idx][0] - self.positions[pos_idx-1][0]
            del_time = (self.times[pos_idx] - self.times[pos_idx-1]) / cv2.getTickFrequency()

            angle += math.atan2(del_y, del_x)
            speed += math.sqrt(del_x * del_x + del_y * del_y) / del_time 

        angle /= len(self.positions)
        speed /= len(self.times)

        # Add a puck to the space and apply a speed at the determined
        # angle
        puck = self.table.add_puck(position=self.positions[-1])

        impulse = speed * pymunk.Vec2d(1, 0).rotated(angle)
        puck.body.apply_impulse(impulse)

        # Simulate several steps into the future
        future_pos = []
        dt = 1.0/10.0
        for t in range(15):
            self.table.space.step(dt)
            future_pos.append(tuple(puck.body.position))
        
        # Remove the puck once the simulation is over
        self.table.remove_puck(puck)

        return future_pos
