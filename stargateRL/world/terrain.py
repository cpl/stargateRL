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


class HeightMap(object):
    """Construct the terrain heightmap."""

    def __init__(self, width, height, seed=0):
        """Construct the terrain."""
        self._width = width
        self._height = height
        self._elevation = [[None for x in range(width)] for y in range(height)]

        # If the seed is -1, use a random seed, if the seed is 0 use seed 0
        self._seed = random.getrandbits(21) if seed == -1 else seed
        # Assign the seed to the RNG
        random.seed(self._seed)

    def generate_special(self, special='megarandom', **kargs):
        """Special custom settings for elevation generation."""
        if special == 'megarandom':
            self.generate_elevation(random.uniform(10.0, 1000.0),
                                    random.randint(1, 10),
                                    random.randint(2, 14),
                                    random.uniform(0.1, 1.0),
                                    random.uniform(1.0, 10.0),
                                    random.randint(1, 128))

    def save_image(self, file_path):
        """Store a BMP image of the map, with some naive colors."""
        pixels = []
        graymap = []
        for row in self._elevation:
            for val in row:
                graymap.append((int(255*val), int(255*val), int(255*val)))
                if val <= 0.08:
                    pixels.append((22, 41, 85))  # deep water
                elif val <= 0.13:
                    pixels.append((46, 65, 114))  # water
                elif val < 0.15:
                    pixels.append((255, 206, 107))  # sand
                elif val < 0.3:
                    pixels.append((61, 205, 61))  # grass
                elif val < 0.6:
                    pixels.append((59, 111, 59))  # dark grass
                elif val < 0.8:
                    pixels.append((64, 55, 43))  # hilly
                elif val > 0.99:
                    pixels.append((255, 0, 255))  # debug magenta
                else:
                    pixels.append((255, 255, 255))

        blank_image = Image.new('RGB', (self._width, self._height))
        gimg = Image.new('RGB', (self._width, self._height))
        gimg.putdata(graymap)
        gimg.save('{}d_{}.bmp'.format(self._seed, file_path))
        blank_image.putdata(pixels)
        blank_image.save('{}g_{}.bmp'.format(self._seed, file_path))

    def generate_elevation(self, scale, octaves, exponent, persistance,
                           lacunarity, terraces=1.0, offset=(0, 0),
                           mode='simplex'):
        """Fill the elevation matrix with noise."""
        max_noise = 0.0
        min_noise = 0.0

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

                self._elevation[x][y] = noise_height

        # Prepare for another normalization
        mnoise = None
        xnoise = None
        for y in range(self._height):
            for x in range(self._width):
                # Normalize heightmap values between 0.0 and 1.0
                noise_height = normalize(self._elevation[x][y],
                                         min_noise, max_noise)

                # Apply exponential filter to clear land mass
                noise_height = math.pow(noise_height, exponent)

                # Apply continental filter
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

                self._elevation[x][y] = noise_height

        # Apply final changes
        for y in range(self._height):
            for x in range(self._width):
                self._elevation[x][y] = normalize(self._elevation[x][y],
                                                  mnoise, xnoise)


test_hm = HeightMap(500, 500, -1)
# test_hm.generate_elevation(150.0, 5, 4, 0.5, 3.0)
# test_hm.generate_special()
test_hm.save_image('testing')
