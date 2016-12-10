import pyglet
import entity
import mapset
import config
import graphics

from pyglet.window import key

myMap = mapset.Map(config.MAP_SIZE_X, config.MAP_SIZE_Y)

player = entity.Entity('Engineer', 1, 1, graphics.PRIEST)

window = pyglet.window.Window(config.MAP_SIZE_X * config.TILE_SIZE,
                              config.MAP_SIZE_Y * config.TILE_SIZE)

batch = pyglet.graphics.Batch()

for row in myMap.tiles:
    for tile in row:
        tile.sprite.batch = batch


@window.event
def on_key_press(symbol, modifiers):
        if symbol == key.UP:
            if myMap.tiles[player.position_y+1][player.position_x].walkable:
                player.add_position(0, 1)
        elif symbol == key.DOWN:
            if myMap.tiles[player.position_y-1][player.position_x].walkable:
                player.add_position(0, -1)
        elif symbol == key.LEFT:
            if myMap.tiles[player.position_y][player.position_x-1].walkable:
                player.add_position(-1, 0)
        elif symbol == key.RIGHT:
            if myMap.tiles[player.position_y][player.position_x+1].walkable:
                player.add_position(1, 0)
        player.sprite.set_position(player.position_x * config.TILE_SIZE,
                                   player.position_y * config.TILE_SIZE)
        print player.position_x, player.position_y
        print myMap


@window.event
def on_draw():
    window.clear()
    batch.draw()
    player.sprite.draw()


pyglet.app.run()
