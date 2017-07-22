"""Terain generators."""

import math
import random
import cPickle as pickel
from os import path

from stargateRL.world.utils import normalize, noise, continent
from stargateRL.paths import DirectoryPaths


class NoiseGenerator(object):
    """Construct the terrain heightmap."""

    def __init__(self, width, height, seed, settings=None):
        """Construct the terrain."""
        self._width = width
        self._height = height

        # Generate empty noise map
        self._noise_map = [[None for _ in range(width)] for _ in range(height)]

        # If no settings are given, use defaults
        if settings is None:
            self._settings = {'seed': seed, 'scale': 150.0, 'octaves': 5,
                              'exponent': 4, 'persistance': 0.5,
                              'lacunarity': 3.0, 'terraces': 1.0,
                              'continent_filter': True, 'width': width,
                              'height': height, 'offset': (0, 0),
                              'mode': 'simplex'}
        else:
            self._settings = settings

        self.generate_noise_map()

    def get(self, x, y):
        """Return the noise value at x, y."""
        return self._noise_map[x][y]

    def set(self, x, y, value):
        """Set the noise value at x, y."""
        self._noise_map[x][y] = value

    def settings(self):
        """Return the settings used in generation."""
        return self._settings

    def data(self):
        """Return the noise map data."""
        return self._noise_map

    def generate_noise_map(self):
        """Fill the elevation matrix with noise."""
        # Initial min/max values
        max_noise = 0.0
        min_noise = 0.0

        # Apply offset to the noise map
        octaves_offsets = []
        for _ in range(self._settings['octaves']):
            offset_x = random.randint(-100000, 100000) + \
                self._settings['offset'][0]
            offset_y = random.randint(-100000, 100000) + \
                self._settings['offset'][1]
            octaves_offsets.append((offset_x, offset_y))

        # Go trough each position on the map, and generate the noise
        for y in range(self._height):
            for x in range(self._width):

                # Initialize the noise parameters
                amplitude = 1.0
                frequency = 1.0
                noise_height = 0.0

                # Adjust parameters
                scale = self._settings['scale']
                for octave in range(self._settings['octaves']):
                    sample_x = float(x - self._width / 2) / scale * \
                        frequency + octaves_offsets[octave][0]
                    sample_y = float(y - self._height / 2) / scale * \
                        frequency + octaves_offsets[octave][1]

                    # Obtain noise from the noise library
                    noise_value = noise(sample_x, sample_y,
                                        self._width, self._height,
                                        self._settings['mode'])

                    noise_height += noise_value * amplitude

                    # Update parameters for each octave
                    amplitude *= self._settings['persistance']
                    frequency *= self._settings['lacunarity']

                # Find normalization values
                if noise_height > max_noise:
                    max_noise = noise_height
                if noise_height < min_noise:
                    min_noise = noise_height

                self._noise_map[x][y] = noise_height

        # Prepare for another normalization
        mnoise = None
        xnoise = None
        for y in range(self._height):
            for x in range(self._width):
                # Normalize heightmap values between 0.0 and 1.0
                noise_height = normalize(self._noise_map[x][y],
                                         min_noise, max_noise)

                # Apply exponential filter to clear land mass
                noise_height = math.pow(noise_height,
                                        self._settings['exponent'])

                # Apply continental filter
                if self._settings['continent_filter']:
                    noise_height = continent(noise_height, 0.0, 1.0, 5.0,
                                             float(x) / self._width - 0.5,
                                             float(y) / self._height - 0.5)

                # Check if terraces were enabled and generate terraces
                terraces = self._settings['terraces']
                if terraces != 1.0:
                    noise_height = round(noise_height * terraces) / terraces

                # Check for normalization values
                if noise_height > xnoise or xnoise is None:
                    xnoise = noise_height
                if noise_height < mnoise or mnoise is None:
                    mnoise = noise_height

                self._noise_map[x][y] = noise_height

        # Apply final changes
        for y in range(self._height):
            for x in range(self._width):
                self._noise_map[x][y] = normalize(self._noise_map[x][y],
                                                  mnoise, xnoise)


class WorldData(object):
    """Construct and store all world data."""

    def __init__(self, seed=0, width=500, height=500):
        """Construct the biomes using elevation and moisture."""
        seed = random.getrandbits(21) if seed == -1 else seed
        random.seed(seed)

        self.width = width
        self.height = height

        # Generate map data using noise
        self._generator_elevation = NoiseGenerator(width, height, seed)
        self._generator_moisture = NoiseGenerator(width, height, seed)
        self._data_biomes = self.generate_biomes()

    def elevation(self):
        """Return the elevation matrix only."""
        return self._generator_elevation.data()

    def moisture(self):
        """Return the moisture matrix only."""
        return self._generator_moisture.data()

    def biomes(self):
        """Return the biomes matrix only."""
        return self._data_biomes

    def generate_biomes(self):
        """Go trough eleavtion and moisture, and generate the biomes."""
        biome_matrix =\
            [[None for _ in range(self.width)] for _ in range(self.height)]

        # Elevation and moisture thresholds
        elevation_thresholds = [0.13, 0.3, 0.6, 0.8, 2.0]
        moisture_thresholds = [0.05, 0.1, 0.25, 0.4, 0.65, 2.0]

        # Biome interpretation matrix
        biome_interpretation = [[-1, -1, -1, -1, -1, -1],
                                [0, 1, 2, 2, 3, 3],
                                [4, 1, 1, 5, 5, 6],
                                [4, 4, 7, 7, 8, 8],
                                [9, 10, 11, 12, 12, 12]]

        for x in range(self.width):
            for y in range(self.height):
                for elv_index, elv in enumerate(elevation_thresholds):
                    if self._generator_elevation.get(x, y) < elv:
                        for mst_index, mst in enumerate(moisture_thresholds):
                            if self._generator_moisture.get(x, y) < mst:
                                biome_matrix[x][y] =\
                                    biome_interpretation[elv_index][mst_index]

        return biome_matrix

    def save(self, name='world'):
        """Store the world data as a pickel object."""
        with open(path.join(
                DirectoryPaths.SAVES.value, name + '.pkl'), 'w') as fp:
            pickel.dump(self, fp, protocol=pickel.HIGHEST_PROTOCOL)

    @staticmethod
    def load(name):
        """Load an existing save file."""
        with open(path.join(
                DirectoryPaths.SAVES.value, name + '.pkl'), 'r') as fp:
            return pickel.load(fp)


from stargateRL.world.exports import default_export_biomes

world_data = WorldData(seed=-1)
default_export_biomes(world_data.biomes())
