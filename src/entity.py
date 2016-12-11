import pyglet
import config


class Entity():
    def __init__(self, _name, _x, _y, _rootMap, _ascii, _image):
        self.name = _name
        self.x = _x
        self.y = _y
        self.rootMap = _rootMap
        self.ascii = _ascii

        self.image = pyglet.image.load(_image)
        self.sprite = pyglet.sprite.Sprite(self.image,
                                           _x * config.TILE_SIZE,
                                           _y * config.TILE_SIZE)

    def __str__(self):
        _string = 'Name: ' + self.name + '; Position: ' + str(self.x) + ',' + str(self.y)
        return _string

    def setPosition(self, _x, _y, _force=False):
        if _force:
            self.x = _x
            self.y = _y
            self.sprite.set_position(self.x * config.TILE_SIZE,
                                     self.y * config.TILE_SIZE)
        else:
            if self.rootMap.tiles[_y][_x].isWalkable:
                self.x = _x
                self.y = _y
                self.sprite.set_position(self.x * config.TILE_SIZE,
                                         self.y * config.TILE_SIZE)

    def addPosition(self, _x, _y, _force=False):
        if _force:
            self.x += _x
            self.y += _y
            self.sprite.set_position(self.x * config.TILE_SIZE,
                                     self.y * config.TILE_SIZE)
        else:
            if self.rootMap.tiles[self.y + _y][self.x + _x].isWalkable:
                self.x += _x
                self.y += _y
                self.sprite.set_position(self.x * config.TILE_SIZE,
                                         self.y * config.TILE_SIZE)

    def getPosition(self):
        return self.x, self.y


class Player(Entity):
    def move(self, _key):
        if _key == pyglet.window.key.UP:
            self.addPosition(0, 1)
        elif _key == pyglet.window.key.DOWN:
            self.addPosition(0, -1)
        elif _key == pyglet.window.key.RIGHT:
            self.addPosition(1, 0)
        elif _key == pyglet.window.key.LEFT:
            self.addPosition(-1, 0)
