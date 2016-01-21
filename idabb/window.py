import pyglet
from .config import WINDOW
from .game import drawables

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        kwargs['width'] = WINDOW['width']
        kwargs['height'] = WINDOW['height']
        super().__init__(*args, **kwargs)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.fps_display.update_period = 0.10

    def on_draw(self):
        self.clear()
        self.update()

    def update(self):
        pyglet.clock.tick()
        for element in drawables:
            element.draw()
        self.fps_display.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        for element in drawables:
            if getattr(element, 'mouse_move', None):
                element.mouse_move(x, y)