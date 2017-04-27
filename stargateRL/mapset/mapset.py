"""TODO DOCSTRING."""


class Map(object):
    """A class representation of a map logic."""

    def __init__(self, size_x, size_y, size_z):
        """Construct a map of given sizes."""
        if not isinstance(size_x, int) or\
           not isinstance(size_y, int) or\
           not isinstance(size_z, int):
            raise TypeError('The map dimensions must be positive integers.')

        if size_x <= 0 or size_y <= 0 or size_z <= 0:
            raise AttributeError('The map dimensions must be POSITIVE ints.')

        self.dimensions = (size_x, size_y, size_z)
        self.tiles = []
