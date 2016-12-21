import pyglet
import config
import color
import hashlib
import os
import cPickle as pickel


class GameData:
    ''' This class is all that has to be saved in order to generated a
    game save state/snapshot. The GameData class only stores the given data,
    and allows access to it (read/write) to the program. '''
    def __init__(self, root_map=None, player=None, entities=[]):
        self.root_map = root_map

        self.player = player
        self.root_map.get_tile(player.x,
                               player.y).entity = self.player

        self.entities = entities
        for entity in entities:
            self.root_map.get_tile(entity.x, entity.y).entity = entity

    def __repr__(self):
        _entities = ''
        for entity in self.entities:
            _entities += (str(entity)+'\n')
        return 'GameData(\n{},\n{},\n{})'.format(self.root_map,
                                                 self.player,
                                                 _entities)

    def save(self):
        selfhash = hashlib.sha256(os.urandom(32)).hexdigest()
        with open(os.path.join(config.dir_saves,
                               selfhash[:6]), 'w+') as save_file:
            pickel.dump(self, save_file)

    def load(self, save_file):
        with open(os.path.join(config.dir_saves, save_file), 'r') as save_file:
            loaded_game_data = pickel.load(save_file)

            self.root_map = loaded_game_data.root_map
            self.player = loaded_game_data.player
            self.entities = loaded_game_data.entities

            del(loaded_game_data)


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

    def get_colored(self, id,
                    primary=color.BLACK.get_color(),
                    secondary=color.WHITE.get_color()):
        ''' This returns the tile image with the given colors. '''
        image_tile = self.tile_set[id]
        image_data = image_tile.image_data.get_data('RGBA', image_tile.width*4)
        image_pixels = [image_data[p:p+4] for p in range(0, len(image_data), 4)]

        image_background = [p for p in range(len(image_pixels))
                            if image_pixels[p] == color.BLACK.get_color()]
        image_foreground = [p for p in range(len(image_pixels))
                            if image_pixels[p] == color.WHITE.get_color()]

        for pixel in image_background:
            image_pixels[pixel] = primary
        for pixel in image_foreground:
            image_pixels[pixel] = secondary

        combined_pixels = b''
        for pixel in image_pixels:
            combined_pixels += pixel

        return pyglet.image.ImageData(image_tile.width, image_tile.height,
                                      'RGBA', combined_pixels)


class GraphxSelector:

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(image, x, y)

    def move(self, direction):
        self.x += direction[0]
        self.y += direction[1]

    def get_info(self, gm_data):
        print gm_data.root_map.get_tile(self.x, self.y)

        # if gm_data.player.get_position() == (self.x, self.y):
        #     print gm_data.player

    def mouse(self, x, y):
        if self.x != x/config.gfx_tilesize:
            self.x = x/config.gfx_tilesize
        if self.y != y/config.gfx_tilesize:
            self.y = y/config.gfx_tilesize
