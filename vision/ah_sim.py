# Adapted from:
# https://github.com/robogeek42/Air-Hockey

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d
import math, sys, random

WINW=320
WINH=240
PI=3.14247

## Balls
balls = []
   
## players
players = []

# Wall thickness
wt=5.0
# Goal width
gw=WINW/4.0

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+WINH)

def from_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+WINH)
    
class AirHockey(object):

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINW, WINH))
        self.clock = pygame.time.Clock()

        ### Physics stuff
        self.space = pymunk.Space(50)
        self.space.gravity = (0.0,0.0)

        ### walls
        static_body = pymunk.Body()
        self.static_lines = [pymunk.Segment(static_body, (wt, wt), (WINW-wt, wt), 1.0),
                        pymunk.Segment(static_body, (wt, WINH-wt), (WINW-wt, WINH-wt), 1.0),
                        pymunk.Segment(static_body, (wt, wt), (wt, (WINH-gw)/2), 1.0),
                        pymunk.Segment(static_body, (wt, (WINH+gw)/2), (wt, WINH-wt), 1.0),
                        pymunk.Segment(static_body, (WINW-wt, wt), ((WINW-wt), (WINH-gw)/2), 1.0),
                        pymunk.Segment(static_body, (WINW-wt, (WINH+gw)/2), (WINW-wt, WINH-wt), 1.0)
                        ]  
        for line in self.static_lines:
            line.elasticity = 0.7
            line.group = 1
        self.space.add(self.static_lines)

        # Setup Player 1
        pmass=3
        pradius=20
        p1inertia = pymunk.moment_for_circle(pmass, 0, pradius, (0,0))
        self.p1_body = pymunk.Body(pmass, p1inertia)
        self.p1_body.position=(WINW-WINW/8, WINH/2)

        self.p1_shape = pymunk.Circle(self.p1_body, pradius, (0,0))
        self.p1_shape.elasticity = 0.95
        self.space.add(self.p1_body, self.p1_shape)
        players.append(self.p1_shape)

        self.mouse_body = pymunk.Body()
        self.joint1=None
        selected = None

        # Add the ball
        self.addball()

    def addball(self):
        radius=10
        mass=1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        ball_body = pymunk.Body(mass, inertia)
        ball_body.position=(WINW/2,WINH/2)

        mainball = pymunk.Circle(ball_body, radius, (0,0))
        mainball.elasticity = 0.95
        self.space.add(ball_body, mainball)
        balls.append(mainball)
        #ball_body.apply_impulse((40.0,0.0), (0,0))

    def draw_table(self):
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, 0.0], [WINW, wt]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, WINH-wt], [WINW, WINH]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, 0.0], [wt, (WINH-gw)/2]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[0.0, (WINH+gw)/2], [wt,WINH]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[WINW-wt, 0.0], [WINW, (WINH-gw)/2]], 0)
        pygame.draw.rect(self.screen, THECOLORS["brown"], [[WINW-wt, (WINH+gw)/2], [WINW,WINH]], 0)

        pygame.draw.line(self.screen, THECOLORS["grey"], (WINW/2, wt), (WINW/2, WINH-wt), 2)
        circrad=1.2*gw/2
        pygame.draw.circle(self.screen, THECOLORS["grey"], (WINW/2, WINH/2), int(circrad), 2)
        pygame.draw.arc(self.screen, THECOLORS["grey"], [[-circrad, WINH/2-circrad], [+circrad,WINH/2+circrad]], 270, 90, 2)

        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.lines(self.screen, THECOLORS["black"], False, [p1,p2])
 
    def game_frame(self):
        running = True

        mpos = pygame.mouse.get_pos()
        self.mouse_body.position = from_pygame( Vec2d(mpos) )
        self.mouse_body.angle = 0
        self.mouse_body.angular_velocity = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1: # LMB
                #selected = space.point_query_first(from_pygame(Vec2d(mpos)))
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

        for ball in balls:
            p = to_pygame(ball.body.position)
            #if p[0] < 0:
            #    score['p1'] += 1
            #if p[0] >WINW:
            #    score['p2'] += 1

            if p[0] < 0 or p[0]>WINW:
                self.addball()
                self.space.remove(ball)
                balls.remove(ball)

            pygame.draw.circle(self.screen, THECOLORS["purple"], p, int(ball.radius), 0)

        p = to_pygame(self.p1_body.position)
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

if __name__ == "__main__":
    ah = AirHockey()

    running = True
    while running:
        running = ah.game_frame()
    sys.exit(0)
