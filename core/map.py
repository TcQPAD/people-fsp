#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import random

from tile import Tile
from tile_value_enum import TileValueEnum

MAP_X = 512
MAP_Y = 128

"""
Class to describe the map
"""


class Map:

    def __init__(self, display=None):
        self.display = display
        self.map = [[Tile(TileValueEnum.empty) for y in range(MAP_Y + 2)] for x in range(MAP_X + 2)]
        self.fillMap()

    """
    Returns true if the given cell contains a person
    """

    def isCellTaken(self, x, y):
        return self.map[x][y].isCellTaken()

    def getCell(self, x, y):
        return self.map[x][y].getContent()

    def setCell(self, x, y, val):
        self.map[x][y].setContent(val)

    def getSizeX(self):
        return MAP_X

    def getSizeY(self):
        return MAP_Y

    """
    Returns true if the given person has reached an exit cell correspond
    to an exit cell
    """

    def isAtExit(self, person):
        return self.map[person.x][person.y].isAtExit()

    """
    Returns true if the given Tile has an obstacle
    """

    def isObstacle(self, x, y):
        return self.map[x][y].isObstacle()

    """
    Returns true if the given Tile is an exit
    """

    def isExit(self, x, y):
        return self.map[x][y].isExit()

    """
    Returns true if a person can be placed in this Tile
    """

    def canPlacePerson(self, x, y):
        return self.map[x][y].canPlacePerson()

    """
    Moves the person at the given cell to the new AVAILABLE cell
    that MINIMIZES the distance from (x,y) to the TileValueEnum.exit cells
    """

    def movePerson(self, person):

        if self.isAtExit(person):
            return

        # empty the cell
        self.map[person.x][person.y].setContent(TileValueEnum.empty)

        if person.x > 0 and person.y > 0:
            self.movePersonX(person)
            self.movePersonY(person)

        else:

            # borders
            if person.x == 0 and person.y > 0:
                self.moveAlongX(person)

            if person.x > 0 and person.y == 0:
                self.moveAlongY(person)

        if not self.isAtExit(person):
            self.map[person.x][person.y].setContent(person)

    """
    Choose a person's next case to avoid obstacles
    when x > 0
    """

    def movePersonX(self, person):
        if not self.isObstacle(person.x - 1, person.y):
            person.x -= 1

    """
    Choose a person's next case to avoid obstacles
    when y > 0
    """

    def movePersonY(self, person):
        if not self.isObstacle(person.x, person.y - 1):
            person.y -= 1

    def moveAlongX(self, person):
        if self.isObstacle(person.x - 1, person.y):
            person.y += 1

        person.x -= 1

    def moveAlongY(self, person):
        if self.isObstacle(person.x, person.y - 1):
            person.x += 1

        person.y -= 1

    def fillMap(self):
        self.createBorder()
        self.createExit()
        self.createObstacle()

    def createBorder(self):

        """
        On met les bordures nord et sud
        """
        for y in range(MAP_Y + 2):
            self.map[0][y].setContent(TileValueEnum.obstacle)

        for y in range(MAP_Y + 2):
            self.map[511][y].setContent(TileValueEnum.obstacle)

        """      
        On met les bordures ouest et est
        """
        for x in range(1, MAP_X + 1):
            self.map[x][0].setContent(TileValueEnum.obstacle)
        for x in range(1, MAP_X + 1):
            self.map[x][127].setContent(TileValueEnum.obstacle)

    def createExit(self):
        self.map[0][0].setContent(TileValueEnum.exit)
        self.map[0][1].setContent(TileValueEnum.exit)
        self.map[1][0].setContent(TileValueEnum.exit)
        self.map[1][1].setContent(TileValueEnum.exit)

    def createObstacle(self):
        # numberObstacleToGenerate = random.randint(5,9)
        numberObstacleToGenerate = 1
        for i in range(numberObstacleToGenerate):
            x1 = random.randint(2, MAP_X / 2)
            x2 = random.randint(x1, MAP_X - 3)

            y1 = random.randint(4, MAP_Y / 2)
            y2 = random.randint(y1, MAP_Y - 2)
            self.fillArea(x1, y1, x2, y2)

            if self.display is not None:
                self.display.drawObstacle(x1, y1, x2, y2)

    def fillArea(self, x1, y1, x2, y2):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self.map[x][y].setContent(TileValueEnum.obstacle)

    def printMap(self):
        for x in range(MAP_X):
            for y in range(MAP_Y):
                print(self.map[x][y].getContent(), end='')
            print('\n', end='')
