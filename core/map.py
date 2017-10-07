#!/usr/bin/python
# -*- coding: utf-8 -*-

MAP_X = 512
MAP_Y = 128

'''
    Class to describe the map
'''
class Map :

    def __init__(self) :

        self.map = [[0 for x in range(MAP_X)] for y in range(MAP_Y)]