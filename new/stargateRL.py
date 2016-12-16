import game_data
import game_window
import game_logic

import mapset
import entity

import pyglet


class StarGateRL:

    def __init__(self, gm_window=None, gm_data=None, gm_logic=None):
        self.gm_window = gm_window
        self.gm_data = gm_data
        self.gm_logic = gm_logic

    def run(self):
        pyglet.app.run()


if __name__ == '__main__':

    my_map = mapset.Map()
    my_map.load('data/map_ascii/test1.map')

    my_player = entity.Player('Engineer', 1, 1, '@')

    gm_data = game_data.GameData(my_map, my_player)
    gm_wind = game_window.GameWindow(200, 200, resizable=True)

    gm_wind.load_graphx('tileset.png', 16)
    gm_wind.load_mapset(my_map.get_all())

    sg_game = StarGateRL(gm_wind, gm_data)
    sg_game.run()
