import pyglet
import config
import color


class GameData:
    ''' This class is all that has to be saved in order to generated a
    game save state/snapshot. The GameData class only stores the given data,
    and allows access to it (read/write) to the program. '''
    def __init__(self, root_map=None, player=None, entities=None):
        self.root_map = root_map
        self.player = player
        self.entities = entities

    def __repr__(self):
        _entities = ''
        for entity in self.entities:
            _entities += (str(entity)+'\n')
        return 'GameData(\n{},\n{},\n{})'.format(self.root_map,
                                                 self.player,
                                                 _entities)

    def save(self):
        ''' JSON save method. '''
        _entities = []
        for entity in self.entities:
            _entities.append(entity.save())

        return {'root_map': self.root_map.save(), 'player': self.player.save(),
                'entities': _entities}

    def load(self):
        pass


class GraphxData:
    ''' GraphxData calculates and loads the graphical resources at runtime,
    that will be used troughtout the run of the program. '''
    pyglet.resource.path = [config.dir_gfx]

    def __init__(self, path, size):
        self.tile_image = pyglet.resource.image(path)

        self.tile_set = pyglet.image.ImageGrid(self.tile_image,
                                               self.tile_image.width/size,
                                               self.tile_image.height/size)

        self.tile_set = reversed(tuple(zip(*[iter(self.tile_set)]*size)))
        self.tile_set = [tile for row in self.tile_set for tile in row]

    def get_tile(self, id):
        ''' This returns a tile image, with the coresponding id.'''
        return self.tile_set[id]

    def get_colored(self, id, primary=color.black, secondary=color.white):
        ''' This returns the tile image with the given colors. '''
        image_tile = self.tile_set[id]
        image_data = image_tile.image_data.get_data('RGBA', image_tile.width*4)
        image_pixels = [image_data[p:p+4] for p in range(0, len(image_data), 4)]

        image_background = [p for p in range(len(image_pixels))
                            if image_pixels[p] == color.black]
        image_foreground = [p for p in range(len(image_pixels))
                            if image_pixels[p] == color.white]

        for pixel in image_background:
            image_pixels[pixel] = primary
        for pixel in image_foreground:
            image_pixels[pixel] = secondary

        combined_pixels = b''
        for pixel in image_pixels:
            combined_pixels += pixel

        return pyglet.image.ImageData(image_tile.width, image_tile.height,
                                      'RGBA', combined_pixels)

if __name__ == '__main__':
    gfxd = GraphxData('tileset.png', config.gfx_tilesize)
    if gfxd.tile_image.__str__() == '<Texture 256x256>':
        assert True
