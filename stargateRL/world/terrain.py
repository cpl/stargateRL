"""Terrain generation and more."""


from noise import pnoise2
import random


with open('test.pmg', 'w') as pmg_file:
    pmg_file.write('P2\n')
    pmg_file.write('256 256\n')
    pmg_file.write('255\n')

    freq = 0.27
    for y in range(256):
        for x in range(256):
            print pnoise2(x * freq, y * freq, 2, base=random.getrandbits(21)) / 2 + 0.5
