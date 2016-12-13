import pyglet
import config


class Entity():
    def __init__(self, name, x, y, ascii, image_path):
        self._name = name
        self._x = x
        self._y = y
        self._ascii = ascii

        self._map = None

        self._image_path = image_path
        self._image = pyglet.image.load(image_path)
        self._sprite = pyglet.sprite.Sprite(self._image,
                                            x * config.mapdata['tile_size'],
                                            y * config.mapdata['tile_size'])

    def __str__(self):
        string = 'Name: ' + self._name + '; Position: '
        + str(self._x) + ','
        + str(self._y)

        return string

    def initialize(self, root_map=None, batch=None):
        if self._map is not None:
            self.ocupy_position()
        elif root_map is not None:
            self.set_map(root_map)
        if self.get_batch() is None and batch is not None:
            self.set_batch(batch)

    def set_position(self, x, y, force=False):
        if force:
            self.unocupy_position()
            self._x = x
            self._y = y
            self.update_position()
        else:
            if self._map.tiles[y][x]._is_walkable:
                self.unocupy_position()
                self.x = _x
                self.y = _y
                self.update_position()

    def add_position(self, x, y, force=False):
        if force:
            self.unocupy_position()
            self._x += x
            self._y += y
            self.update_position()
        else:
            if self._map._tiles[self._y + y][self._x + x]._is_walkable:
                self.unocupy_position()
                self._x += x
                self._y += y
                self.update_position()

    def get_position(self):
        return self._x, self._y

    def update_position(self):
        self.ocupy_position()
        self._sprite.set_position(self._x * config.mapdata['tile_size'],
                                  self._y * config.mapdata['tile_size'])

    def ocupy_position(self):
        self._map._tiles[self._y][self._x]._is_walkable = False
        self._map._tiles[self._y][self._x]._entity = self

    def unocupy_position(self):
        self._map._tiles[self._y][self._x]._is_walkable = True
        self._map._tiles[self._y][self._x]._entity = None

    def save(self):
        return {'name': self._name, 'x': self._x, 'y': self._y,
                'ascii': self._ascii, 'imagePath': self._image_path}

    def set_batch(self, batch):
        self._sprite.batch = batch

    def get_batch(self):
        return self._sprite.batch

    def set_map(self, root_map):
        self._map = root_map


class Player(Entity):
    def move(self, key):
        if key == pyglet.window.key.UP:
            self.add_position(0, 1)
        elif key == pyglet.window.key.DOWN:
            self.add_position(0, -1)
        elif key == pyglet.window.key.RIGHT:
            self.add_position(1, 0)
        elif key == pyglet.window.key.LEFT:
            self.add_position(-1, 0)
