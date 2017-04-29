#!/usr/bin/python -B
# -*- coding: utf-8 -*-

"""Main file for stargateRL rouge-like game."""

import pyglet
import engine
import mapset

import json


def main():
    """Start the game."""
    # Load config file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Load Tileset
    gx = engine.graphx.GxTileset(config['resources']['tileset'],
                                 config['graphics']['size'])

    # Prepare the map
    map_obj = mapset.mapset.Map(20, 20, 20, 'Main Map')
    map_gen = mapset.generators.Flat(10, 10, ['floor', 'grass'], 'RL')
    map_gen.create()
    map_obj = map_gen.get_map()

    # Create the game window
    window = engine.render.GameWindow(config['graphics']['screen']['width'],
                                      config['graphics']['screen']['height'],
                                      gx,
                                      resizable=config['graphics']['screen']['resizable'],
                                      fullscreen=config['graphics']['screen']['fullscreen'],
                                      style=config['graphics']['screen']['style'])

    # Render the map
    window.render_map(map_obj)

    # Run the pyglet app
    pyglet.app.run()


if __name__ == '__main__':
    main()
