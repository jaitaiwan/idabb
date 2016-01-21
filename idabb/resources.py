import pyglet
from .config import RESOURCES


pyglet.resource.path = RESOURCES['paths']
pyglet.resource.reindex()