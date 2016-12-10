import pyglet
import config
import graphics


class Tile():
    def __init__(self, _x, _y, _graphic, _walkable, _ascii):
        self.x = _x
        self.y = _y
        self.walkable = _walkable
        self.graphic = pyglet.image.load(_graphic)
        self.sprite = pyglet.sprite.Sprite(self.graphic,
                                           x=_x * config.TILE_SIZE,
                                           y=_y * config.TILE_SIZE)
        self.ascii = _ascii

    def set_x(self, _x):
        self.x = _x

    def set_y(self, _y):
        self.y = _y


class Map():
    def __init__(self):
        self.tiles = []

    def __str__(self):
        _string = ''
        for row in self.tiles:
            for tile in row:
                _string += tile.ascii + ' '
            _string += '\n'
        return _string

    def make_empty(self, _len_x, _len_y):
        for y in range(_len_y):
            _row = []
            for x in range(_len_x):
                if x == 0 or y == 0 or x == _len_x - 1 or y == _len_y - 1:
                    _row.append(Tile(x, y, graphics.WALL12, False, '#'))
                else:
                    _row.append(Tile(x, y, graphics.FLOOR12, True, '.'))
            self.tiles.append(_row)

    def save(self, file):
        with open(file, 'w') as output_map:
            output_map.write(str(len(self.tiles[0])) + ' ' +
                             str(len(self.tiles)) + '\n')
            for row in self.tiles:
                for tile in row:
                    output_map.write(tile.ascii)
                output_map.write('\n')

    def update(self, batch):
        for row in self.tiles:
            for tile in row:
                tile.sprite.batch = batch

TILE_ASCII = {'#': Tile(0, 0, graphics.WALL12, False, '#'),
              '.': Tile(0, 0, graphics.FLOOR12, True, '.'),
              ']': Tile(0, 0, graphics.DOOR_C, False, ']')}


def load(file):
    _map = Map()
    with open(file, 'r') as input_map:
        lengths = input_map.readline().split(' ')
        _map.len_x = lengths[0]
        _map.len_y = lengths[1]
        for y, line in enumerate(input_map.readlines()):
            _map.tiles.append([])
            for x, tile in enumerate(line):
                if not tile == '\n':
                    loaded_tile = TILE_ASCII[tile]
                    print loaded_tile.x,
                    loaded_tile.set_x(x)
                    print loaded_tile.x
                    loaded_tile.set_y(y)
                    _map.tiles[y].append(loaded_tile)
    return _map
