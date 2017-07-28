"""Widget support."""

from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.window import key as wkey

from stargateRL.utils import GX_TILESETS, TILE_SIZE
from stargateRL.objects.ftext import FontText


class Widget(object):
    """Standard widget with requierments."""

    def __init__(self, removable=True, key=wkey.ESCAPE):
        """Widget construct."""
        self._batch = Batch()
        self._sprites = []

        self._removable = removable
        self._key = key

    def draw(self):
        """Draw the pyglet batch."""
        self._batch.draw()

    def on_key_press(self, symbol, modifiers):
        """Return False removes the widget from stack, True keeps it."""
        if self._removable and self._key == symbol:
            return False
        else:
            return True


class FilledBoxWidget(Widget):
    """A widget that fills the screen with colored blocks."""

    def __init__(self, position, dimensions, removable,
                 tile_color, tile_id=177):
        """Construct a box at given position of given dimensions w color."""
        super(FilledBoxWidget, self).__init__(removable=removable)

        x, y = position
        x_tiles, y_tiles = dimensions

        for x_tile in range(x_tiles):
            for y_tile in range(y_tiles):
                self._sprites.append(
                    Sprite(
                        GX_TILESETS['MAIN'].get_colored(tile_id, tile_color),
                        (x + x_tile) * TILE_SIZE,
                        (y + y_tile) * TILE_SIZE,
                        batch=self._batch, usage='static'))


class BorderWidget(Widget):
    """A widget that draws a widget around the given area."""

    def __init__(self, position, dimensions, removable, tile_color, tiles):
        """Construct a border widget, can be used with other widgets."""
        super(BorderWidget, self).__init__(removable=removable)

        # LTC - LeftTopCorner, BE - BottomEdge
        LTC, LBC, RBC, RTC, TE, BE, LE, RE = tiles

        x, y = position
        x_tiles, y_tiles = dimensions

        # Left, bottom, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(LBC, tile_color),
                x * TILE_SIZE, y * TILE_SIZE,
                batch=self._batch, usage='static'))
        # Left, top, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(LTC, tile_color),
                x * TILE_SIZE, (y + y_tiles - 1) * TILE_SIZE,
                batch=self._batch, usage='static'))
        # Right, bottom, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(RBC, tile_color),
                (x + x_tiles - 1) * TILE_SIZE, y * TILE_SIZE,
                batch=self._batch, usage='static'))
        # Right, top, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(RTC, tile_color),
                (x + x_tiles - 1) * TILE_SIZE, (y + y_tiles - 1) * TILE_SIZE,
                batch=self._batch, usage='static'))

        # Bottom and top edges
        for x_tile in range(1, x_tiles-1):
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(TE, tile_color),
                    (x + x_tile) * TILE_SIZE, (y + y_tiles - 1) * TILE_SIZE,
                    batch=self._batch, usage='static'))
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(BE, tile_color),
                    (x + x_tile) * TILE_SIZE, y * TILE_SIZE,
                    batch=self._batch, usage='static'))

        # Left and right edges
        for y_tile in range(1, y_tiles-1):
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(RE, tile_color),
                    (x + x_tiles - 1) * TILE_SIZE, (y + y_tile) * TILE_SIZE,
                    batch=self._batch, usage='static'))
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(LE, tile_color),
                    x * TILE_SIZE, (y + y_tile) * TILE_SIZE,
                    batch=self._batch, usage='static'))


class SelectionMenuWidget(Widget):
    """A menu of options."""

    def __init__(self, position, dimensions, colors, options, **kargs):
        """Construct the selection menu."""
        super(SelectionMenuWidget, self).__init__(
            removable=kargs.get('removable'))

        border_color, default_color, active_color = colors
        x, y = position
        x_tiles, y_tiles = dimensions

        self._options = options
        self._index = 0
        self._colors = colors
        self._op_len = len(options)

        for index, option in enumerate(options):
            string = option[0]
            self._sprites.append(
                string
            )

    def on_key_press(self, symbol, modifiers):
        """Get called on window.event on_key_press."""
        if symbol == wkey.ENTER:
            _, command, args = self._options[self._index]
            command(*args)
        elif symbol == wkey.UP:
            self._index = (self._index - 1) % self._op_len
        elif symbol == wkey.DOWN:
            self._index = (self._index + 1) % self._op_len

        return True
