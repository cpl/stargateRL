#!/usr/bin/python

import game_data
import game_window
import game_logic

import mapset
import entity
import config

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

    gm_data = game_data.GameData(my_map, my_player)
    gm_wind = game_window.GameWindow(config.window_width,
                                     config.window_height,
                                     resizable=True,
                                     caption=config.window_caption)

    gm_wind.load_graphx('tileset.png', config.gfx_tilesize)

    gm_wind.render_mapset(my_map.get_all())
    gm_wind.render_player(gm_data.player)

    gm_logic = game_logic.GameLogic(gm_data, gm_wind)

    @gm_wind.event
    def on_key_press(symbol, modifiers):
        if symbol in [key.UP, key.DOWN, key.LEFT, key.RIGHT]:
            gm_logic.move_player(symbol, modifiers)

    sg_game = StarGateRL(gm_wind, gm_data, gm_logic)
    sg_game.run()
