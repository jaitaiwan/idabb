import pyglet

class Shape():
    """ Defines some of the common things we need for all our GL shapes """
    def __init__(self, width=50, height=100, x=0, y=0, color=(255,255,255,255), **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.__dict__.update(kwargs)

    @property
    def cx(self):
        """ Get the center x position """
        return self.x + (self.width/2)

    @cx.setter
    def cx(self, cx):
        self.x = cx - (self.width/2)

    @property
    def cy(self):
        """ Gets the center y position """
        return self.y + (self.height/2)

    @cy.setter
    def cy(self, cy):
        self.y = cy - (self.height/2)

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y

    @property
    def top(self):
        return self.y + self.height

    @property
    def red(self):
        return self.color[0]

    @property
    def green(self):
        return self.color[1]

    @property
    def blue(self):
        return self.color[2]

    @property
    def alpha(self):
        return self.color[3]

class Triangle(Shape):
    """ Draws isosceles and equalateral triangles """
    @property
    def verticies(self):
        return (
            self.left, self.bottom,
            self.right, self.bottom,
            self.cx, self.top
        )

    @property
    def vertice_colors(self):
        return self.color * 3

    def draw(self):
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES, (
            'v2f', self.verticies,
        ), ('c4f', self.vertice_colors))

class Box(Shape):
    """ Draws rectangles and squares """
    @property
    def verticies(self):
        return (
            self.left, self.bottom, #bottom left corner
            self.left, self.top, #top left corner
            self.right, self.top, #top right corner
            self.right, self.bottom #top bottom corner
        )
    
    @property
    def vertice_colors(self):
        return self.color * 4

    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, (
            'v2f', self.verticies,
        ), ('c4f', self.vertice_colors))