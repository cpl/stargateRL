"""Contains classes for all sorts of objects (TOTALLY ripped from Unity)."""

from pyglet.sprite import Sprite

from stargateRL.utils import GX_TILESETS
from stargateRL.engine.graphx import TileColor


class SpriteObject(object):
    """Spriteobject are objects made out of sprites."""

    def __init__(self, batch=None, group_order=None):
        """Construct sprite object."""
        self._batch = batch
        self._group_order = group_order


# TODO: Assign y_tiles to do something.
class SpriteText(SpriteObject):
    """This can be a single word, a line of text or even a block of text."""

    def __init__(self, string, x, y, x_tiles=None, y_tiles=None,
                 tile_color=TileColor(), batch=None, group_order=None):
        """Construct the text out of sprites."""
        super(SpriteText, self).__init__(batch, group_order)
        self._string = string

        # Create sprites from string
        ts = GX_TILESETS['MAIN'].tile_size
        self._sprites = []
        (x_mod, y_mod) = (0, 0)
        for letter in string:
            letter_ord = ord(letter)
            if letter_ord == 10:
                y_mod -= 1
                x_mod = 0
                continue
            elif x_tiles is not None and x_mod >= x_tiles:
                y_mod -= 1
                x_mod = 0

            x_mod += 1
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(letter_ord, tile_color),
                    (x+x_mod)*ts, (y+y_mod)*ts,
                    batch=self._batch, group=self._group_order))

    def set_color(self, tile_color=TileColor(), start=0, end=None):
        """Change the color of the text or part of the text."""
        for index, sprite in enumerate(self._sprites[start:end]):
            sprite.image =\
                GX_TILESETS['MAIN'].get_colored(ord(self._string[index+start]),
                                                tile_color)

    def set_batch(self, batch=None):
        """Set the batch of the sprites."""
        for sprite in self._sprites:
            sprite.batch = batch

    def set_group(self, group_order=None, start=0, end=None):
        """Set the group of the sprites."""
        for sprite in self._sprites[start:end]:
            sprite.group = group_order
