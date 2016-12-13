from game_window import GameWindow
from game_data import GameData
from mapset import Map
from mapset import Selector
from entity import Player
from entity import Entity

from pyglet.window import key

import pyglet
import config

import json

if __name__ == '__main__':

    MGD = GameData(GameWindow(config.window['width'],
                              config.window['height']),
                   Map(config.mapdata['len_x'],
                       config.mapdata['len_y']),
                   Player('Engineer', 3, 4, '@',
                          config.graphx['priest']),
                   Selector(config.graphx['selector']),
                   entities=[Entity('Demon', 3, 3, 'D',
                                    config.graphx['demon'])])

    MGD.sync()
    MGD.initialize()

    @MGD._game_window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.Q:
            print 'GAME SAVED'
            with open(config.root['map_json']+'map.json', 'w+') as output_file:
                json.dump(MGD._root_map.save(), output_file, indent=2)

    pyglet.app.run()
