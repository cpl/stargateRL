from game_window import GameWindow
from pyglet.window import key

import pyglet

import json
import entity
import config
import mapset

if __name__ == '__main__':
    game = GameWindow()

    mymap = mapset.Map(config.mapdata['lenX'], config.mapdata['lenY'])
    mymap.loadMap('data/map_ascii/test1.map')

    mymap.setBatch(game.batch_map)

    game.selector.rootMap = mymap

    player = entity.Player('Engineer', 3, 3,
                           mymap, '@', config.graphx['priest'])

    game.player = player

    @game.event
    def on_key_press(symbol, modifiers):
        if symbol == key.Q:
            with open(config.root['map_json']+'map.json', 'w+') as outputFile:
                json.dump(mymap.save(), outputFile, indent=2)

    demon = entity.Entity('Demon', 4, 3, mymap, 'D', config.graphx['demon'])

    player.sprite.batch = game.batch_entity
    demon.sprite.batch = game.batch_entity

    pyglet.app.run()
