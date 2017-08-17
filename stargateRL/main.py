"""Main method for stargateRL."""
import pdb
import pyglet

from stargateRL.objects import widgets
from stargateRL.engine.screen import GameWindow
from stargateRL.engine.colors import ThemeColors, ElevationColors
from stargateRL.world.genesis import WorldData
from stargateRL.world.exports import default_export_biomes, exactmatch
from stargateRL.launcher.utils import load_config
from stargateRL.debug import logger


def compile_world():
    """Start world creation."""
    world_data = WorldData('test_world', 1)
    for planet in world_data.planets:
        # monochrome(planet.moisture, planet.hash_name + '.moisture')
        exactmatch(planet.elevation, planet.hash_name + '.elevation',
                   values=[(0.10, ElevationColors.OCEAN),
                           (0.13, ElevationColors.BEACH),
                           (0.3, ElevationColors.PLAINS),
                           (0.6, ElevationColors.PLATEU),
                           (0.8, ElevationColors.HILLS),
                           (2.0, ElevationColors.MOUNTAINS)])

        default_export_biomes(planet.biomes, planet.hash_name + '.biomes')

    world_data.save()


def main():
    """Start the game."""
    logger.info('Started main program')
    pyglet.options['debug_gl'] = False

    CONFIG = load_config()
    window_config = CONFIG['window']

    window = GameWindow(window_config['width'],
                        window_config['height'],
                        fullscreen=window_config['fullscreen'],
                        resizable=window_config['resizable'],
                        style=window_config['style'],
                        vsync=CONFIG['graphics']['vsync'])

    # Configurate window
    window.set_mouse_visible(window_config['mouse'])
    window.set_icon(pyglet.resource.image(CONFIG['resources']['icon']))

    screen_background = widgets.FilledBoxWidget(
                            position=(0, 0),
                            dimensions=(window.x_tiles, window.y_tiles),
                            removable=False, tile_color=ThemeColors.MENU,
                            tile_id=219)

    # Create the screen border
    screen_border = widgets.BorderWidget(position=(0, 0),
                                         dimensions=(window.x_tiles,
                                                     window.y_tiles),
                                         removable=False,
                                         tile_color=ThemeColors.BORDER,
                                         tiles=(178, 178, 178, 178,
                                                35, 35, 35, 35))

    # Create the selection menu
    selection_menu =\
        widgets.SelectionMenuWidget(
            position=(window.x_tiles / 4 + 1, window.y_tiles / 2),
            dimensions=(window.x_tiles / 2, window.y_tiles / 4),
            # (TileColor(Border), TileColor(Menu), Default, Active, Selected)
            colors=(ThemeColors.BORDER,
                    ThemeColors.MENU,
                    ThemeColors.TEXT_DEFAULT,
                    ThemeColors.TEXT_ACTIVE,
                    ThemeColors.TEXT_SELECT),
            # Menu options (name, method, args)
            options=(
                ('Compile World', compile_world, []),
                ('Testing Area', pdb.set_trace, []),
                ('Saves/Worlds', None, []),
                ('Settings', None, []),
                ('Credits/About', None, []),
                ('Exit', pyglet.app.exit, [])))

    # Prepare widgets for rendering
    window.push_widget(screen_background)
    window.push_widget(screen_border)
    window.push_widget(selection_menu)

    pyglet.app.run()


if __name__ == '__main__':
    main()
