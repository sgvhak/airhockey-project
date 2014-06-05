#!/usr/bin/env python

import math

import pygame
from pygame.locals import *
from pygame.color import *
  
import numpy as np

from Box2D import *

from .sim_box2d import AirHockeyTable, PPM

TARGET_FPS=60
TIME_STEP=1.0/TARGET_FPS

colors = {
    b2_staticBody  : (255,255,255,255),
    b2_dynamicBody : (127,127,127,255),
    b2_kinematicBody: (127,127,230,255),
    'mouse_point'   : b2Color(0,1,0),
    'joint_line'    : b2Color(0.8,0.8,0.8),
}

class fwQueryCallback(b2QueryCallback):
    def __init__(self, p): 
        super(fwQueryCallback, self).__init__()
        self.point = p
        self.fixture = None

    def ReportFixture(self, fixture):
        body = fixture.body
        if body.type == b2_dynamicBody:
            inside=fixture.TestPoint(self.point)
            if inside:
                self.fixture=fixture
                # We found the object, so stop the query
                return False
        # Continue the query
        return True

class AirHockeyGame(AirHockeyTable):

    def __init__(self, screen_width, screen_height):
        super(AirHockeyGame, self).__init__(screen_width, screen_height)

        self.screen_width = screen_width
        self.screen_height = screen_height

        # pygame setup
        self.screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
        self.clock = pygame.time.Clock()

        self.mouseJoint = None
        self.groundbody = self.world.CreateBody()

        self.add_player()

        self.draw = {
            b2PolygonShape: self.draw_polygon,
            b2CircleShape: self.draw_circle,
            b2EdgeShape: self.draw_edge,
            b2LoopShape: self.draw_loop,
        }

    def add_player(self, mass=3.0, radius=11.0):
        radius_meters = radius / PPM
        density = mass / (math.pi * radius * radius)
        player = self.add_circle(b2Vec2(self.table_width - self.table_width / 8, self.table_height / 2) + self.offset, radius_meters, density=density) 
        self.players.append(player)
        return player

    def remove_player(self, player):
        if not player in self.players:
            raise Exception("object not a player")

        self.world.DestroyBody(player)
        self.players.remove(player)

    def add_mouse_joint(self, p):
        "Indicates that there was a left click at point p (world coordinates)"

        if self.mouseJoint != None:
            return

        # Create a mouse joint on the selected body (assuming it's dynamic)
        # Make a small box.
        aabb = b2AABB(lowerBound=p-(0.001, 0.001), upperBound=p+(0.001, 0.001))

        # Query the world for overlapping shapes.
        query = fwQueryCallback(p)
        self.world.QueryAABB(query, aabb)
        
        if query.fixture:
            body = query.fixture.body
            # A body was selected, create the mouse joint
            self.mouseJoint = self.world.CreateMouseJoint(
                    bodyA=self.groundbody,
                    bodyB=body, 
                    target=p,
                    maxForce=1000.0*body.mass)
            body.awake = True

    def remove_mouse_joint(self, p):
        "Left mouse button up."     

        if self.mouseJoint:
            self.world.DestroyJoint(self.mouseJoint)
            self.mouseJoint = None

    def update_mouse_joint(self, p):
        "Mouse moved to point p, in world coordinates."
        self.mouseWorld = p
        if self.mouseJoint:
            self.mouseJoint.target = p

    def to_world(self, pos):
        """Convert from screen coordinates to model coordinates :param pos: tuple of x and y coordinates"""
        x, y = pos
        return b2Vec2(x / PPM, y / PPM)

    def to_screen(self, point):
        return ( int(point.x * PPM), int(point.y * PPM) )

    def fix_vertices(self, vertices):
        return [self.to_screen(v) for v in vertices]

    def draw_polygon(self, polygon, body, fixture, color):
        transform=body.transform
        vertices=self.fix_vertices([transform*v for v in polygon.vertices])
        pygame.draw.polygon(self.screen, [c/2.0 for c in colors[body.type]], vertices, 0)
        pygame.draw.polygon(self.screen, color, vertices, 1)

    def draw_circle(self, circle, body, fixture, color):
        position=self.fix_vertices([body.transform*circle.pos])[0]
        pygame.draw.circle(self.screen, color, position, int(circle.radius*PPM))

    def draw_edge(self, edge, body, fixture, color):
        vertices=self.fix_vertices([body.transform*edge.vertex1, body.transform*edge.vertex2])
        pygame.draw.line(self.screen, color, vertices[0], vertices[1])

    def draw_loop(self, loop, body, fixture, color):
        transform=body.transform
        vertices=self.fix_vertices([transform*v for v in loop.vertices])
        v1=vertices[-1]
        for v2 in vertices:
            pygame.draw.line(self.screen, color, v1, v2)
            v1=v2

    def draw_body(self, body, color=None):
        if color == None:
            color = colors[body.type]

        for fixture in body.fixtures:
            self.draw[fixture.shape.__class__](fixture.shape, body, fixture, color)

    def render(self):
        # Check the event queue
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                return False
            elif event.type == MOUSEBUTTONDOWN:
                p = self.to_world(event.pos)
                if event.button == 1: # left
                    mods = pygame.key.get_mods()
                    self.add_mouse_joint(p)
            elif event.type == MOUSEBUTTONUP:
                p = self.to_world(event.pos)
                self.remove_mouse_joint(p)
            elif event.type == MOUSEMOTION:
                p = self.to_world(event.pos)
                self.update_mouse_joint(p)

        # Clear the frame
        self.screen.fill((0,0,0,0))

        for puck in self.pucks:
            # Remove old and add new puck if it goes out of the table
            if puck.position[0] < self.offset[0] or puck.position[0] > (self.width + self.offset[0]):
                self.remove_puck(puck)
                self.add_puck()
        
            # Draw puck
            self.draw_body(puck, THECOLORS["red"])

        for player in self.players:
            # Remove old and add new player if it goes out of the table
            if player.position[0] < self.offset[0] or player.position[0] > (self.width + self.offset[0]):
                self.remove_player(player)
                self.add_player()

            # Draw player paddle
            self.draw_body(player)

        # Draw the walls
        self.draw_body(self.walls)

        # If there's a mouse joint, draw the connection between the object and the current pointer position.
        if self.mouseJoint:
            p1 = self.to_screen(self.mouseJoint.anchorB)
            p2 = self.to_screen(self.mouseJoint.target)

            pygame.draw.circle(self.screen, colors['mouse_point'].bytes, p1, 2, 1)
            pygame.draw.circle(self.screen, colors['mouse_point'].bytes, p2, 2, 1)
            pygame.draw.aaline(self.screen, colors['joint_line'].bytes, p1, p2)

        # Make Box2D simulate the physics of our world for one step.
        # Instruct the world to perform a single step of simulation. It is
        # generally best to keep the time step and iterations fixed.
        # See the manual (Section "Simulating the World") for further discussion
        # on these parameters and their implications.
        self.world.Step(TIME_STEP, 6, 2)

        # Flip the screen and try to keep at the target FPS
        pygame.display.flip()
        self.clock.tick(TARGET_FPS)

        return True

    def get_frame(self):
        frame = np.fromstring(pygame.image.tostring(self.screen, 'RGB'), dtype=np.uint8).reshape((self.screen_height, self.screen_width, 3))
        return frame

if __name__=="__main__":
    ah_game = AirHockeyGame(320, 240)

    running = True
    while running:
        running = ah_game.render()
