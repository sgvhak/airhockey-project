from .interface import RobotController
from pymunk import Vec2d

class SimGameController(RobotController):

    def __init__(self, game):
        self.game = game
        self.control_player = self.game.add_player()

    def move_to(self, intercept_point):
        paddle = self.control_player.body

        if intercept_point:
            paddle.position = self.game.to_pygame(Vec2d(intercept_point))
