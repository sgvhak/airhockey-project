#!/usr/bin/env python

from Box2D import *

PPM=275 # pixels per meter
#PPM=7 # old scaling

class AirHockeyTable(object):

    def __init__(self, screen_width, screen_height):
        self.width = float(screen_width) / PPM
        self.height = float(screen_height) / PPM

        # Initialize world
        self.world = b2World(gravity = (0, 0))

        self.offset = b2Vec2(0, self.height / 6)
        self.table_height = int(self.height / 1.5)
        self.table_width = self.width

        # Wall thickness 1"
        self.wt = 7.0 / PPM

        # Goal width
        self.gw = 35.0 / PPM

        self.walls = self.world.CreateStaticBody(
                shapes=[ 
                        # top horizontal
                        b2EdgeShape(vertices=[b2Vec2(self.wt, self.wt) + self.offset, 
                                              b2Vec2(self.table_width-self.wt, self.wt) + self.offset]),
                        # bottom horizontal
                        b2EdgeShape(vertices=[b2Vec2(self.wt, self.table_height-self.wt) + self.offset, 
                                              b2Vec2(self.table_width-self.wt, self.table_height-self.wt) + self.offset]),
                        # left-top vertical
                        b2EdgeShape(vertices=[b2Vec2(self.wt, self.wt) + self.offset, 
                                              b2Vec2(self.wt, (self.table_height-self.gw)/2) + self.offset]),
                        # left-bottom vertical
                        b2EdgeShape(vertices=[b2Vec2(self.wt, (self.table_height+self.gw)/2) + self.offset, 
                                              b2Vec2(self.wt, self.table_height-self.wt) + self.offset]),
                        # right-top vertical
                        b2EdgeShape(vertices=[b2Vec2(self.table_width-self.wt, self.wt) + self.offset, 
                                              b2Vec2(self.table_width-self.wt, (self.table_height-self.gw)/2) + self.offset]),
                        # right-bottom vertical
                        b2EdgeShape(vertices=[b2Vec2(self.table_width-self.wt, (self.table_height+self.gw)/2) + self.offset, 
                                              b2Vec2(self.table_width-self.wt, self.table_height-self.wt) + self.offset]),
                    ]
                ) 

        self.pucks = []
        self.players = []

        self.add_puck()

    def add_circle(self, pos, radius, density=1.0):
        fixture=b2FixtureDef(shape=b2CircleShape(radius=radius, p=(0,0)), density=density, restitution=0.90, friction=0.1)
        circle = self.world.CreateDynamicBody(position=pos, fixtures=fixture)
        return circle

    def add_puck(self):
        puck = self.add_circle(b2Vec2(self.table_width / 2, self.table_height / 2) + self.offset, 9.0 / PPM, 1)
        self.pucks.append(puck)
        return puck

    def remove_puck(self, puck):
        if not puck in self.pucks:
            raise Exception("object is not a puck")

        self.world.DestroyBody(puck)
        self.pucks.remove(puck)
