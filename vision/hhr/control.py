from .interface import RobotController
from pymunk import Vec2d

class SimGameController(RobotController):

    def __init__(self, game, x_pos):
        self.game = game
        self.x_pos = x_pos
        self.control_player = self.game.add_player()

    def use_prediction(self, pred_path, pred_vel):
        paddle = self.control_player.body

        for point in pred_path:
            if point[0] > self.x_pos:
                paddle.position = self.game.to_pygame(Vec2d(self.x_pos+10, point[1]))
                break
