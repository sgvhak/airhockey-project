import pymunk
from pymunk import Vec2d

# For a table of 46" x 26" with table covering frame and a capture size of 320 x 240
# Table would be 320 px x 160 px
# ~7 px per in

class AirHockeyTable(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

        ### Physics stuff
        self.space = pymunk.Space(50)
        self.space.gravity = (0.0,0.0)

        # Wall thickness 1"
        self.wt = 7

        self.offset = Vec2d(0, self.height / 6)
        self.table_height = int(self.height / 1.5)
        self.table_width = self.width

        # Goal width
        self.gw = 40 

        ### Walls
        static_body = pymunk.Body()
            
        self.walls = [pymunk.Segment(static_body, Vec2d(self.wt, self.wt) + self.offset, 
                                                  Vec2d(self.table_width-self.wt, self.wt) + self.offset, 1.0),
                      pymunk.Segment(static_body, Vec2d(self.wt, self.table_height-self.wt) + self.offset, 
                                                  Vec2d(self.table_width-self.wt, self.table_height-self.wt) + self.offset, 1.0),
                      pymunk.Segment(static_body, Vec2d(self.wt, self.wt) + self.offset, 
                                                  Vec2d(self.wt, (self.table_height-self.gw)/2) + self.offset, 1.0),
                      pymunk.Segment(static_body, Vec2d(self.wt, (self.table_height+self.gw)/2) + self.offset, 
                                                  Vec2d(self.wt, self.table_height-self.wt) + self.offset, 1.0),
                      pymunk.Segment(static_body, Vec2d(self.table_width-self.wt, self.wt) + self.offset, 
                                                  Vec2d(self.table_width-self.wt, (self.table_height-self.gw)/2) + self.offset, 1.0),
                      pymunk.Segment(static_body, Vec2d(self.table_width-self.wt, (self.table_height+self.gw)/2) + self.offset, 
                                                  Vec2d(self.table_width-self.wt, self.table_height-self.wt) + self.offset, 1.0),
                      ]  
        for line in self.walls:
            line.elasticity = 0.7
            line.group = 1
        self.space.add(self.walls)

    def add_puck(self, position=None, radius=9, mass=1, elasticity=0.95):
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        puck_body = pymunk.Body(mass, inertia)

        if position:
            puck_body.position = position
        else:
            puck_body.position = (self.width/2, self.height/2)

        new_puck = pymunk.Circle(puck_body, radius, (0,0))
        new_puck.elasticity = elasticity
        self.space.add(puck_body, new_puck)

        return new_puck

    def remove_puck(self, puck):
        self.space.remove(puck)
