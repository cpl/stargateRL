import pyglet
import config
import color


class GameData:

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
        _entities = []
        for entity in self.entities:
            _entities.append(entity.save())

        return {'root_map': self.root_map.save(), 'player': self.player.save(),
                'entities': _entities}

    def load(self):
        pass


class GraphxData:

    def __init__(self, path, row, col):
        self.tile_image = pyglet.resource.image(path)

        self.tile_set = pyglet.image.ImageGrid(self.tile_image, row, col)
        self.tile_set = reversed(tuple(zip(*[iter(self.tile_set)]*16)))
        self.tile_set = [tile for row in self.tile_set for tile in row]

    def get_tile(self, id):
        return self.tile_set[id]

    def get_colored(self, id, primary=color.black, secondary=color.white):

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
