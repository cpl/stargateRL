"""A set of renderable widgets."""


from pyglet.graphics import Batch
from pyglet.sprite import Sprite

from graphx import GxTileset


class Widget(object):
    """Standard Widget class."""

    def draw(self):
        """Draw all sprites from the batch."""
        self.batch.draw()


class BorderWidget(Widget):
    """A simple border around the screen, mainly for testing."""

    def __init__(self, x, y, x_tiles, y_tiles, tile_size):
        """Construct a border."""
        self.sprites = []
        self.batch = Batch()
        self.tileset = GxTileset('borders.png', tile_size)

        # Add corners
        self.sprites.append(Sprite(self.tileset.get_tile(0, 0),
                                   x*tile_size,
                                   y*tile_size,
                                   batch=self.batch))
        self.sprites.append(Sprite(self.tileset.get_tile(2, 2),
                                   (x+x_tiles-1)*tile_size,
                                   (y+y_tiles-1)*tile_size,
                                   batch=self.batch))
        self.sprites.append(Sprite(self.tileset.get_tile(0, 2),
                                   x*tile_size,
                                   (y+y_tiles-1)*tile_size,
                                   batch=self.batch))
        self.sprites.append(Sprite(self.tileset.get_tile(2, 0),
                                   (x+x_tiles-1)*tile_size,
                                   y*tile_size,
                                   batch=self.batch))

        # Add the edges
        for x_tile in range(1, x_tiles-1):
            self.sprites.append(Sprite(self.tileset.get_tile(1, 0),
                                       (x+x_tile)*tile_size,
                                       y*tile_size,
                                       batch=self.batch))
            self.sprites.append(Sprite(self.tileset.get_tile(1, 2),
                                       (x+x_tile)*tile_size,
                                       (y+y_tiles-1)*tile_size,
                                       batch=self.batch))

        for y_tile in range(1, y_tiles-1):
            self.sprites.append(Sprite(self.tileset.get_tile(0, 1),
                                       x*tile_size,
                                       (y+y_tile)*tile_size,
                                       batch=self.batch))
            self.sprites.append(Sprite(self.tileset.get_tile(2, 1),
                                       (x+x_tiles-1)*tile_size,
                                       (y+y_tile)*tile_size,
                                       batch=self.batch))
