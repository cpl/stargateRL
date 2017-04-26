from pyglet.window import key
from utility import config

DIRECTIONS = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0),
              'NE': (1, 1), 'SW': (-1, -1), 'SE': (1, -1), 'NW': (-1, 1),
              'XX': (0, 0)}

LAYOUT_VIKEYS = {key.K: DIRECTIONS['N'],
                 key.L: DIRECTIONS['E'],
                 key.J: DIRECTIONS['S'],
                 key.H: DIRECTIONS['W'],
                 key.Y: DIRECTIONS['NW'],
                 key.U: DIRECTIONS['NE'],
                 key.N: DIRECTIONS['SE'],
                 key.B: DIRECTIONS['SW'],
                 key.PLUS: DIRECTIONS['XX']}

LAYOUT_NUMPAD = {key.NUM_8: DIRECTIONS['N'],
                 key.NUM_6: DIRECTIONS['E'],
                 key.NUM_2: DIRECTIONS['S'],
                 key.NUM_4: DIRECTIONS['W'],
                 key.NUM_7: DIRECTIONS['NW'],
                 key.NUM_9: DIRECTIONS['NE'],
                 key.NUM_3: DIRECTIONS['SE'],
                 key.NUM_1: DIRECTIONS['SW'],
                 key.NUM_5: DIRECTIONS['XX']}

# TODO: Add Laptop layout keys!
LAYOUT_ARROWS = {key.UP: DIRECTIONS['N']}

LAYOUTS = {'vikeys': LAYOUT_VIKEYS,
           'numpad': LAYOUT_NUMPAD}

LAYOUT = LAYOUTS[config.controls_layout]
