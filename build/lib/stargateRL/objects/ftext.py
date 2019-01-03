"""Standard font text objects. Using pyglet.text and pyglet.font."""

from pyglet.text import Label

from stargateRL.utils import TILE_SIZE, DEFAULT_FONT


class Text(object):
    """Default class for any Text/Font based objects."""

    def __init__(self, text, color, position, dimensions, align='left',
                 anchor=('left', 'baseline'), fsdt=0, batch=None, group=None):
        """Construct the text object."""
        # Unpack values
        x, y = position
        x_tiles, y_tiles = dimensions
        anchor_x, anchor_y = anchor

        self._batch = batch
        self._group = group

        # TODO: Simplify number of local variables and this entire mammoth!
        self._label = Label(text=text,
                            font_name=DEFAULT_FONT,
                            font_size=TILE_SIZE + fsdt,
                            bold=False, italic=False,
                            color=color.value.rgba,
                            x=x * TILE_SIZE, y=y * TILE_SIZE,
                            width=x_tiles * TILE_SIZE,
                            height=y_tiles * TILE_SIZE,
                            anchor_x=anchor_x, anchor_y=anchor_y,
                            align=align, multiline=False, dpi=None,
                            batch=batch, group=group)

        # Only check once instead of checking every draw call
        # Dirty? but it works
        if batch is None:
            self._batch = self._label

    def set_color(self, color):
        """Change the color of the Text."""
        self._label.color = color.value.rgba

    def on_draw(self):
        """Draw the text."""
        # If batch is None on __init__, then _batch becomes a ref to _label
        self._batch.draw()


class TextSelectionList(object):
    """Default class for multi line/list text objects."""

    def __init__(self, strings, position, dimensions, colors,
                 align='center', anchor=('center', 'baseline'),
                 batch=None, group=None):
        """Create the labels and list."""
        x, y = position
        x_tiles, y_tiles = dimensions
        default, active, selected = colors

        self._color_active = active
        self._color_default = default
        self._color_selected = selected

        self._labels = []
        self._active = 0

        for index, string in enumerate(strings):
            self._labels.append(
                Text(string, default,
                     position=(x_tiles / 2 + x,
                               y_tiles / 2 + y_tiles / 4 + y - index),
                     dimensions=(x_tiles, TILE_SIZE),
                     align=align, anchor=anchor,
                     fsdt=0, batch=batch, group=group))

        self._activate()

    def _clear(self):
        """Clear previous selections."""
        self._labels[(self._active - 1) % len(self._labels)].set_color(
            self._color_default)
        self._labels[(self._active + 1) % len(self._labels)].set_color(
            self._color_default)

    def _activate(self):
        """Change the color of the active label to active."""
        self._clear()
        self._labels[self._active].set_color(self._color_active)

    def _select(self):
        """Change the color of the active label to selected."""
        self._clear()
        self._labels[self._active].set_color(self._color_selected)

    def increment(self):
        """Do things when the menu incremets."""
        self._active = (self._active - 1) % len(self._labels)
        self._activate()

    def decrement(self):
        """Do things when the menu decrements."""
        self._active = (self._active + 1) % len(self._labels)
        self._activate()

    def select(self):
        """Do thing when the menu option is selected."""
        self._select()
