import pyglet
import config

from pyglet.window import key

DIRECTION = {'UP': (0, 1), 'DOWN': (0, -1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}


class Entity():
    def __init__(self, _name, _position_x, _position_y, _graphic):
        self.name = _name
        self.position_x = _position_x
        self.position_y = _position_y
        self.graphic = pyglet.image.load(_graphic)

        self.sprite = pyglet.sprite.Sprite(self.graphic,
                                           _position_x * config.TILE_SIZE,
                                           _position_y * config.TILE_SIZE)

    def set_position(self, _x, _y):
        self.position_x = _x
        self.position_y = _y

    def add_position(self, _x, _y):
        self.position_x += _x
        self.position_y += _y
