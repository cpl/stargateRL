import pyglet
import config
import graphics


class Tile():
    def __init__(self, _x, _y, _graphic, _walkable):
        self.x = _x
        self.y = _y
        self.walkable = _walkable
        self.graphic = pyglet.image.load(_graphic)
        self.sprite = pyglet.sprite.Sprite(self.graphic,
                                           x=_x * config.TILE_SIZE,
                                           y=_y * config.TILE_SIZE)


class Map():
    def __init__(self, _len_x, _len_y):
        self.len_x = _len_x
        self.len_y = _len_y
        self.tiles = []

        for y in range(_len_y):
            _row = []
            for x in range(_len_x):
                if x == 0 or y == 0 or x == _len_x - 1 or y == _len_y - 1:
                    _row.append(Tile(x, y, graphics.WALL12, False))
                else:
                    _row.append(Tile(x, y, graphics.FLOOR12, True))
            self.tiles.append(_row)

    def __str__(self):
        _string = ''
        for row in self.tiles:
            for tile in row:
                _string += '. ' if tile.walkable else '# '
            _string += '\n'
        return _string
