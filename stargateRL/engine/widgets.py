"""Widget support."""

from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.window import key as wkey

from stargateRL.engine.objects import SpriteText
from stargateRL.utils import GX_TILESETS


class Widget(object):
    """Standard widget with requierments."""

    def __init__(self):
        """Standard widget construct."""
        self._batch = Batch()
        self._sprites = []

    def draw(self):
        """Draw the pyglet batch."""
        self._batch.draw()

    def on_key_press(self, symbol, modifiers):
        """Returning false removes the widget from stack, true keeps it."""
        return False


class FilledBoxWidget(Widget):
    """A widget that fills the screen with colored blocks."""

    def __init__(self, x, y, x_tiles, y_tiles, tile_color, tile_id=177):
        """Construct a box at given position of given dimensions w color."""
        super(FilledBoxWidget, self).__init__()
        tile_size = GX_TILESETS['MAIN'].tile_size
        for x_tile in range(x_tiles):
            for y_tile in range(y_tiles):
                self._sprites.append(
                    Sprite(
                        GX_TILESETS['MAIN'].get_colored(tile_id, tile_color),
                        (x + x_tile) * tile_size,
                        (y + y_tile) * tile_size,
                        batch=self._batch))


class BorderWidget(Widget):
    """A widget that draws a widget around the given area."""

    def __init__(self, x, y, x_tiles, y_tiles, tile_color, **kargs):
        """Construct a border widget, can be used with other widgets."""
        super(BorderWidget, self).__init__()
        ts = GX_TILESETS['MAIN'].tile_size

        # TODO: better way of defining border tiles
        LT_CORNER = kargs.get('LT_CORNER', 178)
        LB_CORNER = kargs.get('LB_CORNER', 178)
        RB_CORNER = kargs.get('RB_CORNER', 178)
        RT_CORNER = kargs.get('RT_CORNER', 178)

        T_EDGE = kargs.get('T_EDGE', 35)
        B_EDGE = kargs.get('B_EDGE', 35)
        L_EDGE = kargs.get('L_EDGE', 35)
        R_EDGE = kargs.get('R_EDGE', 35)

        x_tiles = int(x_tiles)
        y_tiles = int(y_tiles)

        # Left, bottom, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(LB_CORNER, tile_color),
                x * ts, y * ts, batch=self._batch))
        # Left, top, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(LT_CORNER, tile_color),
                x * ts, (y + y_tiles - 1) * ts, batch=self._batch))
        # Right, bottom, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(RB_CORNER, tile_color),
                (x + x_tiles - 1) * ts, y * ts, batch=self._batch))
        # Right, top, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(RT_CORNER, tile_color),
                (x + x_tiles - 1) * ts, (y + y_tiles - 1) * ts,
                batch=self._batch))

        # Bottom and top edges
        for x_tile in range(x_tiles):
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(T_EDGE, tile_color),
                    (x + x_tile) * ts, (y + y_tiles - 1) * ts,
                    batch=self._batch))
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(B_EDGE, tile_color),
                    (x + x_tile) * ts, y * ts, batch=self._batch))
        # Left and right edges
        for y_tile in range(y_tiles):
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(R_EDGE, tile_color),
                    (x + x_tiles - 1) * ts, (y + y_tile) * ts,
                    batch=self._batch))
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(L_EDGE, tile_color),
                    x * ts, (y + y_tile) * ts,
                    batch=self._batch))

    def on_key_press(self, symbol, modifiers):
        """Get called on window.event on_key_press."""
        return True


class SelectionMenuWidget(BorderWidget):
    """A menu of options."""

    def __init__(self, x, y, x_tiles, y_tiles,
                 border_color, tile_color, active_color,
                 *options, **kargs):
        """Construct the selection menu."""
        super(SelectionMenuWidget, self).__init__(x, y, x_tiles, y_tiles,
                                                  border_color, **kargs)

        # Store options and active option
        self._options = options
        self._active = 0
        self._text_objects = []
        self._colors = (tile_color, active_color)

        op_lenght = len(options)
        for index, option in enumerate(options):
            word_length = len(option[0])
            self._text_objects.append(
                SpriteText(option[0], x+x_tiles/2-word_length/2,
                           y+y_tiles-index-op_lenght/2,
                           None, None, tile_color, self._batch))
        self._text_objects[self._active].set_color(self._colors[1])

    def on_key_press(self, symbol, modifiers):
        """Get called on window.event on_key_press."""
        if symbol == wkey.ENTER:
            getattr(self._options[self._active][1],
                    self._options[self._active][2])()
        elif symbol == wkey.UP:
            if self._active <= 0:
                self._text_objects[self._active].set_color(self._colors[0])
                self._active = len(self._options)-1
                self._text_objects[self._active].set_color(self._colors[1])
            else:
                self._text_objects[self._active].set_color(self._colors[0])
                self._active -= 1
                self._text_objects[self._active].set_color(self._colors[1])
        elif symbol == wkey.DOWN:
            if self._active >= len(self._options)-1:
                self._text_objects[self._active].set_color(self._colors[0])
                self._active = 0
                self._text_objects[self._active].set_color(self._colors[1])
            else:
                self._text_objects[self._active].set_color(self._colors[0])
                self._active += 1
                self._text_objects[self._active].set_color(self._colors[1])

        return True
