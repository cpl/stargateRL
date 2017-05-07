"""Graphical resource manager."""

import pyglet


class Color(object):
    """A representation of a color. RGBA."""

    def __init__(self, r, g, b, a):
        """Create a color."""
        self._color = (r, g, b, a)

    def __call__(self):
        """Return the color only."""
        return bytes(bytearray(self._color))


class TileColor(object):
    """A class holding two colors (foreground and background)."""

    def __init__(self, foreground_color='white',
                 background_color='transparent'):
        """Construct the color for the tile."""
        self._foreground_color = foreground_color
        self._background_color = background_color

    def __call__(self):
        """Return the names of the colors."""
        return (self._foreground_color, self._background_color)

    def set_background(self, color):
        """Set the background color."""
        self._background_color = color

    def set_foreground(self, color):
        """Set the foreground color."""
        self._foreground_color = color

    def get_background(self):
        """Return the background color."""
        return self._background_color

    def get_foreground(self):
        """Return the foreground color."""
        return self._foreground_color


COLORS = {'black': Color(0, 0, 0, 255), 'white': Color(255, 255, 255, 255),
          'blue': Color(0, 0, 255, 255), 'red': Color(255, 0, 0, 255),
          'green': Color(0, 255, 0, 255), 'transparent': Color(0, 0, 0, 0),
          'border': Color(70, 76, 84, 255), 'gold': Color(245, 211, 115, 255)}


class GxTileset(object):
    """A image grid composing the Tileset resource."""

    def __init__(self, resource_path, tile_size):
        """Construct the tileset manager."""
        self.source_image = pyglet.resource.image(resource_path)

        self.tile_size = int(tile_size)
        self.x_tiles_count = int(self.source_image.width / tile_size)
        self.y_tiles_count = int(self.source_image.height / tile_size)

        self.tileset_grid = pyglet.image.ImageGrid(self.source_image,
                                                   self.x_tiles_count,
                                                   self.y_tiles_count)

        # Normalize Pyglet's strange way of indexing ImageGrids
        self.tileset_grid = \
            [self.tileset_grid[x:x+self.x_tiles_count]
             for x in range(0, len(self.tileset_grid), self.y_tiles_count)]
        self.tileset_grid = self.tileset_grid[::-1]

    def get_by_id(self, tile_id):
        """Return a Image from the ImageGrid of the tileset."""
        row = self.tileset_grid[int(tile_id / self.x_tiles_count)]
        return row[tile_id % self.y_tiles_count]

    def get(self, row, column):
        """Return the Image from x, y inside ImageGrid."""
        return self.tileset_grid[row][column]

    def get_colored(self, tile_id, tile_color):
        """Return a tile with the given colors."""
        tile_image = self.get_by_id(tile_id)
        image_data = tile_image.image_data.get_data('RGBA', tile_image.width*4)
        image_pxls = [image_data[p:p+4] for p in range(0, len(image_data), 4)]

        image_background = [p for p in range(len(image_pxls))
                            if image_pxls[p] == COLORS['black']()]
        image_foreground = [p for p in range(len(image_pxls))
                            if image_pxls[p] == COLORS['white']()]

        for pixel in image_background:
            image_pxls[pixel] = COLORS[tile_color.get_background()]()
        for pixel in image_foreground:
            image_pxls[pixel] = COLORS[tile_color.get_foreground()]()

        combined_pixels = b''
        for pixel in image_pxls:
            combined_pixels += pixel

        return pyglet.image.ImageData(tile_image.width, tile_image.height,
                                      'RGBA', combined_pixels)
