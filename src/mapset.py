import pyglet
import config
import graphx


class Tile():

    def __init__(self, _ascii, _x, _y, _image,
                 _isWalkable=False,
                 _hasEntity=False):

        self.ascii = _ascii
        self.x = _x
        self.y = _y
        self.isWalkable = _isWalkable
        self.hasEntity = _hasEntity

        self.image = pyglet.image.load(_image)
        self.sprite = pyglet.sprite.Sprite(self.image,
                                           _x * config.TILE_SIZE,
                                           _y * config.TILE_SIZE)

    def __str__(self):
        if self.hasEntity:
            return self.entity.ascii
        else:
            return self.ascii


class Map():

    def __init__(self, _lenX=0, _lenY=0):
        self.tiles = [['' for _ in range(_lenX)] for _ in range(_lenY)]
        self.lenX = _lenX
        self.lenY = _lenY

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

    def loadMap(self, _file):
        with open(_file, 'r') as inputFile:
            for y, line in enumerate(reversed(inputFile.readlines())):
                for x, tile in enumerate(line):
                    if tile == '#':
                        self.tiles[y][x] = Tile(tile, x, y, graphx.WALL)
                    elif tile == '.':
                        self.tiles[y][x] = Tile(tile, x, y, graphx.FLOOR, True)
                    elif tile == ']':
                        self.tiles[y][x] = Tile(tile, x, y, graphx.DOOR_C)
                    elif tile == ')':
                        self.tiles[y][x] = Tile(tile, x, y, graphx.DOOR_O, True)

    def saveMap(self, _file):
        with open(_file, 'w+') as outputFile:
            for row in self.tiles:
                for tile in row:
                    outputFile.write(tile.ascii)
                outputFile.write('\n')
