class Entity:

    def __init__(self, name, x=-1, y=-1, symbol='?'):
        self.name = name
        self.x = x
        self.y = y
        self.symbol = symbol

    def __repr__(self):
        return '''Entity(Name:{},Position:({},{}),Symbol:{})\
               '''.format(self.name, self.x, self.y, self.symbol)

    def save(self):
        return {'name': self.name, 'x': self.x, 'y': self.y,
                'symbol': self.symbol}

    def move(self, x, y):
        self.x += x
        self.y += y

    def set_position(self, x, y):
        self.x = x
        self.y = y


class Player(Entity):

    def __repr__(self):
        return '''Player(Name:{},Position:({},{}),Symbol:{})\
               '''.format(self.name, self.x, self.y, self.symbol)
