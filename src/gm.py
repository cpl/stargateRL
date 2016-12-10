import pyglet
import entity
import mapset
import config
import graphics

from pyglet.window import key

myMap = mapset.Map(config.MAP_SIZE_X, config.MAP_SIZE_Y)

player = entity.Player('Engineer', 1, 1, graphics.PRIEST,
                       myMap, 100, 100, True)

enemy = entity.Entity('Demon', 2, 3, graphics.DEMON, myMap, 100, 100, True)

window = pyglet.window.Window(config.WINDOW_SIZE_X, config.WINDOW_SIZE_Y)

label_player_name = pyglet.text.Label('Name: ' + player.name, x=10, y=config.WINDOW_SIZE_Y-20)
label_player_pos = pyglet.text.Label('POS: ' + str(player.position_x) + ' ' + str(player.position_y), x=200, y=config.WINDOW_SIZE_Y-20)

batch = pyglet.graphics.Batch()

for row in myMap.tiles:
    for tile in row:
        tile.sprite.batch = batch


@window.event
def on_key_press(symbol, modifiers):
    player.move(symbol)
    label_player_pos.text = 'POS: ' + str(player.position_x) + ' ' + str(player.position_y)


@window.event
def on_draw():
    window.clear()
    batch.draw()
    label_player_name.draw()
    label_player_pos.draw()
    enemy.sprite.draw()
    player.sprite.draw()


pyglet.app.run()
