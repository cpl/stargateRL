"""Main method for stargateRL."""
import pyglet

from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import TileColor
from stargateRL.engine import widgets
from stargateRL.utils import CONFIG

# Create the game window
window_config = CONFIG['graphics']['window']

window = GameWindow(window_config['width'],
                    window_config['height'],
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

# Configurate window
window.set_mouse_visible(window_config['mouse'])
window.set_icon(pyglet.resource.image(CONFIG['resources']['icon']))

# Render screen border
screen_border = widgets.BorderWidget(0, 0, window.width/16, window.height/16,
                                     TileColor('border', 'transparent'))
window.push_widget(screen_border)

pyglet.app.run()
