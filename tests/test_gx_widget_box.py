"""Graphical test for Box Widget."""

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

red_box = widgets.FilledBoxWidget(1, 1, 10, 10, TileColor('border', 'red'))
blu_box = widgets.FilledBoxWidget(10, 5, 2, 10, TileColor('blue', 'gold'))
grn_box = widgets.FilledBoxWidget(10, 10, 20, 5, TileColor('green', 'green'))

window.push_widget(red_box)
window.push_widget(grn_box)
window.push_widget(blu_box)

pyglet.app.run()
