''' The following is a set of runtime constants, that can be modified by
the user in order to change the gameplay. '''

import os

dir_src = os.path.dirname(__file__)
dir_root = os.path.join(dir_src, os.path.pardir)
dir_root = os.path.abspath(dir_root)

dir_bin = os.path.join(dir_root, 'bin')
dir_data = os.path.join(dir_root, 'data')
dir_docs = os.path.join(dir_root, 'docs')
dir_test = os.path.join(dir_root, 'test')

dir_gfx = os.path.join(dir_bin, 'graphics')
dir_saves = os.path.join(dir_data, 'saves')

# ---------------------------------------------------------------------------- #

gfx_tilesize = 16

map_size_x = 20
map_size_y = 14

window_width = map_size_x * gfx_tilesize
window_height = map_size_y * gfx_tilesize

window_caption = 'Stargate Rogue Like'

window_fullscreen = False
window_resizeable = False

window_mouse_display = False

selector_show = True
selector_mouse = False
selector_keyboard = False
