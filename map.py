#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from enum import Enum

class Tile(Enum):
    obstacle = 1
    empty = 2
    exit = 3

MAP_X = 512
MAP_Y = 128

'''
    Class to describe the map
'''
class Map :

    def __init__(self) :
        self.map = [[Tile.empty for y in range(MAP_Y + 2)] for x in range(MAP_X + 2)]
        self.fillMap()

    def fillMap(self) :
        self.createBorder()
        '''self.createExit()
        self.createObstacle()'''

    def createBorder(self):
        '''
        On mets les bordures nord et sud
        '''
        for y in range (MAP_Y + 2):
            self.map[0][y] = Tile.obstacle
        for y in range (MAP_Y + 2):
            self.map[MAP_X + 1][y] = Tile.obstacle

        '''
        On mets les bordures ouest et est
        '''

        for x in range (1, MAP_X + 1):
            self.map[x][0] = Tile.obstacle
        for x in range (1, MAP_X + 1):
            self.map[x][MAP_Y + 1] = Tile.obstacle

    def isObstacle(self, x, y) :
        return (self.map[x][y] == Tile.Obstacle)

    def printMap(self):
        for x in range (MAP_X):
            for y in range (MAP_Y):
                print(self.map[x][y], end='')
            print ('\n', end='')

    '''def generateObstacle(self, numberObstacle) :
        return;'''