import pyglet
import mapset
import entity
import config

import json

from pyglet.window import key
from pyglet.window import mouse

from pyglet import gl


class GameWindow(pyglet.window.Window):

    def __init__(self, width, height):
        super(GameWindow, self).__init__(width, height, caption='Stargate RL',
                                         fullscreen=config.window['fullscreen'],
                                         resizable=config.window['resizable'])

        self.set_icon(pyglet.image.load(config.graphx['priest']))

        self._batch_map = None
        self._batch_entity = None

        self._selector = None

        self._viewport_x = 0
        self._viewport_y = 0

        self.set_mouse_visible(config.mouse['visible'])

        self._text_area_look = pyglet.text.Label(
            'Stargate RL',
            font_name='Roboto',
            font_size=12,
            x=30, y=40,
            anchor_x='left', anchor_y='center')

        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA,
                              pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    def on_key_press(self, symbol, modifiers):
        self._player.move(symbol)

        if modifiers:
            self._selector.move(symbol)
        else:
            if symbol == key.D:
                self._viewport_x += 1
            elif symbol == key.A:
                self._viewport_x -= 1
            elif symbol == key.S:
                self._viewport_y -= 1
            elif symbol == key.W:
                self._viewport_y += 1

    def on_mouse_motion(self, x, y, dx, dy):
        self._selector.on_mouse_motion(x, y, dx, dy)

    def on_draw(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        if config.window['camera_follow']:
            gl.glTranslatef(
             (-self._player._x *
              config.mapdata['tile_size'])+config.window['width']/2,
             (-self._player._y *
              config.mapdata['tile_size'])+config.window['height']/2, 0)
        else:
            gl.glTranslatef(-self._viewport_x * config.mapdata['tile_size'],
                            -self._viewport_y * config.mapdata['tile_size'], 0)

        self.clear()
        self._batch_map.draw()
        self._batch_entity.draw()
        self._selector._sprite.draw()
        Panel((20*32, 0), (26*32, 14*32), 33, 255, self._viewport_x, self._viewport_y)
        self._text_area_look.draw()


class Panel():
    def __init__(self, point_bl, point_tr, grey, alpha, sX, sY):
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                             ('v2f', (point_bl[0]+sX*32, point_bl[1]+sY*32,
                                      point_bl[0]+sX*32, point_tr[1]+sY*32,
                                      point_tr[0]+sX*32, point_tr[1]+sY*32,
                                      point_tr[0]+sX*32, point_bl[1]+sY*32)),
                             ('c4B', (grey, grey, grey, alpha)*4))
