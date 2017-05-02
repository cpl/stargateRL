"""Main method for stargateRL."""

import pyglet
import engine
import mapset

import json


def run():
    """Run stargateRL."""
    # Load config file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Create the game window
    screen_config = config['graphics']['screen']
    window = engine.render.GameWindow(screen_config['width'],
                                      screen_config['height'],
                                      resizable=screen_config['resizable'],
                                      fullscreen=screen_config['fullscreen'],
                                      style=screen_config['style'])

    window.widgets['border'] = (engine.widgets.BorderWidget(window.width,
                                                            window.height,
                                                            16))

    # Run the pyglet app
    pyglet.app.run()


if __name__ == '__main__':
    run()
