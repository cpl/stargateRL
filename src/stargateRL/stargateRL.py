#!/usr/bin/python -B

from manager import game_data
from manager import game_window
from manager import game_logic
from manager import game_ui 

import mapset
import entity

from utility import config
from utility import controls

import pyglet

from pyglet.window import key


class StarGateRL:
    ''' The main script, and story. '''
    def __init__(self, gm_window=None, gm_data=None, gm_logic=None):
        self.gm_window = gm_window
        self.gm_data = gm_data
        self.gm_logic = gm_logic

    def run(self):
        pyglet.app.run()


if __name__ == '__main__':

    # TODO: Add menu interface!!!

    my_map = mapset.Map()
    my_map.load('data/map_ascii/test1.map')

    my_player = entity.Player('Engineer', 1, 1, '@')
    entity1 = entity.Entity('Mike', 3, 3, 'M')
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
