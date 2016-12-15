import pyglet

from game_data import GraphxData


class GameWindow(pyglet.window.Window):

    def __init__(self, width, height, **kargs):
        super(GameWindow, self).__init__(width, height, **kargs)

    def __repr__(self):
        return '''GameWindow(Width:{},Height:{},Caption:{})\
               '''.format(self.width, self.height, self.caption)

    def on_draw(self):
        self.clear()
