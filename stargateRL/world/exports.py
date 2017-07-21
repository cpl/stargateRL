"""A set of methods for exporting world data to visual data."""

from os import path

from PIL import Image

from stargateRL.engine.graphx import Colors
from stargateRL.paths import DirectoryPaths


def grayscale(map_data, file_name='map', tone=Colors.WHITE):
    """Store a BMP image of the map, grayscale. The tone can be changed."""
    image_data = []

    file_path = DirectoryPaths.EXPORTS
    file_name = file_name + '.bmp'

    for row in map_data:
        for val in row:
            image_data.append(int(val*nounce))

    img = Image.new('L', (len(map_data), len(map_data[0])))
    img.putdata(image_data)
    img.save(path.join(file_path, file_name))
