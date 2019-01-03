"""Main method for stargateRL."""
import pdb
import pyglet

from stargateRL.objects import widgets
from stargateRL.engine.screen import GameWindow
from stargateRL.engine.colors import ThemeColors
from stargateRL.world.genesis import WorldData
from stargateRL.world.exports import default_export_biomes, monochrome
from stargateRL.launcher.utils import load_config


# DEBUG
# TODO: Prepare settings for world generation
def test_exports(tt):
    """Test export methods."""
    print tt
    world_data = WorldData(seed=-1)
    monochrome(world_data.elevation(), 'elevation')
    monochrome(world_data.moisture(), 'moisture')
    default_export_biomes(world_data.biomes())


def main():
    """Create the game."""
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
                    ThemeColors.TEXT_DEFAULT,
                    ThemeColors.TEXT_ACTIVE,
                    ThemeColors.TEXT_SELECT,
                    ThemeColors.MENU),
            # Menu options (name, method, args)
            options=(
                ('Compile World', test_exports, [None]),
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
