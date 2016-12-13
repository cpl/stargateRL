from game_window import GameWindow

import pyglet

import entity
import config
import mapset

if __name__ == '__main__':
    game = GameWindow()

    mymap = mapset.Map(config.mapdata['lenX'], config.mapdata['lenY'])
    mymap.loadMap('data/map_ascii/test1.map')

    mymap.setBatch(game.batch_map)

    player = entity.Player('Engineer', 3, 3,
                           mymap, '@', config.graphx['priest'])

    game.player = player

    demon = entity.Entity('Demon', 4, 3, mymap, 'D', config.graphx['demon'])

    player.sprite.batch = game.batch_entity
    demon.sprite.batch = game.batch_entity

    @game.event
    def on_mouse_press(x, y, button, modifiers):
        print mymap.tiles[y/32][x/32].save()

    pyglet.app.run()
