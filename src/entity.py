class Entity:
    ''' This class is used to represent any moving, living, (etc...) entity
    inside the game. This includes enemies or event the player. '''
    def __init__(self, name, x=-1, y=-1, symbol='?'):
        self.name = name
        self.x = x
        self.y = y
        self.symbol = symbol

    def __repr__(self):
        return '''Entity(Name:{},Position:({},{}),Symbol:{})\
               '''.format(self.name, self.x, self.y, self.symbol)

    def save(self):
        ''' Soon to be deprecated (or maybe not), JSON save method. '''
        return {'name': self.name, 'x': self.x, 'y': self.y,
                'symbol': self.symbol}

    def move(self, direction):
        ''' Shift the Entity position by a given x and y. '''
        self.x += direction[0]
        self.y += direction[1]

    def set_position(self, direction):
        ''' Set the Entity position to a given x and y. '''
        self.x = direction[0]
        self.y = direction[1]

    def get_position(self):
        ''' Get the Entity position as x,y tuple. '''
        return (self.x, self.y)


class Player(Entity):
    ''' This class will hold special characteristics, unique to the player. '''
    def __repr__(self):
        return '''Player(Name:{},Position:({},{}),Symbol:{})\
               '''.format(self.name, self.x, self.y, self.symbol)
