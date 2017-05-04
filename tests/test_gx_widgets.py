"""Main method for stargateRL."""

import pyglet

from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import GxTileset
from stargateRL.engine import widgets

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

main_menu = widgets.SelectionMenu(gx_tileset, 'Options')
red_box = widgets.FilledBoxWidget(gx_tileset, 1, 1, 10, 10, 'red')
blu_box = widgets.FilledBoxWidget(gx_tileset, 5, 5, 12, 20, 'blue')
grn_box = widgets.FilledBoxWidget(gx_tileset, 1, 1, 50, 5, 'green')

window.push_widget(red_box)
window.push_widget(grn_box)
window.push_widget(blu_box)

window.pop_widget()


@window.event
def on_key_press(symbol, modifiers):
    """Remove a widget on key press."""
    window.pop_widget()


pyglet.app.run()
