class Sprite(object):
    LEFT = 1
    STATIC_X = 2
    RIGHT = 4
    DOWN = 10
    STATIC_Y = 20
    UP = 40

    def __init__(self, resource, **kwargs):
        self.image = resource
        self.__dict__.update(kwargs)
        self.quadrant_bit = 0

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x = value

    @property
    def right(self):
        return self.x + self.image.width

    @right.setter
    def right(self, value):
        self.x = value - self.image.width

    @property
    def top(self):
        return self.y + self.image.height

    @top.setter
    def top(self, value):
        self.y = value - self.image.height

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.y = value

    def draw(self):
        self.image.blit(self.x, self.y)

    @property
    def cx(self):
        return self.x + (self.image.width/2)

    @cx.setter
    def cx(self, value):
        self.x = self.x - (self.image.width/2)

    @property
    def cy(self):
        return self.y + (self.image.height/2)

    @cy.setter
    def cy(self, value):
        self.y = self.y - (self.image.height/2)

    def set_quadrant(self):
        self.qbit = 0
        if not self.quadrant_setup:
            return

        for index in range(0, len(self.quadrant_setup)):
            quads =self.quadrant_setup[index]
            x1 = quads[0]
            y1 = quads[1]
            x2 = quads[2]
            y2 = quads[3]
            # check each vertice to see if we intersect with a quadrant
            if self.intersects(x1, x2) and self.intersects(y1, y2, x_or_y='y'):
                self.qbit += 1 * 2**index

    def intersects(self, d1, d2, x_or_y='x'):
        if x_or_y == 'x':
            if self.left <= d1 and self.right >= d2:
                return True
            elif d1 <= self.left <= d2 or d1 <= self.right <= d2:
                return True
        else:
            if self.bottom <= d1 and self.top >= d2:
                return True
            elif d1 <= self.bottom <= d2 or d1 <= self.top <= d2:
                return True

        return False

    def inverse_intersects(self, d1, d2, x_or_y='x'):
        if x_or_y is 'x':
            if self.left <= d1 <= self.right or self.left <= d2 <= self.right:
                return True
        else:
            if self.bottom <= d1 <= self.top or self.bottom <= d2 <= self.top:
                return True

        return False



    def velocity_intersects_y(self, y, direction):
        if direction == self.UP:
            next_y = self.up + self.vel_y
            if next_y >= y >= self.up:
                return True
        elif direction == self.DOWN:
            next_y = self.y + self.vel_y
            # print('i am %d but I will be %d and the platform is %d' % (self.y, next_y, y))
            if self.y >= y >= next_y:
                return True
        elif direction == self.STATIC_Y:
            if self.y == y or self.top == y:
                return True

        return False

    def velocity_intersects_x(self, x, direction):
        if direction == self.RIGHT:
            next_x = self.right + self.vel_x
            if next_x >= x >= self.right:
                return True
        elif direction == self.LEFT:
            next_x = self.x + self.vel_x
            # print('i am %d but I will be %d and the platform is %d' % (self.x, next_x, x))
            if self.x >= x >= next_x:
                return True
        elif direction == self.STATIC_X:
            if self.x == x or self.right == x:
                return True

        return False

    @property
    def qbit(self):
        return self.quadrant_bit

    @qbit.setter
    def qbit(self, value):
        self.quadrant_bit = value

    def invert_sign (self, number):
        if number < 0: return -1
        else: return 1


    def easeInOutQuint(self, time, start_value, change_value, duration):
        time = duration/2/time
        if time < 1:
            return change_value/2*time**4 + start_value
        time -= 2
        return change_value/2*(time**4 + 2) + start_value