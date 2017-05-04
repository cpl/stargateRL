"""Graphical test for Box Widget."""

import pyglet
import cProfile

from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import TileColor
from stargateRL.engine import widgets
from stargateRL.utils import CONFIG

pyglet.options['debug_gl'] = False

# Create the game window
window_config = CONFIG['graphics']['window']

window = GameWindow(window_config['width'],
                    window_config['height'],
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

for x in range(0, window_config['width']/16, 8):
    for y in range(0, window_config['height']/16, 8):
        window.push_widget(widgets.FilledBoxWidget(x, y, 8, 8,
                                                   TileColor('blue',
                                                             'blue'),
                                                   0))

grn_box = widgets.FilledBoxWidget(10, 10, 20, 5, TileColor('red', 'border'))
window.push_widget(grn_box)

cProfile.run('pyglet.app.run()')
