"""Helper methods for the world module."""

import math
import json
from os.path import join, isfile

from noise import snoise2, pnoise2
from enum import Enum

from stargateRL.debug import logger
from stargateRL.paths import DirectoryPaths


def noise(x, y, width, height, mode='simplex'):
    """Return noise between 0.0 and 1.0."""
    global TOTAL_TIME
    if mode == 'simplex':
        return snoise2(x, y, repeatx=width, repeaty=height) / 2.0 + 0.5
    elif mode == 'perlin':
        return pnoise2(x, y, repeatx=width, repeaty=height) / 2.0 + 0.5
    else:
        raise Exception('Please provide as mode=[simplex|perlin]')


def normalize(value, min_value, max_value):
    """Normalize the given value between 0.0 and 1.0."""
    return float(value - min_value) / float(max_value + min_value)


def continent(elevation, push, edges, strenght, nx, ny):
    """Transform the terrain into continents."""
    distance = 2 * max(abs(nx), abs(ny))
    return (elevation + push) * (edges - 1.0 * math.pow(distance, strenght))


class Biomes(Enum):
    """A set of constants representing biomes."""

    OCEAN = 0
    SEA = 1
    LAKE = 2
    RIVER = 3
    TROPICAL_RAIN_FOREST = 4
    TROPICAL_SEASONAL_FOREST = 5
    GRASSLAND = 6
    SUBTROPICAL_DESERT = 7
    TEMPERATE_RAIN_FOREST = 8
    TEMPERATE_DECIDUOUS_FOREST = 9
    TEMPERATE_DESERT = 10
    TAIGA = 11
    SHRUBLAND = 12
    SNOW = 13
    TUNDRA = 14
    BARE = 15
    SCORCHED = 16


def read_profile(name, format):
    """Read a config file, -1 is random."""
    logger.debug('Reading profile %s %s', name, format)
    if format not in ('elv', 'mst', 'wd'):
        raise Exception('Profile format must be mst/elv/wd, found %s' % format)

    name = '%s_%s.profile.json' % (format, name)
    path = join(DirectoryPaths.PROFILES.value, name)
    if isfile(path):
        with open(path, 'r') as fp:
            return json.load(fp)
    else:
        raise Exception('Given profile was not found, %s' % name)
