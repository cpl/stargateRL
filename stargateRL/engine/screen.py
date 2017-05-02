"""Window/Screen manager."""

import pyglet


class GameWindow(pyglet.window.Window):
    """Window manager."""

    def __init__(self, width, height, graphx, **kargs):
        """Construct the window manager."""
        super(GameWindow, self).__init__(width, height, **kargs)

    def on_resize(self, width, height):
        """Pyglet on window size change."""
        super(GameWindow, self).on_resize(width, height)

    def on_draw(self):
        """Pyglet Window draw method."""
        self.clear()
