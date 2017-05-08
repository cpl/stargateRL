"""Terrain generation and more."""


from noise import snoise2
import random
import math


freq = 1.20
width = 500
height = 200
seed = random.getrandbits(21)


def noise(nx, ny):
    """Noise from 0.0 to 1.0."""
    return snoise2(nx, ny, base=seed) / 2 + 0.5


def a_noise(nx, ny, exp, *en):
    """Advanced noise generation."""
    final = 0.0
    for i, e in enumerate(en):
        final += e * noise(math.pow(2, i) * nx, math.pow(2, i) * ny)
    final = final / sum(en)
    return math.pow(final, exp)


elevation = [[0 for y in range(height)] for x in range(width)]
for y in range(height):
    for x in range(width):
        nx = float(x)/width - 0.5
        ny = float(y)/height - 0.5
        elevation[x][y] = '#' if a_noise(nx, ny, 1.0, 1.0, 0.58, 0.24, 0.19, 0.0, 0.08) > 0.5 else '.'

for r in elevation:
    s = str(r).replace(' ', '')
    s = s.replace(',', '')
    s = s.replace('\'', '')
    print s
