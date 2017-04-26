from utility import config
from pyglet.sprite import Sprite

class FrameUI:
    
    def __init__ (self, gm_window, frame_tile, ratio_x=0, ratio_y=0, x=0, y=0):
        self.gm_window = gm_window
        self.frame_tile = frame_tile

        self.x = x
        self.y = y

        self.ratio_x = ratio_x
        self.ratio_y = ratio_y

        self.tiles_x = int(int(gm_window.width * self.ratio_x)/config.gfx_tilesize)
        self.tiles_y = int(int(gm_window.height * self.ratio_y)/config.gfx_tilesize)

        self.sprites = []

    def render_frame(self, gm_window):
        ts = config.gfx_tilesize

        print 'X:', self.tiles_x
        print 'Y:', self.tiles_y

        for x in range(self.tiles_x):
            self.sprites.append(Sprite(self.frame_tile, x*ts, 0,
                                batch=self.gm_window.batch_f))
            self.sprites.append(Sprite(self.frame_tile, x*ts, (self.tiles_y-1)*ts,
                                batch=self.gm_window.batch_f))


        for y in range(self.tiles_y):
            self.sprites.append(Sprite(self.frame_tile, 0, y*ts,
                                batch=self.gm_window.batch_f))
            self.sprites.append(Sprite(self.frame_tile, (self.tiles_x-1)*ts, y*ts,
                                batch=self.gm_window.batch_f))


#       for x in range(self.frame_x/ts):
#           self.sprites.append(Sprite(self.frame_tile, x*ts, 0,
#                                      batch=self.game_window.batch_f))
#           self.sprites.append(Sprite(self.frame_tile, x*ts, self.frame_y,
#                                      batch=self.game_window.batch_f))
#       y = 0


    def on_resize(self, width, height):
        pass
        #TODO: Add calculations for width and height!
        #NOTE: Switched to Vim
