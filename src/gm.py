import pyglet
import mapset
import entity
import config

from pyglet.window import key
from pyglet import gl


class GameWindow(pyglet.window.Window):

    def __init__(self):
        super(GameWindow, self).__init__(config.window['width'],
                                         config.window['height'],
                                         caption='Stargate RL',
                                         fullscreen=config.window['fullscreen'],
                                         resizable=config.window['resizable'])

        self.set_icon(pyglet.image.load(config.graphx['priest']))

        self.batch_map = pyglet.graphics.Batch()
        self.batch_entity = pyglet.graphics.Batch()

        self.VIEWPORT_X = 0
        self.VIEWPORT_Y = 0

    def on_key_press(self, symbol, modifiers):
        player.move(symbol)

        if symbol == key.D:
            self.VIEWPORT_X += 1
        elif symbol == key.A:
            self.VIEWPORT_X -= 1
        elif symbol == key.S:
            self.VIEWPORT_Y -= 1
        elif symbol == key.W:
            self.VIEWPORT_Y += 1

    def on_draw(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        if config.window['cameraFollow']:
            gl.glTranslatef(
             (-player.x * config.mapdata['tileSize'])+config.window['width']/2,
             (-player.y * config.mapdata['tileSize'])+config.window['height']/2,
             0)
        else:
            gl.glTranslatef(-self.VIEWPORT_X * config.mapdata['tileSize'],
                            -self.VIEWPORT_Y * config.mapdata['tileSize'], 0)

        self.clear()
        self.batch_map.draw()
        self.batch_entity.draw()

    def clearBatches(self):
        self.batch_map = pyglet.graphics.Batch()
        self.batch_entity = pyglet.graphics.Batch()

if __name__ == '__main__':
    game = GameWindow()

    mymap = mapset.Map(config.mapdata['lenX'], config.mapdata['lenY'])
    mymap.loadMap('data/map_ascii/test1.map')

    mymap.setBatch(game.batch_map)

    player = entity.Player('Engineer', 3, 3,
                           mymap, '@', config.graphx['priest'])

    demon = entity.Entity('Demon', 4, 3, mymap, 'D', config.graphx['demon'])

    player.sprite.batch = game.batch_entity
    demon.sprite.batch = game.batch_entity

    pyglet.app.run()
