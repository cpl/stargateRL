"""Helper methods for the world module."""

import math
import json
from os.path import join

from noise import snoise2, pnoise2
from enum import Enum

from stargateRL.paths import DirectoryPaths


import time


TOTAL_TIME = 0


def noise(x, y, width, height, mode='simplex'):
    """Return noise between 0.0 and 1.0."""
    global TOTAL_TIME
    if mode == 'simplex':
        _t0 = time.time()
        r = snoise2(x, y, repeatx=width, repeaty=height) / 2.0 + 0.5
        TOTAL_TIME += time.time() - _t0
        print TOTAL_TIME
        return r
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


def read_profile(name):
    """Read a config file, -1 is random."""
    with open(join(DirectoryPaths.PROFILES.value, name), 'r') as fp:
        return json.load(fp)


# Temporary
# TODO: Replace this with .json profiles
class Profiles(Enum):
    """A set of constants representing world generation profiles."""

    DEFAULT = {'settings': {'scale': 1.0, 'octaves': 5,
                            'exponent': 4, 'persistance': 0.5,
                            'lacunarity': 3.0, 'terraces': 1.0,
                            'continent_filter': True, 'offset': (0, 0),
                            'mode': 'simplex'},
               'seed': -1}

    TESTING = {'settings': {'scale': 1.0, 'octaves': 5,
                            'exponent': 5, 'persistance': 0.5,
                            'lacunarity': 3.0, 'terraces': 1.0,
                            'continent_filter': True, 'offset': (0, 0),
                            'mode': 'simplex',
                            'width': -1, 'height': 0},
               'seed': -1}

    ARCHIPELAGO = {'settings': {'scale': 0.5, 'octaves': 5,
                                'exponent': 6, 'persistance': 0.5,
                                'lacunarity': 3.0, 'terraces': 1.0,
                                'continent_filter': True, 'offset': (0, 0),
                                'mode': 'simplex'},
                   'seed': -1}
