
root = {'graphx': 'bin/graphics/',
        'map_ascii': 'data/map_ascii/',
        'map_json': 'data/map_json/'}

graphx = {'demon': root['graphx']+'demon.gif',
          'door_c': root['graphx']+'door12.gif',
          'floor': root['graphx']+'floor12.gif',
          'door_o': root['graphx']+'openDoor12.gif',
          'priest': root['graphx']+'priest.gif',
          'wall': root['graphx']+'wall12.gif',
          'selector': root['graphx']+'selection.png'}

mapdata = {'len_x': 20,
           'len_y': 14,
           'tile_size': 32}

window = {'camera_follow': False,
          'fullscreen': False,
          'resizable': True,
          'width': mapdata['len_x']*mapdata['tile_size'],
          'height': mapdata['len_y']*mapdata['tile_size']}

mouse = {'visible': False,
         'enabled': False}
