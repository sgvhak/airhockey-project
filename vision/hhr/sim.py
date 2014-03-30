# Adapted from:
# https://github.com/robogeek42/Air-Hockey

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import math, sys, random
import numpy as np

class AirHockeyTable(object):

    def __init__(self, width, height):
        ## Balls
        self.pucks = []
           
        self.width = width
        self.height = height

        ### Physics stuff
        self.space = pymunk.Space(50)
        self.space.gravity = (0.0,0.0)

        # Wall thickness
        self.wt = 5.0

        # Goal width
        self.gw = self.width/4.0

        ### walls
        static_body = pymunk.Body()
        self.static_lines = [pymunk.Segment(static_body, (self.wt, self.wt), (self.width-self.wt, self.wt), 1.0),
                             pymunk.Segment(static_body, (self.wt, self.height-self.wt), (self.width-self.wt, self.height-self.wt), 1.0),
                             pymunk.Segment(static_body, (self.wt, self.wt), (self.wt, (self.height-self.gw)/2), 1.0),
                             pymunk.Segment(static_body, (self.wt, (self.height+self.gw)/2), (self.wt, self.height-self.wt), 1.0),
                             pymunk.Segment(static_body, (self.width-self.wt, self.wt), ((self.width-self.wt), (self.height-self.gw)/2), 1.0),
                             pymunk.Segment(static_body, (self.width-self.wt, (self.height+self.gw)/2), (self.width-self.wt, self.height-self.wt), 1.0)
                             ]  
        for line in self.static_lines:
            line.elasticity = 0.7
            line.group = 1
        self.space.add(self.static_lines)

        # Add the ball
        self.add_puck()

    def add_puck(self):
        radius=10
        mass=1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        ball_body = pymunk.Body(mass, inertia)
        ball_body.position=(self.width/2,self.height/2)

        mainball = pymunk.Circle(ball_body, radius, (0,0))
        mainball.elasticity = 0.95
        self.space.add(ball_body, mainball)
        self.pucks.append(mainball)
        #ball_body.apply_impulse((40.0,0.0), (0,0))

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

    def add_player(self):
        pmass=3
        pradius=20
        p1inertia = pymunk.moment_for_circle(pmass, 0, pradius, (0,0))
        self.p1_body = pymunk.Body(pmass, p1inertia)
        self.p1_body.position=(self.width-self.width/8, self.height/2)

        self.p1_shape = pymunk.Circle(self.p1_body, pradius, (0,0))
        self.p1_shape.elasticity = 0.95
        self.space.add(self.p1_body, self.p1_shape)
        self.players.append(self.p1_shape)

    def draw_table(self):
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, 0.0], [self.width, self.wt]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, self.height-self.wt], [self.width, self.height]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, 0.0], [self.wt, (self.height-self.gw)/2]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, (self.height+self.gw)/2], [self.wt,self.height]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[self.width-self.wt, 0.0], [self.width, (self.height-self.gw)/2]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[self.width-self.wt, (self.height+self.gw)/2], [self.width,self.height]], 0)

        pygame.draw.line(self.screen, THECOLORS["grey"], (self.width/2, self.wt), (self.width/2, self.height-self.wt), 2)
        circrad=1.2*self.gw/2
        pygame.draw.circle(self.screen, THECOLORS["grey"], (self.width/2, self.height/2), int(circrad), 2)
        pygame.draw.arc(self.screen, THECOLORS["grey"], [[-circrad, self.height/2-circrad], [+circrad,self.height/2+circrad]], 270, 90, 2)

        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = self.to_pygame(pv1)
            p2 = self.to_pygame(pv2)
            pygame.draw.lines(self.screen, THECOLORS["black"], False, [p1,p2])
 
    def process_frame(self):
        running = True

        mpos = pygame.mouse.get_pos()
        self.mouse_body.position = self.from_pygame( Vec2d(mpos) )
        self.mouse_body.angle = 0
        self.mouse_body.angular_velocity = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1: # LMB
                #selected = space.point_query_first(self.from_pygame(Vec2d(mpos)))
                #if selected != None:
                self.p1_body.position = self.mouse_body.position
                self.joint1 = pymunk.PivotJoint(self.mouse_body, self.p1_body, (0,0), (0,0) )
                self.space.add(self.joint1)

            elif event.type == MOUSEBUTTONUP:
                if self.joint1 != None:
                    self.space.remove(self.joint1)
                self.joint1 = None
        
        self.p1_body.angular_velocity=0
      
        ### Clear screen
        self.screen.fill(THECOLORS["white"])
        
        ### Draw 
        self.draw_table()

        for ball in self.pucks:
            p = self.to_pygame(ball.body.position)
            #if p[0] < 0:
            #    score['p1'] += 1
            #if p[0] >self.width:
            #    score['p2'] += 1

            if p[0] < 0 or p[0]>self.width:
                self.add_puck()
                self.space.remove(ball)
                self.pucks.remove(ball)

            pygame.draw.circle(self.screen, THECOLORS["purple"], p, int(ball.radius), 0)

        p = self.to_pygame(self.p1_body.position)
        pygame.draw.circle(self.screen, THECOLORS["darkgreen"], p, int(self.p1_shape.radius), 0)
        pygame.draw.circle(self.screen, THECOLORS["black"], p, int(self.p1_shape.radius+1), 2)
        pygame.draw.circle(self.screen, THECOLORS["black"], p, int(self.p1_shape.radius/2), 1)

        ### Update physics
        dt = 1.0/60.0/5.
        for x in range(5):
            self.space.step(dt)
        
        ### Flip screen
        pygame.display.flip()
        self.clock.tick(50)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

        return running

    def to_pygame(self, p):
        """Small hack to convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+self.height)

    def from_pygame(self, p):
        """Small hack to convert pymunk to pygame coordinates"""
        return int(p.x), int(-p.y+self.height)

    def get_frame(self):
        frame = np.fromstring(pygame.image.tostring(self.screen, 'RGB'), dtype=np.uint8).reshape((self.height, self.width, 3))
        return frame

if __name__ == "__main__":
    ah = AirHockeyGame(640, 480)

    running = True
    while running:
        running = ah.process_frame()
    sys.exit(0)
