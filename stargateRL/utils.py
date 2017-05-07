"""Contains useful methods and global variables."""
import os
import json
import pyglet

from stargateRL.engine.graphx import GxTileset

__all__ = ['CONFIG', 'GX_TILESETS', 'GL_SCALING', 'INTENDED_SIZE']

# Define resource path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
pyglet.resource.path = [(os.path.abspath(os.path.join(ROOT_DIR, 'bin')))]


def load_config():
    """Load the config file."""
    config_file_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'config.json'))
    with open(config_file_name, 'r') as config_file:
        return json.load(config_file)


# Load the config
CONFIG = load_config()
# Load the tileset
GX_TILESETS = {'MAIN': GxTileset(CONFIG['resources']['tileset'],
                                 CONFIG['resources']['size'])}

# Graphical settings
INTENDED_SIZE = 16
GL_SCALING =\
    (INTENDED_SIZE / float(CONFIG['resources']['size']))\
    * CONFIG['graphics']['scale']
