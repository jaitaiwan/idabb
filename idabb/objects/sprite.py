class Sprite(object):
    def __init__(self, resource, **kwargs):
        self.image = resource
        self.x = 0
        self.y = 0
        self.__dict__.update(kwargs)

    def intersect(self):
        """ Determine if two objects intersect """
        return not ((self.left > sprite.right)
                or (self.right < sprite.left)
                or (self.top < sprite.bottom)
                or (self.bottom > sprite.top))

    def collide(self, sprite_list):
        """ Determine if a collision is occuring """
        th_return = []
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                th_return.append(sprite)
        return th_return

    def collide_ocne(self, sprite_list):
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                return sprite

        return None

    @property
    def left(self):
        return self.x
    @property
    def right(self):
        return self.x + self.image.width

    @property
    def top(self):
        return self.y + self.image.height

    @property
    def bottom(self):
        return self.y

    def draw(self):
        self.image.blit(self.x, self.y)

    def update(self):
        pass