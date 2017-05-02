"""Graphical resource manager."""

import pyglet
from os import path

from pyglet.image import ImageGrid
from pyglet.resource import image

pyglet.resource.path = [(path.abspath(path.join('bin')))]


class Color(object):
    """A representation of a color. RGBA."""

    def __init__(self, r, g, b, a):
        """Create a color."""
        self.color = (r, g, b, a)

    def __call__(self):
        """Return the color only."""
        colorString = ''
        for atr in self.color:
            colorString += chr(atr)
        return colorString


COLORS = {'black': Color(0, 0, 0, 255), 'white': Color(255, 255, 255, 255),
          'blue': Color(0, 0, 255, 255), 'red': Color(255, 0, 0, 255),
          'green': Color(0, 255, 0, 255), 'transparent': Color(0, 0, 0, 0),
          'border': Color(70, 76, 84, 255)}


class GxTileset(object):
    """A image grid composing the Tileset resource."""

    def __init__(self, resourcePath, tileSize):
        """Construct the tileset manager."""
        self.sourceImage = image(resourcePath)

        self.tileSize = tileSize
        self.xTilesCount = self.sourceImage.width/tileSize
        self.yTilesCount = self.sourceImage.height/tileSize

        self.tilesetGrid = ImageGrid(self.sourceImage,
                                     self.xTilesCount,
                                     self.yTilesCount)

    def get(self, tileId):
        """Return a Image from the ImageGrid of the tileset."""
        return self.tilesetGrid[tileId]

    def getByPosition(self, x, y):
        """Return the Image from x, y inside ImageGrid."""
        return self.tilesetGrid[x+y*self.yTilesCount]

    def getColored(self, tileId, background, foreground):
        """Return a tile with the given colors."""
        image = self.get(tileId)
        imageData = image.image_data.get_data('RGBA', image.width*4)
        imagePixels = [imageData[p:p+4] for p in range(0, len(imageData), 4)]

        imageBackground = [p for p in range(len(imagePixels))
                           if imagePixels[p] == COLORS['black']()]
        imageForeground = [p for p in range(len(imagePixels))
                           if imagePixels[p] == COLORS['white']()]

        for pixel in imageBackground:
            imagePixels[pixel] = background()
        for pixel in imageForeground:
            imagePixels[pixel] = foreground()

        combinedPixels = b''
        for pixel in imagePixels:
            combinedPixels += pixel

        return pyglet.image.ImageData(image.width, image.height,
                                      'RGBA', combinedPixels)
