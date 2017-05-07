"""Contains useful methods and global variables."""
import os
import json
import pyglet

from stargateRL.engine.graphx import GxTileset

__all__ = ['CONFIG', 'GX_TILESETS']

# Define resource path
pyglet.resource.path = [(os.path.abspath(os.path.join('bin')))]


def load_config():
    """Load the config file."""
    # Check local config first
    config_file_name = 'config.json'
    if os.path.isfile('config.local.json'):
        config_file_name = 'config.local.json'
    with open(config_file_name, 'r') as config_file:
        return json.load(config_file)


# Load the config
CONFIG = load_config()
# Load the tileset
GX_TILESETS = {'MAIN': GxTileset(CONFIG['resources']['tileset'],
                                 CONFIG['resources']['size'])}
