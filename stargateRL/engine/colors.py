"""Collection of colors."""

from enum import Enum

from stargateRL.engine.graphx import Color, TileColor


class DefaultColors(Enum):
    """A collection of constant colors."""

    BLACK = Color(0, 0, 0, 255)
    WHITE = Color(255, 255, 255, 255)

    BLUE = Color(0, 0, 255, 255)
    GREEN = Color(0, 255, 0, 255)
    RED = Color(255, 0, 0, 255)

    TRANSPARENT = Color(0, 0, 0, 0)

    TILE = TileColor(WHITE, BLACK)

    # TODO: Move these two colors to a diffrent Enum
    # BORDER = Color(70, 76, 84, 255)
    GOLD = Color(245, 211, 115, 255)


class ThemeColors(Enum):
    """Colors used for the default main menu."""

    TEXT_DEFAULT = Color(43, 43, 42, 255)
    TEXT_ACTIVE = Color(238, 175, 98, 255)
    TEXT_SELECT = Color(128, 94, 53, 255)

    BACKGROUND = Color(34, 40, 51, 255)
    FOREGROUND = Color(217, 215, 206, 255)
    MENU = TileColor(BACKGROUND, FOREGROUND)

    BORDER_BACKGROUND = Color(71, 75, 84, 255)
    BORDER_FOREGROUND = Color(40, 46, 56, 255)
    BORDER = TileColor(BORDER_BACKGROUND, BORDER_FOREGROUND)


class BiomeColors(Enum):
    """Colors used by the default biome image export."""

    OCEAN = Color(14, 54, 93, 255)
    SEA = Color(53, 96, 137, 255)
    LAKE = Color(32, 75, 117, 255)
    RIVER = Color(32, 75, 117, 255)

    TROPICAL_RAIN_FOREST = Color(150, 196, 66, 255)
    TROPICAL_SEASONAL_FOREST = Color(121, 168, 36, 255)
    GRASSLAND = Color(50, 148, 98, 255)
    SUBTROPICAL_DESERT = Color(211, 202, 71, 255)
    TEMPERATE_RAIN_FOREST = Color(155, 197, 66, 255)
    TEMPERATE_DECIDUOUS_FOREST = Color(28, 130, 69, 255)
    TEMPERATE_DESERT = Color(211, 172, 71, 255)
    TAIGA = Color(139, 161, 99, 255)
    SHRUBLAND = Color(114, 91, 41, 255)
    SNOW = Color(218, 215, 200, 255)
    TUNDRA = Color(131, 127, 111, 255)
    BARE = Color(84, 81, 68, 255)
    SCORCHED = Color(58, 54, 35, 255)


class ElevationColors(Enum):
    """Colors used by the default elevation image export."""

    pass


class MoistureColors(Enum):
    """Colors used by the default moisture image export."""

    pass
