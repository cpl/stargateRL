import pyglet
import config

from pyglet.window import key


class Tile():

    def __init__(self, ascii, x, y, image_path,
                 is_walkable=False,
                 has_entity=False):

        self._ascii = ascii
        self._x = x
        self._y = y
        self._is_walkable = is_walkable

        self._entity = None

        self._image_path = image_path
        self._image = pyglet.image.load(image_path)
        self._sprite = pyglet.sprite.Sprite(self._image,
                                            x * config.mapdata['tile_size'],
                                            y * config.mapdata['tile_size'])

    def __str__(self):
        if self._entity is not None:
            return self._entity._ascii
        else:
            return self._ascii

    def save(self):
        jsonObject = {'ascii': self._ascii, 'x': self._x, 'y': self._y,
                      'imagePath': self._image_path}

        if self._entity is not None:
            jsonObject.update({'entity': self._entity.save()})

        return jsonObject


class Map():

    def __init__(self, len_x=0, len_y=0, name='SG_MAP'):
        self._tiles = [['' for _ in range(len_x)] for _ in range(len_y)]
        self._len_x = len_x
        self._len_y = len_y
        self._name = name

    def __str__(self):
        string = ''
        for row in reversed(self._tiles):
            string += '\n'
            for tile in row:
                string += str(tile)
        return string

    def set_batch(self, batch):
        for row in self._tiles:
            for tile in row:
                tile._sprite.batch = batch

    def load_map(self, file, json=False):
        with open(file, 'r') as input_file:
            for y, line in enumerate(reversed(input_file.readlines())):
                for x, tile in enumerate(line):
                    if tile == '#':
                        self._tiles[y][x] = Tile(tile, x, y,
                                                 config.graphx['wall'])
                    elif tile == '.':
                        self._tiles[y][x] = Tile(tile, x, y,
                                                 config.graphx['floor'], True)
                    elif tile == ']':
                        self._tiles[y][x] = Tile(tile, x, y,
                                                 config.graphx['door_c'])
                    elif tile == ')':
                        self._tiles[y][x] = Tile(tile, x, y,
                                                 config.graphx['door_o'], True)

    def save(self):
        jsonObject = []

        for row in self._tiles:
            jsonRow = []
            for tile in row:
                jsonRow.append(tile.save())
            jsonObject.append(jsonRow)

        return {'tiles': jsonObject, 'name': self._name}


class Selector():

    def __init__(self, image_path):
        self._x = 0
        self._y = 0

        self._image_path = image_path
        self._image = pyglet.image.load(image_path)

        self._sprite = pyglet.sprite.Sprite(self._image, self._x, self._y)

    def set_position(self, x, y):
        self._x = x
        self._y = y
        self._sprite.set_position(self._x*config.mapdata['tile_size'],
                                  self._y*config.mapdata['tile_size'])

        self.get_info()

    def move(self, symbol):
        if symbol == key.W and self._y < self._map._len_y-1:
            self.set_position(self._x, self._y+1)
        elif symbol == key.S and self._y > 0:
            self.set_position(self._x, self._y-1)
        elif symbol == key.D and self._x < self._map._len_x-1:
            self.set_position(self._x+1, self._y)
        elif symbol == key.A and self._x > 0:
            self.set_position(self._x-1, self._y)

    def get_info(self):
        print self._map._tiles[self._y][self._x].save()

    def on_mouse_motion(self, x, y, dx, dy):
        if config.mouse['enabled']:
            self.set_position(
                x/config.mapdata['tile_size'],
                y/config.mapdata['tile_size'])
