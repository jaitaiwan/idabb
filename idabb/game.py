import pyglet
from .config import WINDOW
from .objects.player import Player
from .objects.inanimate import Platform, Border
from .objects import colors

drawables = []

drawables.append(Border(x=0,y=0, width=WINDOW['width'], height=WINDOW['border_size'], color=colors.TRANSPARENT))
drawables.append(Border(x=0,y=0, width=WINDOW['border_size'], height=WINDOW['height'], color=colors.TRANSPARENT))
drawables.append(Border(x=WINDOW['width']-WINDOW['border_size'],y=0, width=WINDOW['border_size'], height=WINDOW['height'], color=colors.TRANSPARENT))
drawables.append(Border(x=WINDOW['border_size'],y=WINDOW['height']-WINDOW['border_size'], width=WINDOW['width'], height=WINDOW['border_size'], color=colors.TRANSPARENT))
drawables.append(Platform(x=150, y=100, color=colors.RED, width=200, height=20))
drawables.append(Platform(x=250, y=300, color=colors.RED, width=200, height=20))
drawables.append(Player(x=150, y=150, color=colors.BLUE, name='play'))