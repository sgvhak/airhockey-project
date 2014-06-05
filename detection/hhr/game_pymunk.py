# Adapted from:
# https://github.com/robogeek42/Air-Hockey

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import math, sys, random
import numpy as np

from .sim_pymunk import AirHockeyTable

class AirHockeyGame(AirHockeyTable):

    def __init__(self, width, height):
        super(AirHockeyGame, self).__init__(width, height)
        
        pygame.init()

        ## players
        self.players = [] 

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Setup Player 1
        self.add_player()

        self.mouse_body = pymunk.Body()
        self.joint1=None

        ## Balls
        self.pucks = []

        # Add the ball
        self.add_puck()

    def add_puck(self):
        puck = super(AirHockeyGame, self).add_puck()
        self.pucks.append(puck)

    def remove_puck(self, puck):
        super(AirHockeyGame, self).remove_puck(puck)
        self.pucks.remove(puck)

    def add_player(self, mass=3, radius=11, on_left=False):
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        player_body = pymunk.Body(mass, inertia)
        if on_left:
            player_body.position=(self.width/8, self.height/2)
        else:
            player_body.position=(self.width-self.width/8, self.height/2)

        player_shape = pymunk.Circle(player_body, radius, (0,0))
        player_shape.elasticity = 0.95
        self.space.add(player_body, player_shape)
        self.players.append(player_shape)
        return player_shape

    def draw_table(self):
        # Draw table by drawing two brown rectangles outside of goal bounds, then a whole one over the playing surface
        pygame.draw.rect(self.screen, THECOLORS["brown"], Rect(self.offset, (self.table_width, self.table_height/2-self.gw/2)), 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], Rect(self.offset+Vec2d(0, self.table_height/2+self.gw/2), (self.table_width, self.table_height/2-self.gw/2)), 0)
        pygame.draw.rect(self.screen, THECOLORS["white"], Rect(self.offset+self.wt, (self.table_width-self.wt*2, self.table_height-self.wt*2)), 0)

        # Draw center line and starting posistion circle
        pygame.draw.line(self.screen, THECOLORS["grey"], Vec2d(self.table_width/2, self.wt) + self.offset, (self.table_width/2, self.table_height-self.wt) + self.offset, 2)
        circrad=1.2*self.gw/2
        pygame.draw.circle(self.screen, THECOLORS["grey"], (self.width/2, self.height/2), int(circrad), 2)
        pygame.draw.arc(self.screen, THECOLORS["grey"], [[-circrad, self.height/2-circrad], [+circrad,self.height/2+circrad]], 270, 90, 2)

        # Draw where pymunk puts walls
        for line in self.walls:
            pv1 = line.body.position + line.a.rotated(line.body.angle)
            pv2 = line.body.position + line.b.rotated(line.body.angle)
            p1 = self.to_world(pv1)
            p2 = self.to_world(pv2)
            pygame.draw.lines(self.screen, THECOLORS["black"], False, [p1,p2])
            
    def render(self):
        running = True

        mpos = pygame.mouse.get_pos()
        self.mouse_body.position = self.to_screen( Vec2d(mpos) )
        self.mouse_body.angle = 0
        self.mouse_body.angular_velocity = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1: # LMB
                #selected = space.point_query_first(self.to_screen(Vec2d(mpos)))
                #if selected != None:
                p1_body = self.players[0].body
                p1_body.position = self.mouse_body.position
                self.joint1 = pymunk.PivotJoint(self.mouse_body, p1_body, (0,0), (0,0) )
                self.space.add(self.joint1)

            elif event.type == MOUSEBUTTONUP:
                if self.joint1 != None:
                    self.space.remove(self.joint1)
                self.joint1 = None
      
        ### Clear screen
        self.screen.fill(THECOLORS["black"])
        
        ### Draw 
        self.draw_table()

        for puck in self.pucks:
            p = self.to_world(puck.body.position)

            if p[0] < 0 or p[0]>self.width:
                self.remove_puck(puck)
                self.add_puck()

            pygame.draw.circle(self.screen, THECOLORS["red"], p, int(puck.radius), 0)

        for p_shape in self.players:
            p_body = p_shape.body
            p_body.angular_velocity = 0
            p = self.to_world(p_body.position)
            pygame.draw.circle(self.screen, THECOLORS["darkgreen"], p, int(p_shape.radius), 0)
            pygame.draw.circle(self.screen, THECOLORS["black"], p, int(p_shape.radius+1), 2)
            pygame.draw.circle(self.screen, THECOLORS["black"], p, int(p_shape.radius/2), 1)

        ### Update physics
        dt = 1.0/60.0/5.
        for x in range(5):
            self.space.step(dt)
        
        ### Flip screen
        pygame.display.flip()
        self.clock.tick(50)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

        return running

    def to_world(self, p):
        """Small hack to convert pymunk to pygame coordinates. (formerly to_pygame)"""
        return int(p.x), int(-p.y+self.height)  # invert the y axis

    def to_screen(self, p):
        """Small hack to convert pygame to pymunk coordinates. (formerly from_pygame)"""
        return int(p.x), int(-p.y+self.height)  # invert the y axis

    def get_frame(self):
        frame = np.fromstring(pygame.image.tostring(self.screen, 'RGB'), dtype=np.uint8).reshape((self.height, self.width, 3))
        return frame

if __name__ == "__main__":
    ah = AirHockeyGame(320, 240)

    running = True
    while running:
        running = ah.render()
    sys.exit(0)
