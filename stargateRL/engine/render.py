# -*- coding: utf-8 -*-
"""TODO: DOCSTRING."""

import pyglet
import graphx


class GameWindow(pyglet.window.Window):
    """Manager for the pyglet game window."""

    def __init__(self, width, height, **kargs):
        """Init GameWindow as Pyglet Window."""
        super(GameWindow, self).__init__(width, height, **kargs)

        self.graphx_manager = None

        self.batch_terrain = pyglet.graphics.Batch()   # Tiles
        self.batch_entities = pyglet.graphics.Batch()  # NPCs
        self.batch_player = pyglet.graphics.Batch()    # Player
        self.batch_effects = pyglet.graphics.Batch()   # Effects
        self.batch_overlay = pyglet.graphics.Batch()   # UI

    def load_tileset(self, graphx_manager):
        """Load tileset from file, with given size."""
        if not isinstance(graphx_manager, graphx.GraphX):
            raise TypeError('''Argument must be of type GraphX, found {}\
                            '''.format(type(graphx_manager)))
        self.graphx_manager = graphx_manager

    def on_draw(self):
        """Call the pyglet window draws on each batch."""
        self.clear()

        # Order matters!
        self.batch_terrain.draw()  # Layer: Bottom
        self.batch_entities.draw()
        self.batch_player.draw()
        self.batch_effects.draw()
        self.batch_overlay.draw()  # Layer: Top
