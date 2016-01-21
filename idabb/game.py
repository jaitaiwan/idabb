import pyglet
from .config import WINDOW
from .objects.player import Player
from .objects import colors

drawables = []

drawables.append(
    Player(x=0, y=0, color=colors.BLUE)
)