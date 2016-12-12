import pyglet
import config


class Entity():
    def __init__(self, _name, _x, _y, _rootMap, _ascii, _image):
        self.name = _name
        self.x = _x
        self.y = _y
        self.rootMap = _rootMap
        self.ascii = _ascii

        self.imagePath = _image
        self.image = pyglet.image.load(_image)
        self.sprite = pyglet.sprite.Sprite(self.image,
                                           _x * config.mapdata['tileSize'],
                                           _y * config.mapdata['tileSize'])

        _rootMap.tiles[_y][_x].isWalkable = False
        _rootMap.tiles[_y][_x].entity = self

    def __str__(self):
        _string = 'Name: ' + self.name + '; Position: ' + str(self.x) + ',' + str(self.y)
        return _string

    def setPosition(self, _x, _y, _force=False):
        if _force:
            self.unocupyPosition()
            self.x = _x
            self.y = _y
            self.updatePosition()
        else:
            if self.rootMap.tiles[_y][_x].isWalkable:
                self.unocupyPosition()
                self.x = _x
                self.y = _y
                self.updatePosition()

    def addPosition(self, _x, _y, _force=False):
        if _force:
            self.unocupyPosition()
            self.x += _x
            self.y += _y
            self.updatePosition()
        else:
            if self.rootMap.tiles[self.y + _y][self.x + _x].isWalkable:
                self.unocupyPosition()
                self.x += _x
                self.y += _y
                self.updatePosition()

    def getPosition(self):
        return self.x, self.y

    def updatePosition(self):
        self.ocupyPosition()
        self.sprite.set_position(self.x * config.mapdata['tileSize'],
                                 self.y * config.mapdata['tileSize'])

    def ocupyPosition(self):
        self.rootMap.tiles[self.y][self.x].isWalkable = False
        self.rootMap.tiles[self.y][self.x].entity = self

    def unocupyPosition(self):
        self.rootMap.tiles[self.y][self.x].isWalkable = True
        self.rootMap.tiles[self.y][self.x].entity = None

    def save(self):
        return {'name': self.name, 'x': self.x, 'y': self.y,
                'ascii': self.ascii, 'imagePath': self.imagePath}


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
