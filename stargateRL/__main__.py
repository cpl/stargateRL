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

window.set_mouse_visible(window_config['mouse'])
window.set_icon(pyglet.resource.image(CONFIG['resources']['icon']))

screen_border = widgets.BorderWidget(0, 0, window.width/16, window.height/16,
                                     TileColor('border', 'transparent'))


# main_menu = widgets.SelectionMenuWidget(GX_TILESET,
#                                         window.width/64,
#                                         window.height/32,
#                                         window.width/32,
#                                         window.height/64, 'gold',
#                                         'border', 'white',
#                                         'Settings', 'Exit',
#                                         L_EDGE=240, R_EDGE=240,
#                                         T_EDGE=240, B_EDGE=240,
#                                         LB_CORNER=240, LT_CORNER=240,
#                                         RB_CORNER=240, RT_CORNER=240)


window.push_widget(screen_border)
# window.push_widget(main_menu)

# @window.event
# def on_key_press(symbol, modifiers):
#     """Override Window key handler."""
#     print symbol
#     print pyglet.window.key.ESCAPE
#     if symbol == pyglet.window.key.ESCAPE:
#         return pyglet.event.EVENT_HANDLED


pyglet.app.run()
