import pyglet

from utility import config
from utility import color

from manager.game_data import GraphxData
from manager.game_data import GraphxSelector


class GameWindow(pyglet.window.Window):
    ''' In charge of rendering everything from given game data. '''
    def __init__(self, width, height, **kargs):
        super(GameWindow, self).__init__(width, height, **kargs)

        self.graphx = None
        self.selector = None

        self.batch_t = pyglet.graphics.Batch() # Tiles
        self.batch_p = pyglet.graphics.Batch() # Player
        self.batch_e = pyglet.graphics.Batch() # Entities
        self.batch_f = pyglet.graphics.Batch() # Frame

    def __repr__(self):
        return '''GameWindow(Width:{},Height:{},Caption:{})\
               '''.format(self.width, self.height, self.caption)

    def load_graphx(self, path, size):
        self.graphx = GraphxData(path, size)
        self.selector = GraphxSelector(
            0, 0, self.graphx.get_colored(176,
                                          color.TRANSPARENT.get_color(),
                                          color.ORANGE.get_color()))

    def update_selector(self):
        ts = config.gfx_tilesize
        self.selector.sprite.set_position(self.selector.x*ts,
                                          self.selector.y*ts)

    def render_player(self, player):
        ts = config.gfx_tilesize
        self.player_sprite = pyglet.sprite.Sprite(
            self.graphx.get_colored(64, '\x00\x00\x00\xff', '\x88\x88\x88\x88'),
            player.x*ts, player.y*ts, batch=self.batch_p)

    def render_entities(self, entities):
        ts = config.gfx_tilesize
        self.entities_sprites = []
        for entity in entities:
            self.entities_sprites.append(
                pyglet.sprite.Sprite(self.graphx.get_tile(1),
                                     entity.x*ts, entity.y*ts,
                                     batch=self.batch_e))

    def update_player(self, x, y):
        self.player_sprite.set_position(x*config.gfx_tilesize,
                                        y*config.gfx_tilesize)

    def render_mapset(self, tiles):
        ts = config.gfx_tilesize

        # TODO: Improve tile detection and rendering

        self.tiles_sprites = []
        for tile in tiles:

            if tile.symbol == '#':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(
                        self.graphx.get_colored(35,
                                                color.BRICK_LIGHT.get_color(),
                                                color.BRICK_DARK.get_color()),
                        tile.x*ts, tile.y*ts, batch=self.batch_t))

            elif tile.symbol == '.':
                self.tiles_sprites.append(
                    pyglet.sprite.Sprite(
                        self.graphx.get_colored(43,
                                                color.WOOD_LIGHT.get_color(),
                                                color.WOOD_DARK.get_color()),
                        tile.x*ts, tile.y*ts, batch=self.batch_t))

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
        self.batch_e.draw()
        self.batch_p.draw()
        self.selector.sprite.draw()
        self.batch_f.draw()
