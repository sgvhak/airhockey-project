from .sim import AirHockeyTable
from .interface import PuckPredictor

class TableSimPredictor(PuckPredictor):

    def __init__(self, threshold, width, height):
        self.table = AirHockeyTable(width, height)
        self._threshold = threshold

    def threshold(self):
        return self._threshold

    def add_puck_event(self, tick, coords, radius):
        pass

    def predicted_path(self):
        pass
