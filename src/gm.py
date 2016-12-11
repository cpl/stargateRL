import pyglet
import mapset
import entity
import config
import graphx

window = pyglet.window.Window(config.WINDOW_SIZE_X,
                              config.WINDOW_SIZE_Y)

batch_map = pyglet.graphics.Batch()
batch_entity = pyglet.graphics.Batch()

mymap = mapset.Map(config.MAP_SIZE_X, config.MAP_SIZE_Y)
mymap.loadMap('src/maps/test1.map')
mymap.setBatch(batch_map)

player = entity.Player('Engineer', 3, 3, mymap, '@', graphx.PRIEST)
demon = entity.Entity('Demon', 4, 3, mymap, 'D', graphx.DEMON)

player.sprite.batch = batch_entity
demon.sprite.batch = batch_entity

demon.setPosition(1, 1)
demon.setPosition(0, 0)
demon.addPosition(0, 1)
demon.addPosition(1, 0)


@window.event
def on_draw():
    window.clear()
    batch_map.draw()
    batch_entity.draw()


@window.event
def on_key_press(symbol, modifiers):
    player.move(symbol)


pyglet.app.run()
