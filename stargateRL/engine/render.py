# -*- coding: utf-8 -*-
"""TODO: DOCSTRING."""

from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.window import Window


class GameWindow(Window):
    """Manager for the pyglet game window."""

    def __init__(self, width, height, tileset_gx, **kargs):
        """Init GameWindow as Pyglet Window."""
        super(GameWindow, self).__init__(width, height, **kargs)

        self.tileset = tileset_gx

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
                self.terrain_sprites.append(Sprite(self.tileset.get_tile(0, 0),
                                                   tile.position[0]*tile_size,
                                                   tile.position[1]*tile_size,
                                                   batch=self.batch_terrain))
        print len(self.terrain_sprites)

    def on_draw(self):
        """Call the pyglet window draws on each batch."""
        self.clear()

        # Order matters!
        self.batch_terrain.draw()  # Layer: Bottom
        self.batch_entities.draw()
        self.batch_player.draw()
        self.batch_effects.draw()
        self.batch_overlay.draw()  # Layer: Top
