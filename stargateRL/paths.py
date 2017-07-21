"""All relevant paths for stargateRL."""

import os
import sys

import os.path as path

from enum import Enum


# Directories
class DirectoryPaths(Enum):
    """Create a enum of all relevant directory paths."""

    ROOT = path.abspath(os.path.join(sys.prefix, 'stargateRL'))
    DATA = path.join(ROOT, 'data')
    EXPORTS = path.join(DATA, 'exports')
    SAVES = path.join(DATA, 'saves')
    BIN = path.join(DATA, 'bin')
    TILES = path.join(BIN, 'tiles')


# Files
class FilePaths(Enum):
    """Create an enum of all relevant file paths."""

    CONFIG = path.join(DirectoryPaths.DATA, 'config.json')
    ICON = path.join(DirectoryPaths.BIN, 'icon.png')
