import pyglet
import config
import color

from game_data import GraphxData


class GameWindow(pyglet.window.Window):

    def __init__(self, width, height, **kargs):
        super(GameWindow, self).__init__(width, height, **kargs)

        self.graphx = None
        self.tiles_batch = pyglet.graphics.Batch()

    def __repr__(self):
        return '''GameWindow(Width:{},Height:{},Caption:{})\
               '''.format(self.width, self.height, self.caption)

    def load_graphx(self, path, size):
        self.graphx = GraphxData(path, size)

    def load_mapset(self, tiles):
        self.tiles_sprites = []
        for tile in tiles:
            if tile.symbol == '#':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.get_colored(35, color.red, color.visiniu),
                                         tile.x*16, tile.y*16,
                                         batch=self.tiles_batch))
            elif tile.symbol == '.':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.get_colored(43, color.sand, color.sanddark),
                                         tile.x*16, tile.y*16,
                                         batch=self.tiles_batch))
            elif tile.symbol == ')':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.tile_set[0],
                                         tile.x*16, tile.y*16,
                                         batch=self.tiles_batch))
            elif tile.symbol == ']':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.tile_set[0],
                                         tile.x*16, tile.y*16,
                                         batch=self.tiles_batch))
            else:
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.tile_set[1],
                                         tile.x*16, tile.y*16,
                                         batch=self.tiles_batch))

    def on_draw(self):
        self.clear()
        self.tiles_batch.draw()
