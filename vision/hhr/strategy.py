import math

import cv2
import pymunk

from .sim import AirHockeyTable
from .interface import PuckPredictor

class TableSimPredictor(PuckPredictor):

    def __init__(self, threshold, width, height):
        self.table = AirHockeyTable(width, height)
        self._threshold = threshold

        self.last_pos = (0,0)
        self.curr_pos = (0,0)
        self.last_time = 0
        self.curr_time = 0

    def threshold(self):
        return self._threshold

    def add_puck_event(self, tick, coords, radius):
        self.last_pos = self.curr_pos
        self.curr_pos = coords

        self.last_time = self.curr_time
        self.curr_time = tick

    def predicted_path(self):
        del_y = self.curr_pos[1] - self.last_pos[1]
        del_x = self.curr_pos[0] - self.last_pos[0]
        del_time = (self.curr_time - self.last_time) / cv2.getTickFrequency()

        if del_time <= 0:
            return None

        angle = math.atan2(del_y, del_x)
        speed = math.sqrt(del_x * del_x + del_y * del_y) / del_time 

        puck = self.table.add_puck(position=self.curr_pos)

        impulse = speed * pymunk.Vec2d(1, 0).rotated(angle)
        puck.body.apply_impulse(impulse)

        future_pos = []
        dt = 1.0/10.0
        for t in range(15):
            self.table.space.step(dt)
            future_pos.append(tuple(puck.body.position))
        
        self.table.remove_puck(puck)

        return future_pos
