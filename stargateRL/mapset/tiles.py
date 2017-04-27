"""TODO DOCSTRING."""


class Tile(object):
    """A class representation of a tile logic."""

    def __init__(self, x, y, z):
        """Construct a tile."""
        if not isinstance(x, int) or\
           not isinstance(y, int) or\
           not isinstance(z, int):
            raise TypeError('The tile position must be a natural number.')

        if x < 0 or y < 0 or z < 0:
            raise AttributeError('The tile positions must be natural numbers.')

        self.position = (x, y, z)
