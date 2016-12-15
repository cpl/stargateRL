

class Tile:

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __repr__(self):
        return '''Tile(X:{:3},Y:{:3},Symbol:{})\
               '''.format(self.x, self.y, self.symbol)


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

        return 'Map(Size(X:{},Y:{}),Tiles({})) //Map'.format(self.size_x,
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
                            self.tiles[y][x] = Tile(x, y, char)

    def get_tile(self, x, y):
        return self.tiles[y][x]

    def set_tile(self, x, y, tile):
        self.tiles[y][x] = tile

    def display(self):
        for row in reversed(self.tiles):
            for tile in row:
                print tile.symbol,
            print


if __name__ == '__main__':
    my_tile = Tile(5, 4, '@')
    my_map = Map(1, 1, [my_tile, my_tile, my_tile, my_tile])
    my_map.load('data/map_ascii/test1.map')

    my_map.display()
