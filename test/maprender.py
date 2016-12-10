import pyglet

from pyglet.window import key

priest_image = pyglet.image.load('bin/graphics/priest.gif')
wall_image = pyglet.image.load('bin/graphics/wall12.gif')
floor_image = pyglet.image.load('bin/graphics/floor12.gif')

batch = pyglet.graphics.Batch()
floor_tiles = []
for x in range(18):
    for y in range(13):
        floor_tiles.append(pyglet.sprite.Sprite(floor_image, x*32+32, y*32+32, batch=batch))
wall_tiles = []
for x in range(20):
    for y in range(15):
        if x == 0 or y == 0 or x == 19 or y == 14:
            wall_tiles.append(pyglet.sprite.Sprite(wall_image, x*32, y*32, batch=batch))

priest = pyglet.sprite.Sprite(priest_image, x=32, y=32)

window = pyglet.window.Window()


@window.event
def on_key_press(symbol, modifiers):
    yP = priest.y
    xP = priest.x
    if symbol == key.UP:
        if yP < 416:
            yP += 32
    elif symbol == key.DOWN:
        if yP > 32:
            yP -= 32
    elif symbol == key.LEFT:
        if xP > 32:
            xP -= 32
    elif symbol == key.RIGHT:
        if xP < 576:
            xP += 32
    priest.set_position(xP, yP)
    print xP, yP


@window.event
def on_draw():
    window.clear()
    batch.draw()
    priest.draw()

pyglet.app.run()
