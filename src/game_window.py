import pyglet
import config
import color

from game_data import GraphxData


class GameWindow(pyglet.window.Window):

    def __init__(self, width, height, **kargs):
        super(GameWindow, self).__init__(width, height, **kargs)

        self.graphx = None
        self.batch_t = pyglet.graphics.Batch()
        self.batch_p = pyglet.graphics.Batch()
        self.batch_e = pyglet.graphics.Batch()

    def __repr__(self):
        return '''GameWindow(Width:{},Height:{},Caption:{})\
               '''.format(self.width, self.height, self.caption)

    def load_graphx(self, path, size):
        self.graphx = GraphxData(path, size)

    def render_player(self, player):
        ts = config.gfx_tilesize
        self.player_sprite = pyglet.sprite.Sprite(
            self.graphx.get_colored(64, '\x00\x00\x00\xff', '\x88\x88\x88\x88'),
            player.x*ts, player.y*ts, batch=self.batch_p)

    def update_player(self, x, y):
        self.player_sprite.set_position(x*config.gfx_tilesize,
                                        y*config.gfx_tilesize)

    def render_mapset(self, tiles):
        ts = config.gfx_tilesize

        self.tiles_sprites = []
        for tile in tiles:
            if tile.symbol == '#':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.get_colored(35, color.red, color.visiniu),
                                         tile.x*ts, tile.y*ts,
                                         batch=self.batch_t))
            elif tile.symbol == '.':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.get_colored(43, color.sand, color.sanddark),
                                         tile.x*ts, tile.y*ts,
                                         batch=self.batch_t))
            elif tile.symbol == ')':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.get_tile(41),
                                         tile.x*ts, tile.y*ts,
                                         batch=self.batch_t))
            elif tile.symbol == ']':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.get_tile(41),
                                         tile.x*ts, tile.y*ts,
                                         batch=self.batch_t))
            else:
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(self.graphx.tile_set[1],
                                         tile.x*ts, tile.y*ts,
                                         batch=self.batch_t))

    def on_draw(self):
        self.clear()
        self.batch_t.draw()
        self.batch_p.draw()
