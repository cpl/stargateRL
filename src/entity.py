import pyglet
import config


class Entity():
    def __init__(self, name, x, y, root_map, ascii, image_path):
        self._name = name
        self._x = x
        self._y = y
        self._root_map = root_map
        self._ascii = ascii

        self._image_path = image_path
        self._image = pyglet.image.load(image_path)
        self._sprite = pyglet.sprite.Sprite(self._image,
                                            x * config.mapdata['tile_size'],
                                            y * config.mapdata['tile_size'])

        root_map._tiles[y][x]._is_walkable = False
        root_map._tiles[y][x]._entity = self

    def __str__(self):
        string = 'Name: ' + self._name + '; Position: '
        + str(self._x) + ','
        + str(self._y)

        return string

    def set_position(self, x, y, force=False):
        if force:
            self.unocupy_position()
            self._x = x
            self._y = y
            self.update_position()
        else:
            if self._root_map.tiles[y][x]._is_walkable:
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
            if self._root_map._tiles[self._y + y][self._x + x]._is_walkable:
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
        self._root_map._tiles[self._y][self._x]._is_walkable = False
        self._root_map._tiles[self._y][self._x]._entity = self

    def unocupy_position(self):
        self._root_map._tiles[self._y][self._x]._is_walkable = True
        self._root_map._tiles[self._y][self._x]._entity = None

    def save(self):
        return {'name': self._name, 'x': self._x, 'y': self._y,
                'ascii': self._ascii, 'imagePath': self._image_path}


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
