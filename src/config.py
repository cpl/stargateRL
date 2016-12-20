import os

dir_src = os.path.dirname(__file__)
dir_root = os.path.join(dir_src, os.path.pardir)
dir_root = os.path.abspath(dir_root)

dir_bin = os.path.join(dir_root, 'bin')
dir_gfx = os.path.join(dir_bin, 'graphics')

gfx_tilesize = 16

map_size_x = 20
map_size_y = 14

window_width = map_size_x * gfx_tilesize
window_height = map_size_y * gfx_tilesize
window_caption = 'Stargate Rogue Like'
