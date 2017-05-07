"""Graphical test for Box Widget."""

import pyglet

from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import TileColor, Geometry
from stargateRL.engine import widgets
from stargateRL.utils import CONFIG

pyglet.options['debug_gl'] = False

# Create the game window
window_config = CONFIG['window']

window = GameWindow(window_config['width'],
                    window_config['height'],
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

red_box = widgets.FilledBoxWidget(Geometry(0, 0, 300, 300),
                                  TileColor('red', 'border'))
window.push_widget(red_box)

pyglet.app.run()
