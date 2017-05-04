"""Contains classes for all sorts of objects (TOTALLY ripped from Unity)."""

import pyglet
from stargateRL.utils import GX_TILESETS


class SpriteObject(object):
    """TODO: Docstring."""

    def __init__(self, batch=None, group_order=None):
        """Spriteobject are objects made out of sprites."""
        pass


class SpriteText(SpriteObject):
    """TODO: Docstring."""

    def __init__(self, string, pos_x, pos_y,
                 foreground_color='white', background_color='transparent',
                 batch=None, group_order=None):
        """Convert a string to a set of sprites, using the tileset letters."""
        self._string = string
        self._batch = batch
        self._group_order = group_order
        self.set_text(string, pos_x, pos_y, foreground_color, background_color)

    def set_text(self, string, pos_x, pos_y, foreground_color='transparent',
                 background_color='white'):
        """Change the text of the current SpriteObject."""
        ts = GX_TILESETS['MAIN'].tile_size
        self._sprites = []
        for index, letter in enumerate(string):
            self._sprites.append(
                pyglet.sprite.Sprite(
                    GX_TILESETS['MAIN'].get_colored(ord(letter),
                                                    background_color,
                                                    foreground_color),
                    (pos_x+index-(len(string)+1)/2)*ts,
                    pos_y * ts, batch=self._batch))

    def set_color(self, foreground_color='white',
                  background_color='transparent',
                  letter_start=0, letter_end=-1):
        """Change the color of the text or some letters only."""
        for index, letter in enumerate(self.string[letter_start:letter_end]):
            self._sprites[index].image = GX_TILESETS['MAIN'].get_colored(ord(letter), background_color, foreground_color)
