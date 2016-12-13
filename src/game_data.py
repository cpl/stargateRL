import config
import pyglet


class GameData():

    def __init__(self, game_window, root_map, player, selector, entities=[]):
        self._game_window = game_window
        self._root_map = root_map
        self._player = player
        self._selector = selector

        self._batch_map = pyglet.graphics.Batch()
        self._batch_entity = pyglet.graphics.Batch()

        self._entities = entities

    def sync(self):
        self._root_map.load_map('data/map_ascii/test1.map')

        self._player._map = self._root_map

        self._selector._map = self._root_map

        for entity in self._entities:
            entity.set_batch(self._batch_entity)
            entity._map = self._root_map

        self._game_window._player = self._player
        self._game_window._selector = self._selector

    def initialize(self):
        self._player.set_batch(self._batch_entity)
        self._player.initialize()
        self._root_map.set_batch(self._batch_map)

        for entity in self._entities:
            entity.initialize()

        self._game_window._batch_map = self._batch_map
        self._game_window._batch_entity = self._batch_entity
