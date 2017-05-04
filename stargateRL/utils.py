"""Contains useful methods and global variables."""
import os
import json
from stargateRL.engine.graphx import GxTileset

__all__ = ['CONFIG', 'GX_TILESETS']


def load_config():
    """Load the config file."""
    # Check local config first
    config_file_name = 'config.json'
    if os.path.isfile('config.local.json'):
        config_file_name = 'config.local.json'
    with open(config_file_name, 'r') as config_file:
        return json.load(config_file)


CONFIG = load_config()
# Load the tileset
GX_TILESETS = {'MAIN': GxTileset(CONFIG['resources']['tileset'],
                       CONFIG['graphics']['size'])
			  }

