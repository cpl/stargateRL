"""Graphical resource manager."""

import pyglet


class Color(object):
    """A representation of a color. RGBA."""

    def __init__(self, r, g, b, a):
        """Create a color."""
        self.color = (r, g, b, a)

    def __call__(self):
        """Return the color only."""
        color_string = ''
        for atr in self.color:
            color_string += chr(atr)
        return color_string


COLORS = {'black': Color(0, 0, 0, 255), 'white': Color(255, 255, 255, 255),
          'blue': Color(0, 0, 255, 255), 'red': Color(255, 0, 0, 255),
          'green': Color(0, 255, 0, 255), 'transparent': Color(0, 0, 0, 0),
          'border': Color(70, 76, 84, 255), 'gold': Color(245, 211, 115, 255)}


class GxTileset(object):
    """A image grid composing the Tileset resource."""

    def __init__(self, resource_path, tile_size):
        """Construct the tileset manager."""
        self.source_image = pyglet.resource.image(resource_path)

        self.tile_size = tile_size
        self.x_tiles_count = self.source_image.width / tile_size
        self.y_tiles_count = self.source_image.height / tile_size

        self.tileset_grid = pyglet.image.ImageGrid(self.source_image,
                                                   self.x_tiles_count,
                                                   self.y_tiles_count)

        # Normalize Pyglet's strange way of indexing ImageGrids
        self.tileset_grid = \
            [self.tileset_grid[x:x+tile_size]
             for x in range(0, len(self.tileset_grid), tile_size)]
        self.tileset_grid = self.tileset_grid[::-1]

    def get_by_id(self, tile_id):
        """Return a Image from the ImageGrid of the tileset."""
        row = self.tileset_grid[int(tile_id / self.tile_size)]
        return row[tile_id % self.tile_size]

    def get(self, row, column):
        """Return the Image from x, y inside ImageGrid."""
        return self.tileset_grid[row][column]

    def get_colored(self, tile_id, background, foreground):
        """Return a tile with the given colors."""
        if not isinstance(background, str) or not isinstance(foreground, str):
            print background, foreground
            print type(background), type(foreground)
            raise Exception('{} {} {}'.format(tile_id, background, foreground))
        tile_image = self.get_by_id(tile_id)
        image_data = tile_image.image_data.get_data('RGBA', tile_image.width*4)
        image_pxls = [image_data[p:p+4] for p in range(0, len(image_data), 4)]

        image_background = [p for p in range(len(image_pxls))
                            if image_pxls[p] == COLORS['black']()]
        image_foreground = [p for p in range(len(image_pxls))
                            if image_pxls[p] == COLORS['white']()]

        for pixel in image_background:
            image_pxls[pixel] = COLORS[background]()
        for pixel in image_foreground:
            image_pxls[pixel] = COLORS[foreground]()

        combined_pixels = b''
        for pixel in image_pxls:
            combined_pixels += pixel

        return pyglet.image.ImageData(tile_image.width, tile_image.height,
                                      'RGBA', combined_pixels)
