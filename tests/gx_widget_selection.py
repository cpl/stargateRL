"""Graphical test for SlectionMenu Widget."""

import pyglet

from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import TileColor
from stargateRL.engine import widgets
from stargateRL.utils import CONFIG


# Create the game window
window_config = CONFIG['graphics']['window']

window = GameWindow(window_config['width'],
                    window_config['height'],
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

sel_mnu = widgets.SelectionMenuWidget(window.x_tiles/4, window.y_tiles/4,
                                      window.x_tiles/2, window.y_tiles/2,
                                      TileColor('gold', 'transparent'),
                                      TileColor('white', 'transparent'),
                                      TileColor('red', 'gold'),
                                      'New Thing', 'Debug', 'Settings', 'Exit')

window.push_widget(sel_mnu)

pyglet.app.run()
