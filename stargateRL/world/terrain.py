"""Terrain generation and more."""


from noise import pnoise2 as noise2
import random
from random import getrandbits


def noise(x, y, width, height):
    """Return noise between 0.0 and 1.0."""
    return noise2(x, y, repeatx=width, repeaty=height) / 2.0 + 0.5


def normalize(min_value, max_value, value):
    """Normalize the given value between 0.0 and 1.0."""
    return float(value - min_value) / (max_value + min_value)


def generate_noise_map(width, height, scale, octaves, persistance, lacunarity,
                       seed=0):
    """Generate a 2D map of noise."""
    random.seed(seed)

    if scale <= 0:
        scale = 0.0001
    if width < 1:
        width = 1
    if height < 1:
        height = 1
    if lacunarity < 1:
        lacunarity = 1
    if octaves < 0:
        octaves = 0

    noise_map = [[0 for y in range(height)] for x in range(width)]

    max_noise = 0
    min_noise = 0

    octaves_offsets = []
    for o in range(octaves):
        offset_x = random.randint(-100000, 100000)
        offset_y = random.randint(-100000, 100000)
        octaves_offsets.append((offset_x, offset_y))

    for y in range(height):
        for x in range(width):

            amplitude = 1.0
            frequency = 1.0
            noise_height = 0.0

            for o in range(octaves):
                sample_x = float(x - width / 2) / scale * \
                    frequency + octaves_offsets[o][0]
                sample_y = float(y - height / 2) / scale * \
                    frequency + octaves_offsets[o][1]

                noise_value = noise(sample_x, sample_y, width, height)
                noise_height += noise_value * amplitude

                amplitude *= persistance
                frequency *= lacunarity

            if noise_height > max_noise:
                max_noise = noise_height
            if noise_height < min_noise:
                min_noise = noise_height

            noise_map[x][y] = noise_height

    for y in range(height):
        for x in range(width):
            noise_map[x][y] = normalize(min_noise, max_noise, noise_map[x][y])
            import math
            noise_map[x][y] = math.pow(noise_map[x][y], 7)

    return noise_map


def create_pgm(noise_map, file_name):
    """Create PGM heightmap."""
    with open(file_name, 'w') as pmg:
        pmg.write('P2\n')
        pmg.write('{} {}\n'.format(len(noise_map), len(noise_map[0])))
        pmg.write('255\n')
        for row in noise_map:
            for noise in row:
                pmg.write('{}\n'.format(int(noise * 255.0)))


# my_seed = getrandbits(21)
my_seed = 21
print my_seed
create_pgm(generate_noise_map(width=1024, height=1024, scale=250.0, octaves=4,
                              persistance=0.4, lacunarity=1.87, seed=my_seed),
           '{}.pgm'.format(my_seed))
