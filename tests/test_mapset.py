"""Test mapset module."""

import unittest
from stargateRL.mapset import tiles, mapset


class TestTile(unittest.TestCase):
    """A set of tests for the Tile class."""

    def test_basic(self):
        """Test construction of a tile."""
        tile = tiles.Tile(1, 2, 0)
        self.assertIsInstance(tile, tiles.Tile)
        self.assertIsInstance(tile.position, tuple)

        self.assertEqual(tile.position[0], 1)
        self.assertEqual(tile.position[1], 2)
        self.assertEqual(tile.position[2], 0)

        with self.assertRaises(TypeError):
            tile.position[0] = 5
        self.assertEqual(tile.position[0], 1)

    def test_invalid_attriute(self):
        """Try creating invalid map."""
        tiles.Tile(0, 0, 0)
        with self.assertRaises(AttributeError):
            tiles.Tile(-1, -2, -3)

    def test_invalid_type(self):
        """Try creating invalid map."""
        with self.assertRaises(TypeError):
            tiles.Tile('0a', 'b', 2)


class TestMap(unittest.TestCase):
    """A set of test for the Map class."""

    def test_basic(self):
        """Test construction of a map."""
        mymap = mapset.Map(100, 120, 20)
        self.assertIsInstance(mymap, mapset.Map)
        self.assertIsInstance(mymap.dimensions, tuple)

        self.assertEqual(mymap.dimensions[0], 100)
        self.assertEqual(mymap.dimensions[1], 120)
        self.assertEqual(mymap.dimensions[2], 20)

        with self.assertRaises(TypeError):
            mymap.dimensions[0] = 0
        self.assertEqual(mymap.dimensions[0], 100)

    def test_invalid_attriute(self):
        """Try creating invalid map."""
        with self.assertRaises(AttributeError):
            mapset.Map(0, 0, 0)
        with self.assertRaises(AttributeError):
            mapset.Map(-1, -1, -2)
        with self.assertRaises(AttributeError):
            mapset.Map(0, 100, 10)

    def test_invalid_type(self):
        """Try creating invalid map."""
        with self.assertRaises(TypeError):
            mapset.Map('0a', 'b', 2)
