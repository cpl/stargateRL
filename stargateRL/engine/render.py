# -*- coding: utf-8 -*-
"""TODO: DOCSTRING."""

from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.window import Window


class GameWindow(Window):
    """Manager for the pyglet game window."""

    def __init__(self, width, height, **kargs):
        """Init GameWindow as Pyglet Window."""
        super(GameWindow, self).__init__(width, height, **kargs)
        self.widgets = []

    def add_widget(self, widget):
        """Append a Widget to be rendered."""
        self.widgets.append(widget)

    def on_draw(self):
        """Call Pyglet window draw method."""
        self.clear()
        for widget in self.widgets:
            widget.draw()

    def on_resize(self, width, height):
        """Update all widgets on screen resize."""
        # TODO: Change widget structure to support this


class LevelRender(object):
    """Render manager for the Level (map, player, critters, etc...)."""

    def __init__(self, width, height, tileset_gx, **kargs):
        """Construct the Level Renderer."""
        self.tileset = tileset_gx

        self.width = width
        self.height = height

        self.batch_terrain = Batch()   # Tiles
        self.batch_entities = Batch()  # NPCs
        self.batch_player = Batch()    # Player
        self.batch_effects = Batch()   # Effects
        self.batch_overlay = Batch()   # UI

    def render_map(self, map_logic):
        """Render the map."""
        self.terrain_sprites = []
        tile_size = self.tileset.size
        for row in map_logic.tiles:
            for tile in row:
                self.terrain_sprites.append(Sprite(self.tileset.get_tile(2, 1),
                                                   tile.position[0]*tile_size,
                                                   tile.position[1]*tile_size,
                                                   batch=self.batch_terrain))

    def on_draw(self):
        """Call the pyglet window draws on each batch."""
        # Always clear() before rendering this
        # Order matters!
        self.batch_terrain.draw()  # Layer: Bottom
        self.batch_entities.draw()
        self.batch_player.draw()
        self.batch_effects.draw()
        self.batch_overlay.draw()  # Layer: Top
