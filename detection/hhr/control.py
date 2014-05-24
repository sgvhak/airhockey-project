from .interface import RobotController
from pymunk import Vec2d
from Box2D import b2Vec2

class PyMunkGameController(RobotController):

    def __init__(self, game):
        self.game = game
        self.control_player = self.game.add_player(mass=1e10)

    def move_to(self, intercept_point):
        paddle = self.control_player.body

        if intercept_point:
            paddle.position = self.game.to_pygame(Vec2d(intercept_point))

class Box2dGameController(RobotController):

    def __init__(self, game):
        self.game = game
        self.game.remove_player(self.game.players[0])
        self.control_player = self.game.add_player(density=1e10)

    def move_to(self, intercept_point):
        paddle = self.control_player

        if intercept_point:
            paddle.position = self.game.to_world(intercept_point[0], intercept_point[1])
