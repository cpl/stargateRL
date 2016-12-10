import pyglet
import config

from pyglet.window import key


class Entity():
    def __init__(self, _name, _position_x, _position_y, _graphic, _map,
                 _health, _hp, _is_alive):
        self.name = _name
        self.position_x = _position_x
        self.position_y = _position_y
        self.graphic = pyglet.image.load(_graphic)
        self.root = _map
        self.health = _health
        self.max_hp = _hp

        self.is_alive = _is_alive

        self.sprite = pyglet.sprite.Sprite(self.graphic,
                                           _position_x * config.TILE_SIZE,
                                           _position_y * config.TILE_SIZE)

    def set_position(self, _x, _y):
        self.position_x = _x
        self.position_y = _y

    def add_position(self, _x, _y):
        self.position_x += _x
        self.position_y += _y


class Player(Entity):
    def move(self, _key):
        if _key == key.UP:
            if self.root.tiles[self.position_y+1][self.position_x].walkable:
                self.add_position(0, 1)
        elif _key == key.DOWN:
            if self.root.tiles[self.position_y-1][self.position_x].walkable:
                self.add_position(0, -1)
        elif _key == key.LEFT:
            if self.root.tiles[self.position_y][self.position_x-1].walkable:
                self.add_position(-1, 0)
        elif _key == key.RIGHT:
            if self.root.tiles[self.position_y][self.position_x+1].walkable:
                self.add_position(1, 0)
        self.sprite.set_position(self.position_x * config.TILE_SIZE,
                                 self.position_y * config.TILE_SIZE)
