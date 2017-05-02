"""Main method for stargateRL."""

import pyglet
from engine.screen import GameWindow
from engine.graphx import GxTileset

import json

gxTileset = GxTileset('tileset.png', 16)

# Load config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Create the game window
windowConfig = config['graphics']['window']
window = GameWindow(windowConfig['width'], windowConfig['height'], gxTileset,
                    fullscreen=windowConfig['fullscreen'],
                    resizable=windowConfig['resizable'],
                    style=windowConfig['style'])

pyglet.app.run()
