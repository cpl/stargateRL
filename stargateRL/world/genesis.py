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

    def __init__(self, width, height, seed):
        """Construct the terrain."""
        self._width = width
        self._height = height
        self._noise_map = [[None for x in range(width)] for y in range(height)]
        self._seed = seed

    def get(self, x, y):
        """Return the noise value at x, y."""
        return self._noise_map[x][y]

    def set(self, x, y, value):
        """Set the noise value at x, y."""
        self._noise_map[x][y] = value

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
            'map_seed{!s}_size{!s}x{!s}_scale{!s}_octaves{!s}_exponent{!s}\
_per{!s}_lac{!s}_terraces{!s}_c{!s}_offset{!s}_m{!s}_gray.bmp'

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

                    # Update parameters for each octave
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

    def __init__(self, seed=0, width=500, height=500,
                 elevation_noise_map=None, moisture_noise_map=None):
        """Construct the biomes using elevation and moisture."""
        seed = random.getrandbits(21) if seed == -1 else seed
        random.seed(seed)

        if elevation_noise_map is None:
            elevation_noise_map = NoiseGenerator(width, height, seed)
        if moisture_noise_map is None:
            moisture_noise_map = NoiseGenerator(width, height, seed)

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

    def export_elevation(self):
        """Export the elevation color map."""
        pixels = []
        file_path =\
            'map_seed{!s}_size{!s}x{!s}_scale{!s}_octaves{!s}_exponent{!s}\
_per{!s}_lac{!s}_terraces{!s}_c{!s}_offset{!s}_m{!s}_elevation_color.bmp'

        for x in range(self.width):
            for y in range(self.height):
                val = self._elevation_map.get(x, y)
                # LOW LEVEL
                if val <= 0.08:
                    pixels.append((22, 41, 85))     # deep water
                elif val <= 0.13:
                    pixels.append((46, 65, 114))    # water
                elif val < 0.15:
                    pixels.append((255, 206, 107))  # sand
                # MEDIUM LEVEL
                elif val < 0.3:
                    pixels.append((61, 205, 61))    # grass
                elif val < 0.6:
                    pixels.append((59, 111, 59))    # dark grass
                # HIGH LEVEL
                elif val < 0.8:
                    pixels.append((64, 55, 43))     # hilly
                # VERY HIGH LEVEL
                else:
                    pixels.append((255, 255, 255))  # snow mountain

        image = Image.new('RGB', (self.width, self.height))
        image.putdata(pixels)
        image.save(file_path.format(*self._elevation_map._settings))

    def export_moisture(self):
        """Export moisture color map."""
        pixels = []
        file_path =\
            'map_seed{!s}_size{!s}x{!s}_scale{!s}_octaves{!s}_exponent{!s}\
_per{!s}_lac{!s}_terraces{!s}_c{!s}_offset{!s}_m{!s}_moisture_color.bmp'

        for x in range(self.width):
            for y in range(self.height):
                val = self._moisture_map.get(x, y)
                if self._elevation_map.get(x, y) < 0.15:
                    pixels.append((0, 0, 0))  # ocean/sea level
                elif val < 0.05:
                    pixels.append((162, 178, 190))    # very dry
                elif val < 0.1:
                    pixels.append((71, 107, 132))     # medium dry
                elif val < 0.25:
                    pixels.append((146, 188, 94))     # little dry
                elif val < 0.4:
                    pixels.append((115, 162, 57))     # little wet
                elif val < 0.65:
                    pixels.append((255, 152, 76))     # medium wet
                else:
                    pixels.append((233, 81, 37))      # very wet

        image = Image.new('RGB', (self.width, self.height))
        image.putdata(pixels)
        image.save(file_path.format(*self._moisture_map._settings))

    def export_biomes(self):
        """Export biome color map."""
        pixels = []
        file_path =\
            'map_seed{!s}_size{!s}x{!s}_scale{!s}_octaves{!s}_exponent{!s}\
_per{!s}_lac{!s}_terraces{!s}_c{!s}_offset{!s}_m{!s}_biomes_color.bmp'

        for x in range(self.width):
            for y in range(self.height):
                val = self._biome_map[x][y]
                if val == -1:
                    pixels.append((0, 0, 0))
                elif val == 0:
                    pixels.append((255, 223, 190))
                elif val == 1:
                    pixels.append((111, 177, 123))
                elif val == 2:
                    pixels.append((166, 207, 130))
                elif val == 3:
                    pixels.append((105, 159, 56))
                elif val == 4:
                    pixels.append((231, 190, 146))
                elif val == 5:
                    pixels.append((206, 168, 104))
                elif val == 6:
                    pixels.append((161, 193, 97))
                elif val == 7:
                    pixels.append((109, 160, 57))
                elif val == 8:
                    pixels.append((189, 184, 152))
                elif val == 9:
                    pixels.append((137, 132, 122))
                elif val == 10:
                    pixels.append((110, 110, 132))
                elif val == 11:
                    pixels.append((62, 62, 75))
                elif val == 12:
                    pixels.append((255, 255, 255))
                else:
                    raise Exception('Unknow value {!s}'.format(val))

        image = Image.new('RGB', (self.width, self.height))
        image.putdata(pixels)
        image.save(file_path.format(*self._elevation_map._settings))

    def generate_biomes(self):
        """Go trough eleavtion and moisture, and generate the biomes."""
        for x in range(self.width):
            for y in range(self.height):
                # Add moisture to water areas
                elevation_value = self._elevation_map.get(x, y)
                moisture_value = self._moisture_map.get(x, y)

                # Lowest elevation is ignored, moisture is set to max
                if elevation_value < 0.15:
                    self._moisture_map.set(x, y, 1.0)
                    self._biome_map[x][y] = -1
                # Low elevation
                elif elevation_value < 0.3:
                    if moisture_value < 0.05:
                        self._biome_map[x][y] = 0
                    elif moisture_value < 0.1:
                        self._biome_map[x][y] = 1
                    elif moisture_value < 0.25:
                        self._biome_map[x][y] = 2
                    elif moisture_value < 0.4:
                        self._biome_map[x][y] = 2
                    elif moisture_value < 0.65:
                        self._biome_map[x][y] = 3
                    else:
                        self._biome_map[x][y] = 3
                # Medium elevation
                elif elevation_value < 0.6:
                    if moisture_value < 0.05:
                        self._biome_map[x][y] = 4
                    elif moisture_value < 0.1:
                        self._biome_map[x][y] = 1
                    elif moisture_value < 0.25:
                        self._biome_map[x][y] = 1
                    elif moisture_value < 0.4:
                        self._biome_map[x][y] = 5
                    elif moisture_value < 0.65:
                        self._biome_map[x][y] = 5
                    else:
                        self._biome_map[x][y] = 6
                # High elevation
                elif elevation_value < 0.8:
                    if moisture_value < 0.05:
                        self._biome_map[x][y] = 4
                    elif moisture_value < 0.1:
                        self._biome_map[x][y] = 4
                    elif moisture_value < 0.25:
                        self._biome_map[x][y] = 7
                    elif moisture_value < 0.4:
                        self._biome_map[x][y] = 7
                    elif moisture_value < 0.65:
                        self._biome_map[x][y] = 8
                    else:
                        self._biome_map[x][y] = 8
                # Mountains
                else:
                    if moisture_value < 0.05:
                        self._biome_map[x][y] = 9
                    elif moisture_value < 0.1:
                        self._biome_map[x][y] = 10
                    elif moisture_value < 0.25:
                        self._biome_map[x][y] = 11
                    elif moisture_value < 0.4:
                        self._biome_map[x][y] = 12
                    elif moisture_value < 0.65:
                        self._biome_map[x][y] = 12
                    else:
                        self._biome_map[x][y] = 12


world_data = WorldData(seed=-1)
world_data._elevation_map.generate_noise_map(150.0, 5, 4, 0.5, 3.0)
world_data._moisture_map.generate_noise_map(150.0, 2, 3, 0.5, 2.0,
                                            continent_filter=False)
world_data.generate_biomes()

world_data.export_elevation()
world_data.export_moisture()
world_data.export_biomes()
