from pyglet.window import key
from pyglet.window import mouse


class GameLogic:

    def __init__(self, game_data, game_window):
        self.game_data = game_data
        self.game_window = game_window

    def move_player(self, symbol, modifiers):
        if modifiers == 512:
            if symbol == key.UP:
                self.game_data.player.move(0,  1)
            elif symbol == key.DOWN:
                self.game_data.player.move(0, -1)
            elif symbol == key.LEFT:
                self.game_data.player.move(-1, 0)
            elif symbol == key.RIGHT:
                self.game_data.player.move(1,  0)
        elif modifiers == 576:
            if symbol == key.UP:
                self.game_data.player.move(-1,  1)
            elif symbol == key.DOWN:
                self.game_data.player.move(1, -1)
            elif symbol == key.LEFT:
                self.game_data.player.move(-1, -1)
            elif symbol == key.RIGHT:
                self.game_data.player.move(1,   1)

        self.game_window.update_player(self.game_data.player.x,
                                       self.game_data.player.y)
