"""TODO DOCSTRING."""


from tiles import Tile
from mapset import Map


class Generator(object):
    """A standard generator with stub methods."""

    def __init__(self, x, y, z, mode=0, name=None):
        """Provide config for the map."""
        self.x = x
        self.y = y
        self.z = z
        self.mode = mode
        self.name = name

        self.map_data = None

    def display_ascii(self):
        """Print out the map data as ASCII."""
        pass

    def create(self):
        """Create the map data."""
        pass

    def get_map(self):
        """Return the map object with the map data."""
        if self.map_data is not None:
            map_obj = Map(self.x, self.y, self.z, self.name)
            map_obj.tiles = self.map_data

            return map_obj
        else:
            self.create()
            return self.get_map()


class Flat(Generator):
    """A flat map generator. Good for testing."""

    def __init__(self, x, y, tags, name):
        """Construc a flat map generator."""
        self.tags = tags
        super(Flat, self).__init__(x, y, 1, name=name)

    def create(self):
        """Create the map data."""
        self.map_data = [[Tile(x, y, 1, self.tags)
                         for x in range(self.x)]
                         for y in range(self.y)]
