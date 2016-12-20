class Tile:

    def __init__(self, x, y, symbol, tags=[]):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.tags = tags

    def __repr__(self):
        return '''Tile(Position:({:3},{:3}),Symbol:{})\
               '''.format(self.x, self.y, self.symbol)

    def save(self):
        return {'x': self.x, 'y': self.y, 'symbol': self.symbol}


class Map:

    def __init__(self, size_x=0, size_y=0, tiles=[]):
        self.size_x = size_x
        self.size_y = size_y
        self.tiles = tiles

    def __repr__(self):
        _string = ''
        for col in self.tiles:
            for tile in col:
                _string += '\n' + str(tile)

        return 'Map(Size:({},{}),Tiles:({}))'.format(self.size_x,
                                                     self.size_y,
                                                     _string+'\n')

    def load(self, file_path, mode=0):
        with open(file_path, 'r') as file_map:
            if mode == 0:
                self.size_x = 0
                self.size_y = 0

                lines = file_map.readlines()
                for line in lines:
                    self.size_y += 1
                for char in line.strip('\n'):
                    self.size_x += 1
                self.tiles = [[None for _ in range(self.size_x)]
                              for _ in range(self.size_y)]

                for y, line in enumerate(reversed(lines)):
                    for x, char in enumerate(line):
                        if char != '\n':
                            self.set_tile(Tile(x, y, char))

    def save(self):
        return {'size_x': self.size_x, 'size_y': self.size_y,
                'tiles': [tile.save() for tile in self.get_all()]}

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def set_tile(self, tile):
        self.tiles[tile.y][tile.x] = tile

    def get_all(self):
        _tiles = []
        for row in self.tiles:
            for tile in row:
                _tiles.append(tile)
        return _tiles

    def display(self):
        for row in reversed(self.tiles):
            for tile in row:
                print tile.symbol,
            print
