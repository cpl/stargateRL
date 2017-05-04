"""Widget support."""

from pyglet.sprite import Sprite
from pyglet.graphics import Batch

import graphx


class Widget(object):
    """Standard widget with requierments."""

    def __init__(self, tileset):
        """Standard widget construct."""
        self._batch = Batch()
        self._sprites = []
        self._tileset = tileset

    def draw(self):
        """Draw the pyglet batch."""
        self._batch.draw()


class FilledBoxWidget(Widget):
    """A widget that fills the screen with colored blocks."""

    def __init__(self, tileset, x, y, x_tiles, y_tiles, color):
        """Construct a box at given position of given dimensions w color."""
        super(FilledBoxWidget, self).__init__(tileset)
        tile_size = tileset.tile_size
        for x_tile in range(x_tiles):
            for y_tile in range(y_tiles):
                self._sprites.append(
                    Sprite(
                        tileset.get_colored(
                            65,
                            graphx.COLORS['transparent'],
                            graphx.COLORS[color]),
                        (x+x_tile)*tile_size,
                        (y+y_tile)*tile_size,
                        batch=self._batch))


class BorderWidget(Widget):
    """A widget that draws a widget around the given area."""

    def __init__(self, tileset, x, y, x_tiles, y_tiles, color, **kargs):
        """Construct a border widget, can be used with other widgets."""
        super(BorderWidget, self).__init__(tileset)
        tile_size = tileset.tile_size

        LB_CORNER = kargs.get('LB_CORNER', 66)
        LT_CORNER = kargs.get('LT_CORNER', 66)
        RB_CORNER = kargs.get('RB_CORNER', 66)
        RT_CORNER = kargs.get('RT_CORNER', 66)

        T_EDGE = kargs.get('RT_CORNER', 211)
        B_EDGE = kargs.get('RT_CORNER', 211)
        L_EDGE = kargs.get('RT_CORNER', 211)
        R_EDGE = kargs.get('RT_CORNER', 211)

        # Left, bottom, corner
        self._sprites.append(
            Sprite(
                tileset.get_colored(
                    LB_CORNER,
                    graphx.COLORS['transparent'],
                    graphx.COLORS[color]),
                x*tile_size,
                y*tile_size,
                batch=self._batch))
        # Left, top, corner
        self._sprites.append(
            Sprite(
                tileset.get_colored(
                    LT_CORNER,
                    graphx.COLORS['transparent'],
                    graphx.COLORS[color]),
                x*tile_size,
                (y_tiles-1)*tile_size,
                batch=self._batch))
        # Right, bottom, corner
        self._sprites.append(
            Sprite(
                tileset.get_colored(
                    RB_CORNER,
                    graphx.COLORS['transparent'],
                    graphx.COLORS[color]),
                (x_tiles-1)*tile_size,
                y*tile_size,
                batch=self._batch))
        # Right, top, corner
        self._sprites.append(
            Sprite(
                tileset.get_colored(
                    RT_CORNER,
                    graphx.COLORS['transparent'],
                    graphx.COLORS[color]),
                (x_tiles-1)*tile_size,
                (y_tiles-1)*tile_size,
                batch=self._batch))

        # Bottom and top edges
        for x_tile in range(x_tiles):
            self._sprites.append(
                Sprite(
                    tileset.get_colored(
                        T_EDGE,
                        graphx.COLORS['transparent'],
                        graphx.COLORS[color]),
                    x_tile*tile_size,
                    (y_tiles-1)*tile_size,
                    batch=self._batch))
            self._sprites.append(
                Sprite(
                    tileset.get_colored(
                        B_EDGE,
                        graphx.COLORS['transparent'],
                        graphx.COLORS[color]),
                    x_tile*tile_size,
                    y*tile_size,
                    batch=self._batch))
        # Left and right edges
        for y_tile in range(y_tiles):
            self._sprites.append(
                Sprite(
                    tileset.get_colored(
                        R_EDGE,
                        graphx.COLORS['transparent'],
                        graphx.COLORS[color]),
                    (x_tiles-1)*tile_size,
                    y_tile*tile_size,
                    batch=self._batch))
            self._sprites.append(
                Sprite(
                    tileset.get_colored(
                        L_EDGE,
                        graphx.COLORS['transparent'],
                        graphx.COLORS[color]),
                    x*tile_size,
                    y_tile*tile_size,
                    batch=self._batch))
