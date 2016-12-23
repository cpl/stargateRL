from pyglet.window import key
from pyglet.window import mouse

from utility import controls


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

        if self.game_data.root_map.check_tile(
           self.game_data.player.get_position(),
           controls.LAYOUT[command]):

            self.game_data.root_map.get_tile(
                self.game_data.player.x,
                self.game_data.player.y).entity = None

            self.game_data.player.move(controls.LAYOUT[command])

            self.game_data.root_map.get_tile(
                self.game_data.player.x,
                self.game_data.player.y).entity = self.game_data.player

            self.game_window.update_player(self.game_data.player.x,
                                           self.game_data.player.y)

    def move_selector(self, command, modifiers):

        self.game_window.selector.move(
            controls.LAYOUT[command])

        self.game_window.selector.get_info(self.game_data)
        self.game_window.update_selector()

    def mouse_selector(self, x, y):
        self.game_window.selector.mouse(x, y)
        self.game_window.selector.get_info(self.game_data)
        self.game_window.update_selector()
