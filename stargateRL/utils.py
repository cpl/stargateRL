"""Contains useful methods and global variables."""
import json
import pyglet

from stargateRL.engine.graphx import GxTileset
from stargateRL.paths import DirectoryPaths, FilePaths

__all__ = ['CONFIG', 'GX_TILESETS', 'GL_SCALING', 'INTENDED_SIZE']


# Reset pyglet resources path then append custom ones
pyglet.resource.path = []
pyglet.resource.path.append((DirectoryPaths.BIN.value))
pyglet.resource.path.append((DirectoryPaths.TILES.value))


def load_config():
    """Load the config file."""
    with open(FilePaths.CONFIG.value, 'r') as config_file:
        return json.load(config_file)


def save_config(config_dictionary):
    """Save the config changes."""
    with open(FilePaths.CONFIG.value, 'w') as config_file:
        json.dump(config_dictionary, config_file, indent=4, sort_keys=True)


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
