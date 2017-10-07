#!/usr/bin/python
# -*- coding: utf-8 -*-

MAP_X = 512
MAP_Y = 128

'''
    Class to describe the map
'''
class Map :

    def __init__(self) :

        self.map = [[0 for y in range(MAP_Y)] for x in range(MAP_X)]

    '''
    Returns true if the given cell contains a person
    '''
    def hasPerson(self, x, y) :
        return self.map[x][y] != 0

    def getCell(self, x, y):
        return self.map[x][y]

    def setCell(self, x, y, val) :
        self.map[x][y] = val

    def getSizeX(self) :
        return MAP_X

    def getSizeY(self) :
        return MAP_Y