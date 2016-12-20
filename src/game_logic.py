from pyglet.window import key
from pyglet.window import mouse


STANDARD_DIRECTIONS = {key.UP: (0,   1), key.DOWN: (0,  -1),
                       key.RIGHT: (1,   0), key.LEFT: (-1,  0)}
MODIFIER_DIRECTIONS = {key.UP: (1,   1), key.DOWN: (-1,  -1),
                       key.RIGHT: (1,   -1), key.LEFT: (-1,  1)}


class GameLogic:
    ''' This class takes care of all logic behind the game, allowing the
    program to modify GameData.'''
    def __init__(self, game_data, game_window):
        self.game_data = game_data
        self.game_window = game_window

    def move_player(self, command, modifiers):
        ''' Based on the user input (arrow keys), the program determines
        the intended move direction of the player. The Cmd button can be used
        to move diagonally. The move_player method is called during the event
        on_key_press inside GameWindow.event.'''

        if modifiers == 512:
            if self.game_data.root_map.check_tile(
               self.game_data.player.get_position(),
               STANDARD_DIRECTIONS[command]):

                self.game_data.player.move(STANDARD_DIRECTIONS[command])
        elif modifiers == 576:
            if self.game_data.root_map.check_tile(
               self.game_data.player.get_position(),
               MODIFIER_DIRECTIONS[command]):

                self.game_data.player.move(MODIFIER_DIRECTIONS[command])

        self.game_window.update_player(self.game_data.player.x,
                                       self.game_data.player.y)
