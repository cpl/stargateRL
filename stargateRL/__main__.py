"""Main method for stargateRL."""

import pyglet

from engine.screen import GameWindow
from engine.graphx import GxTileset
from engine import widgets

import json

# Load config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


# Load the tileset
gx_tileset = GxTileset(config['resources']['tileset'],
                       config['graphics']['size'])

# Create the game window
window_config = config['graphics']['window']

window = GameWindow(window_config['width'],
                    window_config['height'],
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

window.push_widget(widgets.SelectionMenu('a', 'b', 'c'))

pyglet.app.run()
