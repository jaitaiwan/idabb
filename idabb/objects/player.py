from .sprite import Sprite
from .graphics import Box, Triangle
from math import cos, atan, atan2, sin, degrees
from pyglet.resource import image
from pyglet.window import key

def is_negative(number):
    if number < 0:
        return -1
    else: return 1

def quadrant_help(i):
    s = '{0:064b}'.format(i)[::-1]
    ns = ''
    for i, c in enumerate(s):
        val = int(c) * 2**i
        if val:
            ns += str(val) + ','
    return ns

class Player(Sprite):
    def __init__(self, *args, image=image('assets/blue_box.png'), **kwargs):
        super().__init__(image, **kwargs)
        self.__dict__.update(kwargs)
        self.aim_cursor = AimCursor(mouse_angle=0.00, player_x=self.cx, player_y=self.cy)

        # Setup Player Movement
        self.max_velocity = 10
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 2
        self.quad_coefficient = 0.15
        self.animation_time = 5
        self.is_jumping = False
        self.is_falling = False
        self.quadrant_setup = False

        # Setup Mouse
        self.mouse_angle = 0
        self.mouse_dx = 0
        self.mouse_dy = 0
        self.mouse_velocity = 4

        # Setup Physics
        self.gravity = 5
        self.mass = 5
        self.terminal_velocity = self.max_velocity * self.gravity
        self.max_jumps = 2
        self.jumps = 0


        self.keys_pressed = {}

    def draw(self):
        super().draw()
        self.aim_cursor.draw()

    def mouse_move(self, x2, y2, dx, dy):
        # Work out the angle of the mouse
        #if self.mouse_ticks > self.max_mouse_ticks:
        if abs(dy) > self.mouse_velocity or abs(dx) > self.mouse_velocity:
            # self.mouse_ticks = 0
            self.mouse_angle = atan2(self.mouse_dy, self.mouse_dx)
            self.aim_cursor.update(mouse_angle=self.mouse_angle, player_x=self.cx, player_y=self.cy)
            self.mouse_dy = dy
            self.mouse_dx = dx
        self.mouse_dx += dx
        self.mouse_dy += dy

    def check_keys(self):
        if self.on_key(key.A) and abs(self.vel_x) < self.max_velocity:
            self.vel_x -=  self.vel_x_inc()
        elif self.on_key(key.D) and abs(self.vel_x) < self.max_velocity:
            self.vel_x += self.vel_x_inc()

        if abs(self.vel_x) > 0 and (not self.on_key(key.A) and not self.on_key(key.D)):
            self.vel_x += self.vel_x_inc() * self.invert_sign(self.vel_x) * -1

        if self.on_key(key.S) and abs(self.vel_y) < self.max_velocity:
            self.is_falling = True
            self.vel_y -= 5

    def check_falling(self):
        if self.is_falling and self.vel_y > (self.max_velocity * -1):
            self.vel_y += ((abs(self.vel_y) * self.quad_coefficient + self.quad_coefficient) * self.acceleration) *-1

        if self.is_falling is False:
            self.vel_y = 0

    def update(self, elements):
        if self.vel_y or self.vel_x:
            self.set_quadrant()
        self.check_keys() # Check to see if we're moving
        self.check_intersections(elements)
        self.check_falling() # check to see if we're falling
        self.x += self.vel_x
        self.y += self.vel_y
        # print(self.x, self.y)
        self.aim_cursor.update(mouse_angle=self.mouse_angle, player_x=self.cx, player_y=self.cy)

    def vel_x_inc(self):
        return (abs(self.vel_x) * self.quad_coefficient 
            + self.quad_coefficient)* self.acceleration

    def on_key(self, key):
        return key in self.keys_pressed and self.keys_pressed[key]

    def on_key_press(self, symbol, modifiers):
        self.keys_pressed[symbol] = True
        method = getattr(self, 'key_press_'+str(symbol), None)
        if method:
            method(modifiers)

    def on_key_release(self, symbol, modifiers):
        self.keys_pressed[symbol] = False
        method = getattr(self, 'key_release_'+str(symbol), None)
        if method:
            method(modifiers)

    def key_press_119(self, modifiers):
        if self.on_key(key.W) and abs(self.vel_y) < self.max_velocity and self.jumps < self.max_jumps:
            self.is_falling = True
            self.vel_y = self.max_velocity*5
            self.jumps += 1

    def check_platforms(self, element):
        result = 0

        if not element.name == 'platform':
            return result

        # Setup direction variables
        if self.vel_x < 0:
            direction_x = Sprite.LEFT
        elif self.vel_x == 0:
            direction_x = Sprite.STATIC_X
        else:
            direction_x = Sprite.RIGHT

        if self.vel_y < 0:
            direction_y = Sprite.DOWN
        elif self.vel_y == 0:
            direction_y = Sprite.STATIC_Y
        else:
            direction_y = Sprite.UP

        if direction_y != Sprite.UP:
            if self.intersects(
                element.left, 
                element.right) and self.velocity_intersects_y(
                element.top, direction_y):
                result += direction_y
                print(result)

        if self.intersects(element.bottom, element.top, x_or_y='y'):
            if direction_x == Sprite.RIGHT and self.velocity_intersects_x(element.left, direction_x):
                result += direction_x
            elif direction_x == Sprite.LEFT and self.velocity_intersects_x(element.right, direction_x):
                result += direction_x

        return result

        

    def check_boundary(self, element):
        pass

    def check_intersections(self, drawables):
        on_platform = False
        for element in drawables:
            # other element must have quadrants
            if not getattr(element, 'qbit', None):
                continue

            if getattr(element, 'listen_down', None):
                if self.on_key(key.S):
                    continue
            
            # if we have a matching quadrant
            if element.top == 10:
                pass
                # print('checking elements quadrants '+ quadrant_help(element.qbit) + ' against ' + quadrant_help(self.qbit))
                # print(quadrasnt_help(element.qbit & self.qbit))
            if element.qbit & self.qbit:
                # Get the element to do a finer check
                result = self.check_platforms(element)
                if result:
                    if result & Sprite.LEFT:
                        self.left = element.right+0.5
                        self.vel_x = 0

                    elif result & Sprite.RIGHT:
                        self.right = element.left-0.5
                        self.vel_x = 0
                    
                    if result & (Sprite.DOWN):
                        on_platform = True
                        self.is_falling = False
                        self.y = element.top+0.5
                        self.jumps = 0
                #self.check_collision(element)
                
        if on_platform is False:
            self.is_falling = True

class AimCursor(Sprite):
    def __init__(self, *args, player_x=0, player_y=0, mouse_angle=0, **kwargs):
        self.height = 5
        self.width = 5
        self.distance = 30
        self.aim_box = Box(x=player_x, 
                    y=player_y, 
                    height=self.height, width=self.width)
        self.mouse_angle = mouse_angle
        super().__init__(self.aim_box, **kwargs)
        self.update(mouse_angle=mouse_angle, player_y=player_y, player_x=player_x)

    def update(self, player_x=0, player_y=0, mouse_angle=0):
        x_distance = cos(mouse_angle)*self.distance
        y_distance = sin(mouse_angle)*self.distance
        self.aim_box.x = player_x + x_distance
        self.aim_box.y = player_y + y_distance

    def draw(self):
        self.aim_box.draw()
