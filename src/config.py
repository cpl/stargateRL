
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

mapdata = {'lenX': 20,
           'lenY': 14,
           'tileSize': 32}

window = {'cameraFollow': False,
          'fullscreen': False,
          'resizable': True,
          'width': mapdata['lenX']*mapdata['tileSize'],
          'height': mapdata['lenY']*mapdata['tileSize'],
          'visibleMouse': False,
          'enableMouse': True}
