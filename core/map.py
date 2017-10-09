#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from enum import Enum
import random

class Tile(Enum):
    empty = 0
    obstacle = 1
    exit = 2

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
        self.createExit()
        self.createObstacle()

    def createBorder(self):
        '''
        On mets les bordures nord et sud
        '''
        for y in range (MAP_Y + 2):
            self.map[0][y] = Tile.obstacle

        for y in range (MAP_Y + 2):
            self.map[511][y] = Tile.obstacle

        '''
        On mets les bordures ouest et est
        '''

        for x in range (1, MAP_X + 1):
            self.map[x][0] = Tile.obstacle
        for x in range (1, MAP_X + 1):
            self.map[x][127] = Tile.obstacle

    def createExit(self):
        self.map[0][0] = Tile.exit
        self.map[0][1] = Tile.exit
        self.map[1][0] = Tile.exit
        self.map[1][1] = Tile.exit

    def createObstacle(self):
        numberObstacleToGenerate = random.randint(5,9)
        for i in range(numberObstacleToGenerate):
            x1 = random.randint(2, MAP_X / 2)
            x2 = random.randint(x1, MAP_X - 3)

            y1 = random.randint(4, MAP_Y / 2)
            y2 = random.randint(y1, MAP_Y - 2)
            self.fillArea(x1, y1, x2, y2)

    def fillArea(self, x1, y1, x2, y2) :
        for x in range (x1, x2):
            for y in range(y1, y2):
                self.map[x][y] = Tile.obstacle

    def isObstacle(self, x, y) :
        return self.map[x][y] == Tile.obstacle

    def isExit(self, x, y) :
        return self.map[x][y] == Tile.exit

    def printMap(self):
        for x in range (MAP_X):
            for y in range (MAP_Y):
                print(self.map[x][y].value, end='')
            print ('\n', end='')

