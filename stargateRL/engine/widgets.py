"""Widget support."""

from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet.window import key as win_key

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
        """Get called on window.event on_key_press."""
        return False


class FilledBoxWidget(Widget):
    """A widget that fills the screen with colored blocks."""

    def __init__(self, x, y, x_tiles, y_tiles,
                 foreground_color='white',
                 background_color='transparent', tile_id=177):
        """Construct a box at given position of given dimensions w color."""
        super(FilledBoxWidget, self).__init__()
        tile_size = GX_TILESETS['MAIN'].tile_size
        for x_tile in range(x_tiles):
            for y_tile in range(y_tiles):
                self._sprites.append(
                    Sprite(
                        GX_TILESETS['MAIN'].get_colored(tile_id,
                                                        foreground_color,
                                                        background_color),
                        (x + x_tile) * tile_size,
                        (y + y_tile) * tile_size,
                        batch=self._batch))


class BorderWidget(Widget):
    """A widget that draws a widget around the given area."""

    def __init__(self, x, y, x_tiles, y_tiles,
                 foreground_color='white',
                 background_color='transparent', **kargs):
        """Construct a border widget, can be used with other widgets."""
        super(BorderWidget, self).__init__()
        ts = GX_TILESETS['MAIN'].tile_size

        LT_CORNER = kargs.get('LT_CORNER', 178)
        LB_CORNER = kargs.get('LB_CORNER', 178)
        RB_CORNER = kargs.get('RB_CORNER', 178)
        RT_CORNER = kargs.get('RT_CORNER', 178)

        T_EDGE = kargs.get('T_EDGE', 35)
        B_EDGE = kargs.get('B_EDGE', 35)
        L_EDGE = kargs.get('L_EDGE', 35)
        R_EDGE = kargs.get('R_EDGE', 35)

        # Left, bottom, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(LB_CORNER,
                                                background_color,
                                                foreground_color),
                x * ts, y * ts, batch=self._batch))
        # Left, top, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(LT_CORNER,
                                                background_color,
                                                foreground_color),
                x * ts, (y + y_tiles - 1) * ts, batch=self._batch))
        # Right, bottom, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(RB_CORNER,
                                                background_color,
                                                foreground_color),
                (x + x_tiles - 1) * ts, y * ts, batch=self._batch))
        # Right, top, corner
        self._sprites.append(
            Sprite(
                GX_TILESETS['MAIN'].get_colored(RT_CORNER,
                                                background_color,
                                                foreground_color),
                (x + x_tiles - 1) * ts, (y + y_tiles - 1) * ts,
                batch=self._batch))

        # Bottom and top edges
        for x_tile in range(x_tiles):
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(T_EDGE,
                                                    background_color,
                                                    foreground_color),
                    (x + x_tile) * ts, (y + y_tiles - 1) * ts,
                    batch=self._batch))
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(B_EDGE,
                                                    background_color,
                                                    foreground_color),
                    (x + x_tile) * ts, y * ts, batch=self._batch))
        # Left and right edges
        for y_tile in range(y_tiles):
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(R_EDGE,
                                                    background_color,
                                                    foreground_color),
                    (x + x_tiles - 1) * ts, (y + y_tile) * ts,
                    batch=self._batch))
            self._sprites.append(
                Sprite(
                    GX_TILESETS['MAIN'].get_colored(L_EDGE,
                                                    background_color,
                                                    foreground_color),
                    x * ts, (y + y_tile) * ts,
                    batch=self._batch))

    def on_key_press(self, symbol, modifiers):
        """Get called on window.event on_key_press."""
        return True


class SelectionMenuWidget(BorderWidget):
    """A menu of options."""

    def __init__(self, tileset, x, y, x_tiles, y_tiles, border_color,
                 color_inactive, color_active, *options, **kargs):
        """Construct a selction menu."""
        super(SelectionMenuWidget, self).__init__(tileset, x, y,
                                                  x_tiles, y_tiles,
                                                  border_color, **kargs)
        self.active = 0
        self._text_sprites = []
        self.options = options
        self.tileset = tileset
        self.colors = (color_inactive, color_active)
        self.draw()

    def draw(self):
        """Prepare the menu for drawing."""
        tileset = self.tileset
        self._text_sprites = []

        x = self.x
        y = self.y
        x_tiles = self.x_tiles
        y_tiles = self.y_tiles

        for index, option in enumerate(self.options):
            if index == self.active:
                color = self.colors[1]
            else:
                color = self.colors[0]
            self._text_sprites.append(
                tileset.string_to_sprites(option,
                                          x + x_tiles / 2,
                                          y + y_tiles - 3 - index, color,
                                          self._batch))
        self._text_sprites[0][0].color = (0, 255, 0)
        super(SelectionMenuWidget, self).draw()

    def on_key_press(self, symbol, modifiers):
        """Get called on window.event on_key_press."""
        if symbol == win_key.UP:
            if self.active <= 0:
                self.active = len(self.options) - 1
            else:
                self.active -= 1
        elif symbol == win_key.DOWN:
            if self.active >= len(self.options) - 1:
                self.active = 0
            else:
                self.active += 1

        self.draw()
        return True
