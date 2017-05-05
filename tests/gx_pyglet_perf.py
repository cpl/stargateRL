"""Test from StackOverflow, question 17235418."""

import pyglet
from pyglet.gl import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Direct OpenGL commands to this window.
config = Config(double_buffer = True)
window = pyglet.window.Window(config = config)
window.set_vsync(True)
window.set_fullscreen(True)

colorSwap = 0
fullscreen = 1

fps_display = pyglet.clock.ClockDisplay()

def on_draw(dt):
    global colorSwap
    glClear(GL_COLOR_BUFFER_BIT)  # Clear the color buffer
    glLoadIdentity()              # Reset model-view matrix

    glBegin(GL_QUADS)
    if colorSwap == 1:
        glColor3f(1.0, 0.0, 0.0)
        colorSwap = 0
    else:
        glColor3f(0.0, 1.0, 0.0)
        colorSwap = 1

    glVertex2f(window.width, 0)
    glVertex2f(window.width, window.height)
    glVertex2f(0.0, window.height)
    glVertex2f(0.0, 0.0)
    glEnd()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    global fullscreen
    if symbol == pyglet.window.key.F:
        if fullscreen == 1:
            window.set_fullscreen(False)
            fullscreen = 0
        else:
            window.set_fullscreen(True)
            fullscreen = 1
    elif symbol == pyglet.window.key.ESCAPE:
        print ''


dt = pyglet.clock.tick()
pyglet.clock.schedule_interval(on_draw, 0.0001)
pyglet.app.run()