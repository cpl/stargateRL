import pyglet
import mapset
import entity
import config

import json

from pyglet.window import key
from pyglet.window import mouse

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

        self.set_mouse_visible(config.window['visibleMouse'])

        self.selector = mapset.Selector(config.graphx['selector'])

    def on_key_press(self, symbol, modifiers):
        self.player.move(symbol)

        if modifiers:
            self.selector.move(symbol)
        else:
            if symbol == key.D:
                self.VIEWPORT_X += 1
            elif symbol == key.A:
                self.VIEWPORT_X -= 1
            elif symbol == key.S:
                self.VIEWPORT_Y -= 1
            elif symbol == key.W:
                self.VIEWPORT_Y += 1

        if symbol == key.Q:
            with open(config.root['map_json']+'map.json', 'w+') as outputFile:
                json.dump(mymap.save(), outputFile, indent=2)

    def on_draw(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        if config.window['cameraFollow']:
            gl.glTranslatef(
             (-self.player.x *
              config.mapdata['tileSize'])+config.window['width']/2,
             (-self.player.y *
              config.mapdata['tileSize'])+config.window['height']/2,
             0)
        else:
            gl.glTranslatef(-self.VIEWPORT_X * config.mapdata['tileSize'],
                            -self.VIEWPORT_Y * config.mapdata['tileSize'], 0)

        self.clear()
        self.batch_map.draw()
        self.batch_entity.draw()
        self.selector.sprite.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.selector.on_mouse_motion(x, y, dx, dy)

    def clearBatches(self):
        self.batch_map = pyglet.graphics.Batch()
        self.batch_entity = pyglet.graphics.Batch()
