import pyglet
import mapset
import entity
import config
import graphx

from pyglet.window import key
from pyglet import gl


class GameWindow(pyglet.window.Window):

    def __init__(self):
        super(GameWindow, self).__init__(config.WINDOW_SIZE_X,
                                         config.WINDOW_SIZE_Y,
                                         caption='Stargate RL',
                                         fullscreen=config.WINDOW_FULLSCREEN,
                                         resizable=config.WINDOW_RESIZABLE)

        self.set_icon(pyglet.image.load(graphx.PRIEST))

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

        if config.CAMERA_FOLLOW_PLAYER:
            gl.glTranslatef(
                (-player.x * config.TILE_SIZE)+config.WINDOW_SIZE_X/2,
                (-player.y * config.TILE_SIZE)+config.WINDOW_SIZE_Y/2, 0)
        else:
            gl.glTranslatef(-self.VIEWPORT_X * config.TILE_SIZE,
                            -self.VIEWPORT_Y * config.TILE_SIZE, 0)

        self.clear()
        self.batch_map.draw()
        self.batch_entity.draw()

    def clearBatches(self):
        self.batch_map = pyglet.graphics.Batch()
        self.batch_entity = pyglet.graphics.Batch()

if __name__ == '__main__':
    game = GameWindow()

    mymap = mapset.Map(config.MAP_SIZE_X, config.MAP_SIZE_Y)
    mymap.loadMap('src/maps/test1.map')

    mymap.setBatch(game.batch_map)

    player = entity.Player('Engineer', 3, 3, mymap, '@', graphx.PRIEST)
    demon = entity.Entity('Demon', 4, 3, mymap, 'D', graphx.DEMON)

    player.sprite.batch = game.batch_entity
    demon.sprite.batch = game.batch_entity

    pyglet.app.run()
