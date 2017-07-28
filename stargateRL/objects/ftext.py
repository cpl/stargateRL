"""Standard font text objects. Using pyglet.text and pyglet.font"""

from pyglet.text import Label
from enum import Enum

from stargateRL.utils import TILE_SIZE


class TextConstants(Enum):
    """Constants used in text/font objects."""

    DEFAULT_FONT = ''

    ALIGN_LEFT = 'left'
    ALIGN_RIGHT = 'right'
    ALIGN_CENTER = 'center'

    ANCHOR_LEFT = 'left'
    ANCHOR_RIGHT = 'right'
    ANCHOR_CENTER = 'center'
    ANCHOR_BASELINE = 'baseline'


class Text(object):
    """Default class for any Text/Font based objects."""

    def __init__(self, text, color, position, dimensions,
                 batch=None, group=None):
        """Construct the text object."""
        # Unpack values
        x, y = position
        x_tiles, y_tiles = dimensions

        self._batch = batch
        self._group = group

        self._label = Label(text=text,
                            font_name=TextConstants.DEFAULT_FONT.value,
                            font_size=TILE_SIZE, bold=False, italic=False,
                            color=color.value.rgba(), x=x, y=y,
                            width=x_tiles*TILE_SIZE, height=y_tiles*TILE_SIZE,
                            anchor_x='left', anchor_y='baseline', align='left',
                            multiline=False, dpi=None,
                            batch=batch, group=group)

        # Only check once instead of checking every draw call
        # Dirty but it works
        if batch is None:
            self._batch = self._label

    def on_draw(self):
        """Draw the text."""
        # If batch is None on __init__, then _batch becomes a ref to _label
        self._batch.draw()


class ListText(object):
    """Default class for multi line/list text objects."""

    def __init__(self, strings, position, dimesions, colors, align, anchor):
        """"""
        # TODO:
        pass

    def change_color(self, id=None, string=None):
        """"""
        # TODO:
        pass


class SelectionListText(ListText):
    """"""

    def __init__(self, strings, position, dimensions, colors, align, anchor):
        """"""
        # TODO:
        pass