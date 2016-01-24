from .graphics import Box
from .sprite import Sprite

class Platform(Sprite):
    def __init__(self, *args, **kwargs):
        self.height = 5
        self.width = 5
        self.distance = 30
        self.box = Box(**kwargs)
        self.name = 'platform'
        self.listen_down = True
        super().__init__(self.box, **kwargs)

    def update(self, drawables):
        if not getattr(self, 'qbit', None):
            self.set_quadrant()

    def draw(self):
        if self.color is False:
            return
        self.box.draw()

class Border(Sprite):
    def __init__(self, *args, **kwargs):
        self.height = 5
        self.width = 5
        self.distance = 30
        self.box = Box(**kwargs)
        self.name = 'platform'
        super().__init__(self.box, **kwargs)

    def update(self, drawables):
        if not getattr(self, 'qbit', None):
            self.set_quadrant()

    def draw(self):
        if self.color is False:
            return
        self.box.draw()
