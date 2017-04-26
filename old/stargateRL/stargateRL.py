#!/usr/bin/python -B
"""DOCSTRING."""

from manager import game_data, game_window, game_logic, game_ui
from utility import config, controls

import mapset
import entity
import pyglet

from pyglet.window import key


class StarGateRL:
    """The main script, and story."""

    def __init__(self, game_window=None, game_data=None, game_logic=None):
        """Init StarGateRL with the window, data and logic."""
        self.game_window = game_window
        self.game_data = game_data
        self.game_logic = game_logic

    def run(self):
        """Start the pyglet app."""
        pyglet.app.run()


if __name__ == '__main__':

    # TODO: Add menu interface
    # TODO: Replace ASCII maps with a map generator/editor

    # Create a (empty) map
    my_map = mapset.Map()

    # Load a map (from ASCII)
    my_map.load('data/map_ascii/test1.map')

    # Create Player at 1, 1
    my_player = entity.Player('Engineer', 1, 1, '@')
    # Create NPC at 3, 3
    entity1 = entity.Entity('Mike', 3, 3, 'M')
    # Create NPC at 3, 1
    entity2 = entity.Entity('Paul', 3, 1, 'P')

    gm_data = game_data.GameData(my_map, my_player, [entity1, entity2])
    gm_wind = game_window.GameWindow(config.window_width,
                                     config.window_height,
                                     resizable=True,
                                     caption=config.window_caption)

    gm_wind.load_graphx('tileset.png', config.gfx_tilesize)

    gm_wind.render_mapset(gm_data.root_map.get_all())
    gm_wind.render_player(gm_data.player)
    gm_wind.render_entities(gm_data.entities)

    gm_frame = game_ui.FrameUI(gm_wind, gm_wind.graphx.get_colored(16), 1, 1, 0, 0)
    gm_frame.render_frame(gm_wind)

    gm_logic = game_logic.GameLogic(gm_data, gm_wind)

    print key.MOD_FUNCTION

    @gm_wind.event
    def on_key_press(symbol, modifiers):

        print 'KeyPress(Symbol:{}, Modifiers:{})'.format(symbol, modifiers)

        if symbol in controls.LAYOUT.keys():
            if modifiers & key.MOD_ALT:
                gm_logic.move_selector(symbol, modifiers)
            else:
                gm_logic.move_player(symbol, modifiers)

        # SAVE LOAD DEBUG
        # if symbol == key.F:
        #     gm_data.save()
        # if symbol == key.Q:
        #     gm_data.load('c75501')
        #     gm_wind.render_mapset(gm_data.root_map.get_all())
        #     gm_wind.render_player(gm_data.player)

    @gm_wind.event
    def on_mouse_motion(x, y, dx, dy):
        gm_logic.mouse_selector(x, y)

    sg_game = StarGateRL(gm_wind, gm_data, gm_logic)
    sg_game.run()
