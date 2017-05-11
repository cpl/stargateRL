"""Terain generators."""


import math
import random
from noise import snoise2, pnoise2
from PIL import Image


def noise(x, y, width, height, mode='simplex'):
    """Return noise between 0.0 and 1.0."""
    if mode == 'simplex':
        return snoise2(x, y, repeatx=width, repeaty=height) / 2.0 + 0.5
    elif mode == 'perlin':
        return pnoise2(x, y, repeatx=width, repeaty=height) / 2.0 + 0.5
    else:
        raise Exception('Please provide as mode=[simplex|perlin]')


def normalize(value, min_value, max_value):
    """Normalize the given value between 0.0 and 1.0."""
    return float(value - min_value) / float(max_value + min_value)


def continent(elevation, push, edges, strenght, nx, ny):
    """Transform the terrain into continents."""
    distance = 2 * max(abs(nx), abs(ny))
    return (elevation + push) * (edges - 1.0 * math.pow(distance, strenght))


class NoiseGenerator(object):
    """Construct the terrain heightmap."""

    def __init__(self, width, height, seed=0):
        """Construct the terrain."""
        self._width = width
        self._height = height
        self._noise_map = [[None for x in range(width)] for y in range(height)]

        # If the seed is -1, use a random seed, if the seed is 0 use seed 0
        self._seed = random.getrandbits(21) if seed == -1 else seed
        # Assign the seed to the RNG
        random.seed(self._seed)

    def generate_special(self, special='megarandom', **kargs):
        """Special custom settings for elevation generation."""
        if special == 'megarandom':
            self.generate_noise_map(random.uniform(10.0, 1000.0),
                                    random.randint(1, 10),
                                    random.randint(2, 14),
                                    random.uniform(0.1, 1.0),
                                    random.uniform(1.0, 10.0),
                                    random.randint(1, 128))

    def export_grayscale(self):
        """Store a BMP image of the map, with some naive colors."""
        graymap = []
        file_path =\
            'gsn_seed{!s}_size{!s}x{!s}_scale{!s}_octaves{!s}_exponent{!s}\
_per{!s}_lac{!s}_terraces{!s}_c{!s}_offset{!s}_m{!s}.bmp'

        for row in self._noise_map:
            for val in row:
                graymap.append(int(val*255))

        gimg = Image.new('L', (self._width, self._height))
        gimg.putdata(graymap)
        gimg.save(file_path.format(*self._settings))

    def generate_noise_map(self, scale, octaves, exponent, persistance,
                           lacunarity, terraces=1.0, continent_filter=True,
                           offset=(0, 0), mode='simplex'):
        """Fill the elevation matrix with noise."""
        max_noise = 0.0
        min_noise = 0.0

        self._settings = (self._seed, self._width, self._height, scale,
                          octaves, exponent, persistance, lacunarity, terraces,
                          continent_filter, offset, mode)

        # Apply offset to the noise map
        octaves_offsets = []
        for o in range(octaves):
            offset_x = random.randint(-100000, 100000) + offset[0]
            offset_y = random.randint(-100000, 100000) + offset[1]
            octaves_offsets.append((offset_x, offset_y))

        # Go trough each position on the map, and generate the noise
        for y in range(self._height):
            for x in range(self._width):

                # Initialize the noise parameters
                amplitude = 1.0
                frequency = 1.0
                noise_height = 0.0

                # Adjust parameters
                for o in range(octaves):
                    sample_x = float(x - self._width / 2) / scale * \
                        frequency + octaves_offsets[o][0]
                    sample_y = float(y - self._height / 2) / scale * \
                        frequency + octaves_offsets[o][1]

                    # Obtain noise from the noise library
                    noise_value = noise(sample_x, sample_y,
                                        self._width, self._height, mode)

                    noise_height += noise_value * amplitude

                    # Update parameters on each octave pass
                    amplitude *= persistance
                    frequency *= lacunarity

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
                noise_height = math.pow(noise_height, exponent)

                # Apply continental filter
                if continent_filter:
                    noise_height = continent(noise_height, 0.0, 1.0, 5.0,
                                             float(x) / self._width - 0.5,
                                             float(y) / self._height - 0.5)

                # Check if terraces were enabled and generate terraces
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

    def __init__(self, elevation_noise_map, moisture_noise_map, **options):
        """Construct the biomes using elevation and moisture."""
        self._elevation_map = elevation_noise_map
        self._moisture_map = moisture_noise_map

        # Check width and height to match
        if elevation_noise_map._width == moisture_noise_map._width:
            self.width = elevation_noise_map._width
        else:
            raise Exception('Elevation and moisture maps width don\'t match.')
        if elevation_noise_map._height == moisture_noise_map._height:
            self.height = elevation_noise_map._height
        else:
            raise Exception('Elevation and moisture maps height don\'t match.')

        self._biome_map = [[None for x in range(
            self.width)] for y in range(self.width)]

        self.elevation_range = options.get(
            'elevation_range', self.elevation_range)
        self.moisture_range = options.get(
            'moisture_range', self.moisture_range)

    def generate_biomes(self, biomes_matrix):
        """Go trough eleavtion and moisture, and generate the biomes."""
        for x in range(self.width):
            for y in range(self.height):
                print self._elevation_map[x][y], self._moisture_map[x][y]

                if self._elevation_map[x][y] < self.water_line:
                    self._moisture_map[x][y] = 1.0


# nm = NoiseGenerator(500, 500, -1)
# nm.generate_noise_map(150.0, 4, 5, 0.5, 3.0)
# nm.export_grayscale()

"""
EL
0.15--------0.30--------0.60--------0.80--------1.00

MO
0.00--------0.10--------0.20--------0.40--------0.60--------0.90--------1.00
"""
