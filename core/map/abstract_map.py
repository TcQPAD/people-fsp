#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from abc import ABCMeta, abstractmethod

from core.constants.tile_value_enum import TileValueEnum
from core.map.obstacle import Obstacle

"""
Abstract map to handle the data structure, and common methods
"""


class AbstractMap:
    __metaclass__ = ABCMeta

    def __init__(self, loadedMap=False, queue=None):
        self.map = []
        self.MAP_X = 512
        self.MAP_Y = 128
        self.loadedMap = loadedMap
        self.obstacleList = []
        self.queue = queue

    def getSizeX(self):
        return self.MAP_X

    def getSizeY(self):
        return self.MAP_Y

    """
    Returns true if the given cell contains a person
    """

    def isCellTaken(self, x, y):
        return self.map[x][y].isCellTaken()

    def getCell(self, x, y):
        return self.map[x][y].getContent()

    def setCell(self, x, y, val):
        self.map[x][y].setContent(val)

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
        # no need to check obstacle because obstacle can't touch the borders of the map
        person.y -= 1

    def moveAlongY(self, person):
        # no need to check obstacle because obstacle can't touch the borders of the map
        person.x -= 1

    def fillMap(self):
        self.createBorder()
        self.createExit()

        if not self.loadedMap:
            print("Map : created" + str(self.loadedMap))
            self.createObstacle()
        else:
            print("Map : load")
            self.loadMap()

    def createBorder(self):

        """
        On met les bordures nord et sud
        """
        for y in range(self.MAP_Y + 2):
            self.map[0][y].setContent(TileValueEnum.obstacle)

        for y in range(self.MAP_Y + 2):
            self.map[511][y].setContent(TileValueEnum.obstacle)

        """      
        On met les bordures ouest et est
        """
        for x in range(1, self.MAP_X + 1):
            self.map[x][0].setContent(TileValueEnum.obstacle)
        for x in range(1, self.MAP_X + 1):
            self.map[x][127].setContent(TileValueEnum.obstacle)

    def createExit(self):
        self.map[0][0].setContent(TileValueEnum.exit)
        self.map[0][1].setContent(TileValueEnum.exit)
        self.map[1][0].setContent(TileValueEnum.exit)
        self.map[1][1].setContent(TileValueEnum.exit)

    def createObstacle(self):
        numberObstacleToGenerate = random.randint(3, 5)
        i = 0

        while i < numberObstacleToGenerate:
            x1 = random.randint(2, self.MAP_X / 2)
            x2 = random.randint(x1, self.MAP_X - 3)

            y1 = random.randint(4, self.MAP_Y / 2)
            y2 = random.randint(y1, self.MAP_Y - 2)

            obstacle = Obstacle(x1, x2, y1, y2)

            if not self.checkCoordonnee(obstacle):
                i += 1
                self.obstacleList.append(obstacle)
                for x in range(x1, x2):
                    for y in range(y1, y2):
                        self.map[x][y].setContent(TileValueEnum.obstacle)

    def fillArea(self, x1, y1, x2, y2):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self.map[x][y].setContent(TileValueEnum.obstacle)

    def checkCoordonnee(self, obstacle):
        if not self.obstacleList:
            return False

        for oneObstacle in self.obstacleList:
            if obstacle.isInside(oneObstacle):
                return True

        return False

    def draw(self):
        print("Draw " + str(len(self.obstacleList)) + " obstacle(s)")

        for obstacle in self.obstacleList:
            self.fillArea(obstacle.x1, obstacle.x2, obstacle.y1, obstacle.y2)

            if self.queue is not None:
                self.queue.put(str(obstacle.x1) + " " + str(obstacle.y1) + " " + str(obstacle.x2) + " " + str(obstacle.y2))

    @abstractmethod
    def loadMap(self):
        pass
