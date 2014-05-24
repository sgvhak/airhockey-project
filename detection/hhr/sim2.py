#!/usr/bin/env python

import pygame
from pygame.locals import *

from Box2D import *

#PPM=275 # pixels per meter
PPM=7 # old scaling
TARGET_FPS=60
TIME_STEP=1.0/TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 320,240

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
                        b2EdgeShape(vertices=[b2Vec2(self.wt, self.wt) + self.offset, 
                                              b2Vec2(self.table_width-self.wt, self.wt) + self.offset]),
                        b2EdgeShape(vertices=[b2Vec2(self.wt, self.table_height-self.wt) + self.offset, 
                                              b2Vec2(self.table_width-self.wt, self.table_height-self.wt) + self.offset]),
                        b2EdgeShape(vertices=[b2Vec2(self.wt, self.wt) + self.offset, 
                                              b2Vec2(self.wt, (self.table_height-self.gw)/2) + self.offset]),
                        b2EdgeShape(vertices=[b2Vec2(self.wt, (self.table_height+self.gw)/2) + self.offset, 
                                              b2Vec2(self.wt, self.table_height-self.wt) + self.offset]),
                        b2EdgeShape(vertices=[b2Vec2(self.table_width-self.wt, self.wt) + self.offset, 
                                              b2Vec2(self.table_width-self.wt, (self.table_height-self.gw)/2) + self.offset]),
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
        self.pucks.append( self.add_circle(b2Vec2(self.width - self.width / 2, self.height / 2) + self.offset, 9.0 / PPM, 1) )

    def remove_puck(self, puck):
        if not puck in self.pucks:
            raise Exception("object is not a puck")

        self.world.DestroyBody(puck)
        self.pucks.remove(puck)

colors = {
    b2_staticBody  : (255,255,255,255),
    b2_dynamicBody : (127,127,127,255),
    b2_kinematicBody: (127,127,230,255),
    'mouse_point'     : b2Color(0,1,0),
    'joint_line'      : b2Color(0.8,0.8,0.8),
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
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

    def add_player(self):
        self.players.append( self.add_circle(b2Vec2(self.width - self.width / 8, self.height / 2) + self.offset, 11.0 / PPM, 3) )

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

    def to_world(self, x, y):
        return b2Vec2(x / PPM, (self.screen_height - y) / PPM)

    def to_screen(self, point):
        return ( int(point.x) * PPM, int(self.screen_height - point.y * PPM) )

    def fix_vertices(self, vertices):
        return [self.to_screen(v) for v in vertices]

    def draw_polygon(self, polygon,  body, fixture):
        transform=body.transform
        vertices=self.fix_vertices([transform*v for v in polygon.vertices])
        pygame.draw.polygon(self.screen, [c/2.0 for c in colors[body.type]], vertices, 0)
        pygame.draw.polygon(self.screen, colors[body.type], vertices, 1)

    def draw_circle(self, circle, body, fixture):
        position=self.fix_vertices([body.transform*circle.pos])[0]
        pygame.draw.circle(self.screen, colors[body.type], position, int(circle.radius*PPM))

    def draw_edge(self, edge, body, fixture):
        vertices=self.fix_vertices([body.transform*edge.vertex1, body.transform*edge.vertex2])
        pygame.draw.line(self.screen, colors[body.type], vertices[0], vertices[1])

    def draw_loop(self, loop, body, fixture):
        transform=body.transform
        vertices=self.fix_vertices([transform*v for v in loop.vertices])
        v1=vertices[-1]
        for v2 in vertices:
            pygame.draw.line(self.screen, colors[body.type], v1, v2)
            v1=v2

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size, color, drawwidth=0)

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        pygame.draw.aaline(self.screen, color.bytes, p1, p2)


    def DrawCircle(self, center, radius, color, drawwidth=1):
        """
        Draw a wireframe circle given the center, radius, axis of orientation and color.
        """
        if radius < 1: radius = 1
        else: radius = int(radius)

        pygame.draw.circle(self.screen, color.bytes, center, radius, drawwidth)

    def render(self):
        # Check the event queue
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                return False
            elif event.type == MOUSEBUTTONDOWN:
                p = self.to_world(*event.pos)
                if event.button == 1: # left
                    mods = pygame.key.get_mods()
                    self.add_mouse_joint(p)
            elif event.type == MOUSEBUTTONUP:
                p = self.to_world(*event.pos)
                self.remove_mouse_joint(p)
            elif event.type == MOUSEMOTION:
                p = self.to_world(*event.pos)
                self.update_mouse_joint(p)

        # Remove old and add new puck if it goes out of the table
        for puck in self.pucks:
            if puck.position[0] < self.offset[0] or puck.position[0] > (self.width + self.offset[0]):
                self.remove_puck(puck)
                self.add_puck()

        self.screen.fill((0,0,0,0))
        # Draw the world
        for body in self.world.bodies:
            # The body gives us the position and angle of its shapes
            for fixture in body.fixtures:
                self.draw[fixture.shape.__class__](fixture.shape, body, fixture)

        # If there's a mouse joint, draw the connection between the object and the current pointer position.
        if self.mouseJoint:
            p1 = self.to_screen(self.mouseJoint.anchorB)
            p2 = self.to_screen(self.mouseJoint.target)

            self.DrawPoint(p1, 2, colors['mouse_point'])
            self.DrawPoint(p2, 2, colors['mouse_point'])
            self.DrawSegment(p1, p2, colors['joint_line'])

        # Make Box2D simulate the physics of our world for one step.
        # Instruct the world to perform a single step of simulation. It is
        # generally best to keep the time step and iterations fixed.
        # See the manual (Section "Simulating the World") for further discussion
        # on these parameters and their implications.
        self.world.Step(TIME_STEP, 8, 3)

        # Flip the screen and try to keep at the target FPS
        pygame.display.flip()
        self.clock.tick(TARGET_FPS)

        return True

if __name__=="__main__":
    ah_game = AirHockeyGame(320, 240)

    running = True
    while running:
        running = ah_game.render()
