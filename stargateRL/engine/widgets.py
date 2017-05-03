"""Widget support."""

import pyglet


class Widget(object):
    """Standard widget with requierments."""

    def __init__(self):
        """Standard widget construct."""
        self._batch = pyglet.graphics.Batch()
        self._sprites = []

    def draw(self):
        """Draw the pyglet batch."""
        self._batch.draw()


class SelectionMenu(Widget):
    """A selection menu with options, widget."""

    def __init__(self, *options):
        """Construct a selection menu."""
        super(SelectionMenu, self).__init__()
