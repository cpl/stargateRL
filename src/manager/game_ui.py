from utility import config

class FrameUI:
    
    def __init__ (self, game_window):
        self.game_window = game_window

        self.map_width = 0
        self.map_height = 0

        self.right_width = 0
        self.right_height = 0

        self.bottom_width = 0
        self.bottom_height = 0

    @window.event
    def on_resize(self, width, height):
        pass
        #TODO: Add calculations for width and height!
        #NOTE: Switched to Vim
