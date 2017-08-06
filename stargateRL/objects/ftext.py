"""Standard font text objects. Using pyglet.text and pyglet.font."""

from pyglet.text import Label

from stargateRL.utils import TILE_SIZE, DEFAULT_FONT


class Text(object):
    """Default class for any Text/Font based objects."""

    def __init__(self, text, color, position, align='left',
                 anchor=('left', 'baseline'), fsdt=0, batch=None, group=None):
        """Construct the text object."""
        # Unpack values
        x, y = position
        anchor_x, anchor_y = anchor

        self._batch = batch
        self._group = group

        self._label = Label(text=text,
                            font_name=DEFAULT_FONT,
                            font_size=TILE_SIZE+fsdt, bold=False, italic=False,
                            color=color.value.rgba(),
                            x=x*TILE_SIZE, y=y*TILE_SIZE,
                            anchor_x=anchor_x, anchor_y=anchor_y,
                            align=align, multiline=False, dpi=None,
                            batch=batch, group=group)

        # Only check once instead of checking every draw call
        # Dirty? but it works
        if batch is None:
            self._batch = self._label

    def on_draw(self):
        """Draw the text."""
        # If batch is None on __init__, then _batch becomes a ref to _label
        self._batch.draw()


class TextSelectionList(object):
    """Default class for multi line/list text objects."""

    def __init__(self, strings, position, dimesions, colors, align, anchor):
        """"""
        # TODO:
        pass
