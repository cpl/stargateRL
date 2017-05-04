"""Contains classes for all sorts of objects (TOTALLY ripped from Unity)."""

from enum import Enum
from stargateRL.utils import *


class SpriteObject(object):
	"""TODO: docstring."""
	
	def __init__(self, batch, group_order=None):
		pass


class Text(SpriteObject):

	def __init__(self, string, pos_x, pos_y,
		         foreground_color='white', background_color='transparent',
				 batch=None, group_order=None,):

		ts = GX_TILESETS['MAIN'].tile_size
        """Convert a string to a set of sprites, using the tileset letters."""
        self._string = string
        self._batch = batch
        self._group_order = group_order
        self.set_text(string, background_color, foreground_color, pos_x, pos_y)

    def set_color(self, foreground_color='white', background_color='transparent',
    			  letter_start=0, letter_end=-1):
    	for index, letter in enumerate(string[letter_start:letter_end]):
    		self._sprites[index].image = 
    				GX_TILESETS['MAIN'].get_colored(ord(letter), background_color,
    												foreground_color)

    def set_text(self, string, pos_x, pos_y,
    			 background_color='white', background_color='transparent',):
    	self._sprites = []
    	for index, letter in enumerate(string):
            self._sprites.append(
                pyglet.sprite.Sprite(GX_TILESETS['MAIN'].get_colored(ord(letter),
                                     background_color, foreground_color),
                                     (pos_x+index-(len(string)+1)/2)*ts, pos_y*ts,
                                     batch=self._batch))
