"""Contains useful methods and global variables."""
import pyglet

from stargateRL.engine.graphx import GxTileset
from stargateRL.paths import DirectoryPaths
from stargateRL.launcher.utils import load_config

# Reset pyglet resources path then append custom ones
pyglet.resource.path = []
pyglet.resource.path.append((DirectoryPaths.BIN.value))
pyglet.resource.path.append((DirectoryPaths.TILES.value))


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
