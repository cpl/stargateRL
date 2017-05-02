# -*- coding: utf-8 -*-
"""TODO: DOCSTRING."""

import pyglet
from os import path

pyglet.resource.path = [(path.abspath(path.join('bin')))]


class GxTileset(object):
    """Graphics set of all tiles."""

    def __init__(self, filepath, size):
        """Init graphx manager."""
        tile_image = pyglet.resource.image(filepath)

        self.size = size

        self.columns = tile_image.width/size
        self.rows = tile_image.height/size

        self.tile_set = pyglet.image.ImageGrid(tile_image,
                                               tile_image.width/size,
                                               tile_image.height/size)

        # Optional wizzardry
        # self.tile_set = reversed(tuple(zip(*[iter(self.tile_set)]*16)))
        # self.tile_set = [tile for row in self.tile_set for tile in row]

    def get_tile(self, x, y):
        """Get the tile of coordinates x, y."""
        if x >= self.columns or y >= self.rows:
            raise IndexError('Argument is out of bounds.')

        return self.tile_set[x+y*self.rows]
