import game_data
import game_window
import game_logic

import pyglet


class StarGateRL:

    def __init__(self, gm_window=None, gm_data=None, gm_logic=None):
        self.gm_window = gm_window
        self.gm_data = gm_data
        self.gm_logic = gm_logic

    def run(self):
        pyglet.app.run()


if __name__ == '__main__':
    sg_game = StarGateRL(game_window.GameWindow(600, 480, caption='SGRL'))
    sg_game.run()
