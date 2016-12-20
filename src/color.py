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

        print colorstring
        return colorstring

BLACK = Color('#000000', 'ff')
WHITE = Color('#ffffff', 'ff')

RED = Color('#ff0000', 'ff')
GREEN = Color('#00ff00', 'ff')
BLUE = Color('#0000ff', 'ff')

WOOD_DARK = Color('#775533', 'ff')
WOOD_LIGHT = Color('#bb9977', 'ff')

BRICK_DARK = Color('#773333', 'ff')
BRICK_LIGHT = Color('#cc5555', 'ff')

a = 'HELP'
a += BRICK_DARK.get_color()
print a
