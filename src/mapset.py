import pyglet
import config

from pyglet.window import key


class Tile():

    def __init__(self, _ascii, _x, _y, _image,
                 _isWalkable=False,
                 _hasEntity=False):

        self.ascii = _ascii
        self.x = _x
        self.y = _y
        self.isWalkable = _isWalkable

        self.entity = None

        self.imagePath = _image
        self.image = pyglet.image.load(_image)
        self.sprite = pyglet.sprite.Sprite(self.image,
                                           _x * config.mapdata['tileSize'],
                                           _y * config.mapdata['tileSize'])

    def __str__(self):
        if self.entity is not None:
            return self.entity.ascii
        else:
            return self.ascii

    def save(self):
        _jsonObject = {'ascii': self.ascii, 'x': self.x, 'y': self.y,
                       'imagePath': self.imagePath}

        if self.entity is not None:
            _jsonObject.update({'entity': self.entity.save()})

        return _jsonObject


class Map():

    def __init__(self, _lenX=0, _lenY=0, _name='SG_MAP'):
        self.tiles = [['' for _ in range(_lenX)] for _ in range(_lenY)]
        self.lenX = _lenX
        self.lenY = _lenY
        self.name = _name

    def __str__(self):
        _string = ''
        for row in reversed(self.tiles):
            _string += '\n'
            for tile in row:
                _string += str(tile)
        return _string

    def setBatch(self, _batch):
        for row in self.tiles:
            for tile in row:
                tile.sprite.batch = _batch

    def loadMap(self, _file, _json=False):
        with open(_file, 'r') as inputFile:
            for y, line in enumerate(reversed(inputFile.readlines())):
                for x, tile in enumerate(line):
                    if tile == '#':
                        self.tiles[y][x] = Tile(tile, x, y,
                                                config.graphx['wall'])
                    elif tile == '.':
                        self.tiles[y][x] = Tile(tile, x, y,
                                                config.graphx['floor'], True)
                    elif tile == ']':
                        self.tiles[y][x] = Tile(tile, x, y,
                                                config.graphx['door_c'])
                    elif tile == ')':
                        self.tiles[y][x] = Tile(tile, x, y,
                                                config.graphx['door_o'], True)

    def save(self):
        _jsonObject = []

        for row in self.tiles:
            _jsonRow = []
            for tile in row:
                _jsonRow.append(tile.save())
            _jsonObject.append(_jsonRow)

        return {'tiles': _jsonObject, 'name': self.name}


class Selector():

    def __init__(self, _image, _rootMap=None):
        self.x = 0
        self.y = 0
        self.rootMap = _rootMap

        self.imagePath = _image
        self.image = pyglet.image.load(_image)

        self.sprite = pyglet.sprite.Sprite(self.image, self.x, self.y)

    def set_position(self, _x, _y):
        self.x = _x
        self.y = _y
        self.sprite.set_position(self.x*config.mapdata['tileSize'],
                                 self.y*config.mapdata['tileSize'])

        self.get_info()

    def move(self, symbol):
        if symbol == key.W and self.y < self.rootMap.lenY-1:
            self.set_position(self.x, self.y+1)
        elif symbol == key.S and self.y > 0:
            self.set_position(self.x, self.y-1)
        elif symbol == key.D and self.x < self.rootMap.lenX-1:
            self.set_position(self.x+1, self.y)
        elif symbol == key.A and self.x > 0:
            self.set_position(self.x-1, self.y)

    def get_info(self):
        print self.rootMap.tiles[self.y][self.x].save()

    def on_mouse_motion(self, x, y, dx, dy):
        if config.window['enableMouse']:
            self.set_position(
                x/config.mapdata['tileSize'],
                y/config.mapdata['tileSize'])
