from .sprite import Sprite
from .graphics import Box, Triangle
from math import cos, tan, atan2, sqrt

def is_negative(number):
    if number < 0:
        return -1
    else: return 1

class Player(Sprite):
    def __init__(self, *args, velocity=5, **kwargs):
        resource = Box(**kwargs)
        
        self.resource = resource
        self.max_velocity = velocity
        self.velocity = 0
        self.acceleration = 0.05
        super().__init__(resource, **kwargs)

    def draw(self):
        self.resource.draw()

    @property
    def x(self):
        return self.resource.x

    @property
    def y(self):
        return self.resource.y

    @x.setter
    def x(self, x):
        self.resource.x = x


    @y.setter
    def y(self, y):
        self.resource.y = y

    @property
    def cx(self):
        return self.resource.cx

    @cx.setter
    def cx(self, value):
        self.resource.cx = value

    @property
    def cy(self):
        return self.resource.cy

    @cy.setter
    def cy(self, value):
        self.resource.cy = value

    def mouse_move(self, )