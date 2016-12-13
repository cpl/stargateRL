from game_window import GameWindow
from pyglet.window import key

import pyglet

import json
import entity
import config
import mapset

if __name__ == '__main__':
    game = GameWindow()

    mymap = mapset.Map(config.mapdata['len_x'], config.mapdata['len_y'])
    mymap.load_map('data/map_ascii/test1.map')

    mymap.set_batch(game._batch_map)

    game._selector._root_map = mymap

    player = entity.Player('Engineer', 3, 3,
                           mymap, '@', config.graphx['priest'])

    game._player = player

    @game.event
    def on_key_press(symbol, modifiers):
        if symbol == key.Q:
            with open(config.root['map_json']+'map.json', 'w+') as outputFile:
                json.dump(mymap.save(), outputFile, indent=2)

    demon = entity.Entity('Demon', 4, 3, mymap, 'D', config.graphx['demon'])

    player._sprite.batch = game._batch_entity
    demon._sprite.batch = game._batch_entity

    pyglet.app.run()
