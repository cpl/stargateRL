"""Terain generators."""


from __future__ import print_function

import json
import math
import time
import random
import hashlib
import cPickle as pickel
from os import path

from stargateRL.world.utils import normalize, noise, continent, Profiles
from stargateRL.paths import DirectoryPaths
from stargateRL.debug import logger


class NoiseGenerator(object):
    """Construct the terrain heightmap."""

    def __init__(self, width, height, settings=None):
        """Construct the terrain."""
        self._width = width
        self._height = height

        logger.debug('Created new NoiseGenerator %ix%i', width, height)

        # Generate empty noise map
        self._noise_map = [[None for _ in range(width)] for _ in range(height)]

        # If no settings are given, use defaults
        if settings is None:
            self._settings = Profiles.DEFAULT
        else:
            self._settings = settings

        logger.debug('NoiseGenerator settings: %s', settings)

        self.generate_noise_map()

    def get(self, x, y):
        """Return the noise value at x, y."""
        return self._noise_map[x][y]

    def set(self, x, y, value):
        """Set the noise value at x, y."""
        self._noise_map[x][y] = value

    @property
    def settings(self):
        """Return the settings used in generation."""
        return self._settings

    @property
    def data(self):
        """Return the noise map data."""
        return self._noise_map

    def generate_noise_map(self):
        """Fill the elevation matrix with noise."""
        # Initial min/max values
        max_noise = 0.0
        min_noise = 0.0

        logger.debug('Setup noise generator')

        # Apply offset to the noise map
        octaves_offsets = []
        for _ in range(self._settings['octaves']):
            offset_x = random.randint(-100000, 100000) + \
                self._settings['offset'][0]
            offset_y = random.randint(-100000, 100000) + \
                self._settings['offset'][1]
            octaves_offsets.append((offset_x, offset_y))
        logger.debug('Generated octaves offset')

        # Go trough each position on the map, and generate the noise
        _units = self._width * self._height
        logger.debug('Start noise generation: %d units', _units)
        _t0 = time.time()
        for y in range(self._height):
            for x in range(self._width):
                # Initialize the noise parameters
                amplitude = 1.0
                frequency = 1.0
                noise_height = 0.0

                # Adjust parameters
                scale = self._settings['scale'] * (self._width / 3.3)
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
        _dt = time.time() - _t0
        logger.debug(
            'Finished noise gen in %fs, %fu/s', _dt, _units / _dt)

        # Prepare for another normalization
        mnoise = None
        xnoise = None
        logger.debug('Start noise normalization and filter')
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
        logger.debug('Applying final normalization to noise')
        for y in range(self._height):
            for x in range(self._width):
                self._noise_map[x][y] = normalize(self._noise_map[x][y],
                                                  mnoise, xnoise)
        logger.debug('Finished noise generation')


class PlanetGenerator(object):
    """Generate planet data such as elevation, moisture and biomes."""

    MIN = 100
    MAX = 500

    def __init__(self, settings=None):
        """Construct the biomes using elevation and moisture."""
        self.width = random.randint(PlanetGenerator.MIN, PlanetGenerator.MAX)
        self.height = self.width

        logger.info(
            'Created PlanetGenerator %dx%d', self.width, self.height)

        # Generate map data using noise
        logger.debug('Creating elevation')
        self._generator_elevation = NoiseGenerator(self.width,
                                                   self.height, settings)
        logger.debug('Creating moisture')
        self._generator_moisture = NoiseGenerator(self.width,
                                                  self.height, settings)
        logger.debug('Creating biomes')
        self._data_biomes = self.generate_biomes()

        logger.debug('Computing hash of random state')
        self._hash = hashlib.sha256(str(random.getstate())).hexdigest()

    @property
    def elevation(self):
        """Return the elevation matrix only."""
        return self._generator_elevation.data

    @property
    def moisture(self):
        """Return the moisture matrix only."""
        return self._generator_moisture.data

    @property
    def biomes(self):
        """Return the biomes matrix only."""
        return self._data_biomes

    @property
    def hash_name(self):
        """Return the hash of the planet after generation."""
        return self._hash

    def generate_biomes(self):
        """Go trough eleavtion and moisture, and generate the biomes."""
        # Elevation and moisture thresholds
        elvt = [0.10, 0.13, 0.3, 0.6, 0.8, 2.0]
        mstt = [0.05, 0.1, 0.25, 0.4, 0.65, 2.0]

        # Biome interpretation matrix
        binter = [[0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1],
                  [7, 6, 5, 5, 4, 4],
                  [10, 6, 6, 9, 9, 8],
                  [10, 10, 12, 12, 11, 11],
                  [16, 15, 14, 13, 13, 13]]

        biome_matrix =\
            [[None for _ in range(self.width)] for _ in range(self.height)]

        logger.debug('Starting biome generation')
        _t0 = time.time()
        for x in range(self.width):
            for y in range(self.height):
                elv = self._generator_elevation.get(x, y)
                for elvi, elvc in enumerate(elvt):
                    if elv < elvc:
                        mst = self._generator_moisture.get(x, y)
                        for msti, mstc in enumerate(mstt):
                            if mst < mstc:
                                biome_matrix[x][y] = binter[elvi][msti]
                                break
                            else:
                                continue
                        break
        _dt = time.time() - _t0
        logger.debug('Finished generating biomes in %fs', _dt)

        return biome_matrix


class WorldData(object):
    """Construct and store all world data."""

    def __init__(self, name, world_count, config=Profiles.DEFAULT):
        """Construct the world data using world generator."""
        config = config.value

        logger.debug('Created WorldData with %i worlds', world_count)
        logger.debug('WorldData config: %s', config)

        # Assign random seed if needed (-1 --> random seed)
        if config['seed'] == -1:
            config['seed'] = random.getrandbits(21)
        random.seed(config['seed'])

        logger.debug('WorldData seed: %s', config['seed'])

        self._name = name
        self._config = config

        self._planets = []
        logger.debug('Starting planet generation')
        _t0 = time.time()
        for index in xrange(world_count):
            self._planets.append(PlanetGenerator(config['settings']))
        _dt = time.time() - _t0
        logger.debug(
            'Finished generating %i worlds in %fs, %fw/s',
            world_count, _dt, world_count / _dt)

    @property
    def seed(self):
        """Return the seed of the world."""
        return self._config['seed']

    @property
    def name(self):
        """Return the name of the world."""
        return self._name

    @property
    def planets(self):
        """Return the planets."""
        return self._planets

    def save(self):
        """Store the world data as a pickel object."""
        logger.info('Saving WorldData of %s', self._name)
        file_name = path.join(DirectoryPaths.SAVES.value, self._name)

        # Check for existing save file, and create a new one
        if path.isfile(file_name + '.pkl'):
            file_name = file_name + '(1)'
        _count = 1
        while path.isfile(file_name + '.pkl'):
            file_name = file_name.replace('({})'.format(_count),
                                          '({})'.format(_count + 1))
            _count += 1
        logger.debug('Saved file as %s', file_name)

        # Write the save file and WorldData profile
        with open(file_name + '.pkl', 'w') as fp:
            pickel.dump(self, fp, protocol=pickel.HIGHEST_PROTOCOL)
        with open(file_name + '.config' + '.json', 'w') as fp:
            json.dump(self._config, fp, indent=4)
        logger.info('Finished saving WorldData of %s', self._name)

    @staticmethod
    def load(name):
        """Load an existing save file."""
        logger.info('Loading WorldData of %s', name)
        with open(path.join(
                DirectoryPaths.SAVES.value, name + '.pkl'), 'r') as fp:
            return pickel.load(fp)
