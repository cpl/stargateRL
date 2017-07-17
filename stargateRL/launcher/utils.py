"""Contains useful methods and global variables."""

import json
from stargateRL.paths import FilePaths


def load_config():
    """Load the config file."""
    with open(FilePaths.CONFIG.value, 'r') as config_file:
        return json.load(config_file)


def save_config(config_dictionary):
    """Save the config changes."""
    with open(FilePaths.CONFIG.value, 'w') as config_file:
        json.dump(config_dictionary, config_file, indent=4, sort_keys=True)
