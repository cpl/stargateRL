"""Graphical test for SpriteText."""

import pyglet

from stargateRL.engine.screen import GameWindow
from stargateRL.engine.graphx import TileColor
from stargateRL.engine.objects import SpriteText
from stargateRL.utils import CONFIG


# Create the game window
window_config = CONFIG['graphics']['window']

window = GameWindow(window_config['width'],
                    window_config['height'],
                    fullscreen=window_config['fullscreen'],
                    resizable=window_config['resizable'],
                    style=window_config['style'])

LONG_TEXT = """Est ab voluptatem accusamus rerum quia qui soluta amet.\
Porro unde incidunt voluptas nulla dolor. Illo aut vel earum similique.\
Omnis minima sit amet est non iusto. Voluptates sit maiores corporis.\
Delectus sit veniam iure autem. Sunt minus fuga facilis voluptatem dolore qui.\
Sapiente deleniti mollitia soluta aut minima debitis.

Excepturi totam officia non dolore ratione possimus omnis. Magnam quidem vel\
suscipit consequatur pariatur nostrum. Culpa beatae at voluptatum eos. In nisi\
ut eos et explicabo quia.

Magni quis iure est qui nihil. Molestiae id doloremque ex facilis. Sapiente\
vero eaque omnis optio impedit.

Aliquam voluptatibus id non voluptate quia laudantium architecto sequi.\
Totam ipsum laudantium commodi voluptatem voluptates asperiores illum\
pariatur. Sed quisquam occaecati quo distinctio quaerat reiciendis.
"""
st = SpriteText(LONG_TEXT, 1, window.y_tiles-2, 50, None,
                TileColor('red', 'gold'), window._batch)

pyglet.app.run()
