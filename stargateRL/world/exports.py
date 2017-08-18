"""A set of methods for exporting world data to visual data."""

from os import path

from PIL import Image

from stargateRL.engine.colors import DefaultColors
from stargateRL.engine.colors import BiomeColors
from stargateRL.paths import DirectoryPaths
from stargateRL.world.utils import Biomes
from stargateRL.debug import logger


def monochrome(map_data, file_name='map_monochrome', tone=DefaultColors.WHITE):
    """Store a BMP image of the map, monochrome. The tone can be changed."""
    image_data = []
    logger.info('Exporting monochrome bmp: %s', file_name)

    file_path = DirectoryPaths.EXPORTS.value
    file_name = file_name + '.bmp'

    color = tone.value.rgb
    for row in map_data:
        for val in row:
            image_data.append((int(color[0] * val),
                               int(color[1] * val),
                               int(color[2] * val)))

    img = Image.new('RGB', (len(map_data), len(map_data[0])))
    img.putdata(image_data)
    img.save(path.join(file_path, file_name))


def exactmatch(map_data, file_name='map_exactmatch', values=[]):
    """Store a BMP image of the map, using the given value-color pairs."""
    image_data = []
    logger.info('Exporting exactmatch bmp: %s', file_name)

    file_path = DirectoryPaths.EXPORTS.value
    file_name = file_name + '.bmp'

    for row in map_data:
        for val in row:
            for value_color in values:
                if val <= value_color[0]:
                    image_data.append(value_color[1].value.rgb)
                    break

    img = Image.new('RGB', (len(map_data), len(map_data[0])))
    img.putdata(image_data)
    img.save(path.join(file_path, file_name))


def default_export_biomes(map_data, file_name='biomes'):
    """Store a BMP image of the biomes, using the default value-color pairs."""
    image_data = []
    logger.info('Exporting biomes bmp: %s', file_name)

    file_path = DirectoryPaths.EXPORTS.value
    file_name = file_name + '.bmp'

    for row in map_data:
        for val in row:
            image_data.append(BiomeColors[Biomes(val).name].value.rgb)

    img = Image.new('RGB', (len(map_data), len(map_data[0])))
    img.putdata(image_data)
    img.save(path.join(file_path, file_name))
