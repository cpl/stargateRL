import pyglet
import config


class GameData:

    def __init__(self, root_map=None, player=None, entities=None):
        self.root_map = root_map
        self.player = player
        self.entities = entities

    def __repr__(self):
        _entities = ''
        for entity in self.entities:
            _entities += (str(entity)+'\n')
        return 'GameData(\n{},\n{},\n{})'.format(self.root_map,
                                                 self.player,
                                                 _entities)

    def save(self):
        _entities = []
        for entity in self.entities:
            _entities.append(entity.save())

        return {'root_map': self.root_map.save(), 'player': self.player.save(),
                'entities': _entities}

    def load(self):
        pass

