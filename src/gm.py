import pyglet
import mapset
import entity
import config
import graphx

from pyglet.window import key
from pyglet import gl

window = pyglet.window.Window(config.WINDOW_SIZE_X,
                              config.WINDOW_SIZE_Y,
                              caption='Stargate RL')

icon = pyglet.image.load(graphx.PRIEST)
window.set_icon(icon)

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
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    # This makes the "camera" follow the player
    gl.glTranslatef((-player.x * config.TILE_SIZE)+config.WINDOW_SIZE_X/2,
                    (-player.y * config.TILE_SIZE)+config.WINDOW_SIZE_Y/2, 0)

    window.clear()
    batch_map.draw()
    batch_entity.draw()


@window.event
def on_key_press(symbol, modifiers):
    player.move(symbol)


pyglet.app.run()
