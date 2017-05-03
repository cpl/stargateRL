"""Main method for stargateRL."""

import pyglet
from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import GxTileset

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
                    gx_tileset,
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

pyglet.app.run()
