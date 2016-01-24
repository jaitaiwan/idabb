import pyglet
from .config import WINDOW
from .game import drawables
from .objects.graphics import Box
from .objects import colors

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        kwargs['width'] = WINDOW['width']
        kwargs['height'] = WINDOW['height']
        super().__init__(*args, **kwargs)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.fps_display.update_period = 0.10
        self.set_exclusive_mouse(True)

        self.rows = WINDOW['quadrant_rows']
        self.columns = WINDOW['quadrant_columns']
        self.setup_quadrants()
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def on_draw(self):
        self.clear()
        #self.draw_quads()
        for element in drawables:
            element.draw()
        self.fps_display.draw()

    def draw_quads(self):
        for index in range(0, len(self.quadrants)):
            quad = self.quadrants[index]
            width = quad[2] - quad[0]
            height = quad[3] - quad[1]
            Box(x=quad[0], y=quad[1], height=height, width=width, color=colors.GREEN, outline=True).draw()

    def update(self, t):
        for element in drawables:
            if not getattr(element, 'quadrant_setup', None):
                element.quadrant_setup = self.quadrants
            if getattr(element, 'update', None):
                element.update(drawables)

        # self.check_collisions()

    def check_collisions(self):
        for element in drawables:
            # Element must have an check_collision and quadrant setup
            if not getattr(element, 'check_collision', None) or not getattr(element, 'quadrant_setup', None):
                continue

            # Loop over this element
            for other_element in drawables:
                # other element must have quadrants
                if not getattr(other_element, 'qbit', None):
                    continue
                
                # if we have a matching quadrant
                if other_element.qbit & element.qbit:
                    # Get the element to do a finer check
                    element.check_collision(other_element)

    
    def on_mouse_motion(self, x, y, dx, dy):
        for element in drawables:
            if getattr(element, 'mouse_move', None):
                element.mouse_move(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if pyglet.window.key.ESCAPE is symbol:
            self.set_exclusive_mouse(False)

        for element in drawables:
            if getattr(element, 'on_key_press', None):
                element.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for element in drawables:
            if getattr(element, 'on_key_release', None):
                element.on_key_release(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.set_exclusive_mouse(True)

    def setup_quadrants(self):
        column_width = self.width / self.columns
        row_height = self.height / self.rows
        coordinates = []

        quadrant_num = 1
        i = 0
        for row in range(0, self.rows):
            for column in range(0, self.columns):
                bottom_left = (column*column_width, row*row_height)
                coordinates.append( (bottom_left[0], bottom_left[1],
                    bottom_left[0]+column_width, bottom_left[1]+row_height) )
                i +=1 

        self.quadrants = coordinates

    