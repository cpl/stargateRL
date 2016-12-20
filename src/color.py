''' color.py contains a set of variables (bytestrings) representing
    color values used within GraphxData, get_colored() method.
'''

# black = b'\xff\xff\xff\xff'
# white = b'\x00\x00\x00\xff'
#
# red = b'\xaa\x00\x00\xff'
# visiniu = b'\xaa\x55\x55\xff'
#
# sand = b'\xff\xfe\xc6\xff'
# sanddark = b'\xa5\xa5\x7d\xff'


class Color:

    def __init__(self, hexcode, alpha):
        self.hexcode = hexcode
        self.alpha = alpha

        self.color = self.hex_to_color(hexcode, alpha)

    def __repr__(self):
        return self.color

    def __getattribute__(self):
        return self.color

    def get_hex(self):
        return self.hexcode

    def get_color(self):
        return self.color

    def hex_to_color(self, hexcode, alpha):
        colorstring = ''
        for i in range(1, 7, 2):
            colorstring += chr(int(hexcode[i:i+2], 16))
        colorstring += chr(int(alpha, 16))

        return colorstring

BLACK = Color('#000000', 'ff')
WHITE = Color('#ffffff', 'ff')

TRANSPARENT = Color('#000000', '00')

RED = Color('#ff0000', 'ff')
GREEN = Color('#00ff00', 'ff')
BLUE = Color('#0000ff', 'ff')

ORANGE = Color('#f4a433', 'ff')

WOOD_DARK = Color('#775533', 'ff')
WOOD_LIGHT = Color('#bb9977', 'ff')

BRICK_DARK = Color('#773333', 'ff')
BRICK_LIGHT = Color('#cc5555', 'ff')


# def val_256():
#     _combinations = []
#     _final = []
#     for h1 in '0123456789abcdef':
#         for h2 in '0123456789abcdef':
#             _combinations.append(chr(int(str(h1+h2), 16)))
#     for c1 in _combinations:
#         for c2 in _combinations:
#             for c3 in _combinations:
#                 _final.append(c1+c2+c3)
#     return _final
#
#
# import cPickle
#
# colorlist = val_256()
# with open('colorlist.pkl', 'w+') as color_file:
#     cPickle.dump(colorlist, color_file)
