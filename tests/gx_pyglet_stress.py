"""Stress test for pyglet config."""

import cProfile
import pyglet
import random
from pyglet import clock

# Disable error checking for increased performance
pyglet.options['debug_gl'] = False

clock.set_fps_limit(60)

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60.0

batch = pyglet.graphics.Batch()
window = pyglet.window.Window(WINDOWWIDTH, WINDOWHEIGHT)
fps_display = pyglet.clock.ClockDisplay()

image = pyglet.resource.image("square.jpg")


class Square(pyglet.sprite.Sprite):
    """DOCSTRING."""

    def __init__(self, x, y):
        """DOCSTRING."""
        pyglet.sprite.Sprite.__init__(self, img=image, batch=batch)
        self.x = x
        self.y = y
        self.v_x = random.randint(1, 100)
        self.v_y = random.randint(1, 100)
        self.v_r = random.randint(-100, 100)

    def update(self, dt):
        """DOCSTRING."""
        if self.x > WINDOWWIDTH:
            self.v_x *= -1
        elif self.x < 0:
            self.v_x *= -1
        if self.y > WINDOWHEIGHT:
            self.v_y *= -1
        elif self.y < 0:
            self.v_y *= -1

        self.x += self.v_x * dt
        self.y += self.v_y * dt
        self.rotation += self.v_r * dt


sqrs = []
for _ in range(5000):
    sqrs.append(Square(random.randint(0, WINDOWWIDTH-1),
                       random.randint(0, WINDOWHEIGHT-1)))

elapsed = 0.0


def update(dt):
    """DOCSTRING."""
    global elapsed
    elapsed += dt
    if elapsed >= 10.0:
        clock.unschedule(update)
        window.close()
    else:
        for s in sqrs:
            s.update(dt)


@window.event
def on_draw():
    """DOCSTRING."""
    window.clear()
    batch.draw()
    fps_display.draw()


clock.schedule_interval(update, 1.0/FPS)

if __name__ == '__main__':
    cProfile.run("pyglet.app.run()")
    c = input("...")
