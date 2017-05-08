"""Terrain generation and more."""


from noise import snoise2 as noise2
import random
import math
from random import getrandbits


def noise(x, y, width, height):
    """Return noise between 0.0 and 1.0."""
    return noise2(x, y, repeatx=width, repeaty=height) / 2.0 + 0.5


def normalize(min_value, max_value, value):
    """Normalize the given value between 0.0 and 1.0."""
    return float(value - min_value) / (max_value + min_value)


def continent(elevation, center, edges, water, nx, ny):
    """Transform the terrain into continents."""
    distance = 2 * max(abs(nx), abs(ny))
    return (elevation + center) * (edges - 1.0 * math.pow(distance, water))


def generate_noise_map(width, height, scale, octaves, persistance, lacunarity,
                       terraces, exponent, seed=0):
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
    if terraces < 1:
        terraces = 1.0

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
            noise_map[x][y] = continent(noise_map[x][y], 0.05, 1.0, 1.5,
                                        float(x) / width - 0.5,
                                        float(y) / height - 0.5)
            noise_map[x][y] = math.pow(noise_map[x][y], exponent)
            if terraces != 1.0:
                noise_map[x][y] = round(noise_map[x][y] * terraces) / terraces

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

for i in range(5):
    my_seed = getrandbits(21)
    create_pgm(generate_noise_map(width=500, height=500, scale=250.0, octaves=8,
                                persistance=0.4, lacunarity=1.87, terraces=64.0,
                                exponent=4, seed=my_seed),
            'r{}x{}_scale{}_o{}_p{}_l{}_tr{}_exp{}_seed{}c.pgm'.format(500, 500,
                                                                        250.0, 8,
                                                                        0.4, 1.87,
                                                                        64.0, 4,
                                                                        my_seed))
