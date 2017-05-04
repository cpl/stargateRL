"""Window/Screen manager."""

import pyglet


class GameWindow(pyglet.window.Window):
    """Window manager."""

    def __init__(self, width, height, **kargs):
        """Construct the window manager."""
        super(GameWindow, self).__init__(width, height, **kargs)
        self._widgets = []
        self._testing_batch = pyglet.graphics.Batch()
        self.fps = pyglet.clock.ClockDisplay()

    def push_widget(self, widget):
        """Put a widget on top of the widget stack."""
        self._widgets.append(widget)

    def pop_widget(self):
        """Pop the widget on top of the widget stack."""
        if self._widgets:
            self._widgets.pop()

    # Window events

    def on_resize(self, width, height):
        """Pyglet on window size change."""
        super(GameWindow, self).on_resize(width, height)

    def on_draw(self):
        """Pyglet Window draw method."""
        self.clear()
        self._testing_batch.draw()
        for widget in self._widgets:
            widget.draw()
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        """Whenever a key is pressed (there is also a release method)."""
        if self._widgets:
            if not self._widgets[-1].on_key_press(symbol, modifiers):
                self.pop_widget()
        else:
            super(GameWindow, self).on_key_press(symbol, modifiers)
