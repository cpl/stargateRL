"""Graphical test for sprites."""

import pyglet
import random
import cProfile

from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import TileColor
from stargateRL.utils import CONFIG, GX_TILESETS

pyglet.options['debug_gl'] = False
pyglet.clock.set_fps_limit(60)

# Create the game window
window_config = CONFIG['graphics']['window']

window = GameWindow(window_config['width'],
                    window_config['height'],
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

sprites = []
batch = window._testing_batch
for _ in range(1000):
    sprites.append(pyglet.sprite.Sprite(
        GX_TILESETS['MAIN'].get_colored(240, TileColor('blue', 'red')),
        random.randint(0, 1440), random.randint(0, 900), batch=batch))


@window.event
def on_key_press(symbol, modifers):
    """DOCSTRING."""
    if symbol == pyglet.window.key.UP:
        for sprite in sprites:
            sprite.set_position(sprite.x, sprite.y+5)


cProfile.run('pyglet.app.run()')
