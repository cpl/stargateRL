"""Widget support."""

from pyglet.sprite import Sprite
from pyglet.graphics import Batch, OrderedGroup
from pyglet.window import key as wkey

from stargateRL.utils import GX_TILESETS, TILE_SIZE
from stargateRL.objects.ftext import TextSelectionList, Text
from stargateRL.engine.colors import DefaultColors


class Widget(object):
    """Standard widget with requierments."""

    def __init__(self, removable=True, key=wkey.ESCAPE):
        """Widget construct."""
        self._batch = Batch()
        self._elements = []

        self._removable = removable
        self._key = key

    def draw(self):
        """Draw the pyglet batch."""
        self._batch.draw()

    def on_key_press(self, symbol, modifiers):
        """Return False removes the widget from stack, True keeps it."""
        return self._removable and self._key == symbol
        # if self._removable and self._key == symbol:
        #     return False
        # else:
        #     return True


class FilledBoxWidget(Widget):
    """A widget that fills the screen with colored blocks."""

    def __init__(self, position, dimensions, removable,
                 tile_color=DefaultColors.TILE, tile_id=177, group=None):
        """Construct a box at given position of given dimensions w color."""
        super(FilledBoxWidget, self).__init__(removable=removable)

        x, y = position
        x_tiles, y_tiles = dimensions

        tile = GX_TILESETS['MAIN'].get_colored(tile_id, tile_color)

        for x_tile in range(x_tiles):
            for y_tile in range(y_tiles):
                self._elements.append(
                    Sprite(
                        tile,
                        (x + x_tile) * TILE_SIZE,
                        (y + y_tile) * TILE_SIZE,
                        batch=self._batch, usage='static', group=group))


class BorderWidget(Widget):
    """A widget that draws a widget around the given area."""

    def __init__(self, position, dimensions, removable, tile_color, tiles,
                 batch=None, group=None):
        """Construct a border widget, can be used with other widgets."""
        super(BorderWidget, self).__init__(removable=removable)

        if batch is not None:
            self._batch = batch
        if group is not None:
            self._group = group

        # TODO: Possibly add a constant for `usage`
        # LTC - LeftTopCorner, BE - BottomEdge
        LTC, LBC, RBC, RTC, TE, BE, LE, RE = tiles

        x, y = position
        x_tiles, y_tiles = dimensions

        # Left, bottom, corner
        tile = GX_TILESETS['MAIN'].get_colored(LBC, tile_color)
        self._elements.append(
            Sprite(
                tile,
                x * TILE_SIZE, y * TILE_SIZE,
                batch=self._batch, usage='static'))
        # Left, top, corner
        tile = GX_TILESETS['MAIN'].get_colored(LTC, tile_color)
        self._elements.append(
            Sprite(
                tile,
                x * TILE_SIZE, (y + y_tiles - 1) * TILE_SIZE,
                batch=self._batch, usage='static'))
        # Right, bottom, corner
        tile = GX_TILESETS['MAIN'].get_colored(RBC, tile_color)
        self._elements.append(
            Sprite(
                tile,
                (x + x_tiles - 1) * TILE_SIZE, y * TILE_SIZE,
                batch=self._batch, usage='static'))
        # Right, top, corner
        tile = GX_TILESETS['MAIN'].get_colored(RTC, tile_color)
        self._elements.append(
            Sprite(
                tile,
                (x + x_tiles - 1) * TILE_SIZE, (y + y_tiles - 1) * TILE_SIZE,
                batch=self._batch, usage='static'))

        # Bottom and top edges
        top_tile = GX_TILESETS['MAIN'].get_colored(TE, tile_color)
        bot_tile = GX_TILESETS['MAIN'].get_colored(BE, tile_color)
        for x_tile in range(1, x_tiles - 1):
            self._elements.append(
                Sprite(
                    top_tile,
                    (x + x_tile) * TILE_SIZE, (y + y_tiles - 1) * TILE_SIZE,
                    batch=self._batch, usage='static'))
            self._elements.append(
                Sprite(
                    bot_tile,
                    (x + x_tile) * TILE_SIZE, y * TILE_SIZE,
                    batch=self._batch, usage='static'))

        # Left and right edges
        left_tile = GX_TILESETS['MAIN'].get_colored(RE, tile_color)
        right_tile = GX_TILESETS['MAIN'].get_colored(LE, tile_color)
        for y_tile in range(1, y_tiles - 1):
            self._elements.append(
                Sprite(
                    left_tile,
                    (x + x_tiles - 1) * TILE_SIZE, (y + y_tile) * TILE_SIZE,
                    batch=self._batch, usage='static'))
            self._elements.append(
                Sprite(
                    right_tile,
                    x * TILE_SIZE, (y + y_tile) * TILE_SIZE,
                    batch=self._batch, usage='static'))


class SelectionMenuWidget(FilledBoxWidget):
    """A menu of options."""

    def __init__(self, position, dimensions, colors, options, **kargs):
        """Construct the selection menu."""
        # Prepare groups
        group_background = OrderedGroup(0)
        group_foreground = OrderedGroup(1)

        border_color, default_color, active_color, selected_color, tile_color = colors

        # Create a FilledBox background
        super(SelectionMenuWidget, self).__init__(position, dimensions,
                                                  kargs.get('removable', True),
                                                  tile_id=0,
                                                  tile_color=tile_color,
                                                  group=group_background)

        # Create a Border around the FilledBox
        self._border = BorderWidget(position, dimensions, False, border_color,
                                    tiles=(178, 178, 178, 178, 35, 35, 35, 35),
                                    batch=self._batch, group=group_foreground)

        self._options = options
        self._index = 0
        self._op_len = len(options)

        _strings = []
        for option in options:
            _strings.append(option[0])

        self._tx_list = TextSelectionList(_strings, position, dimensions,
                                          colors=(default_color,
                                                  active_color,
                                                  selected_color),
                                          batch=self._batch,
                                          group=group_foreground)
        self._elements.append(self._tx_list)

    def on_key_press(self, symbol, modifiers):
        """Get called on window.event on_key_press."""
        if symbol == wkey.ENTER:
            self._tx_list.select()
            _, command, args = self._options[self._index]
            command(*args)
        elif symbol == wkey.UP:
            self._tx_list.increment()
            self._index = (self._index - 1) % self._op_len
        elif symbol == wkey.DOWN:
            self._tx_list.decrement()
            self._index = (self._index + 1) % self._op_len

        return True


class TextWidget(Widget):
    """Simple widget to draw text."""

    def __init__(self, string, position, color, align):
        """Construct the simple text widget."""
        super(TextWidget, self).__init__(removable=True)

        self._elements.append(Text(string, color, position,
                                   align, batch=self._batch))
