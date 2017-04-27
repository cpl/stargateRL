"""TODO DOCSTRING."""


class Entity(object):
    """A class representing a NPC or any type of in-world object."""

    def __init__(self, name, x=-1, y=-1):
        """Construct a primitive entity."""
        self.name = name
        self.x = x
        self.y = y
