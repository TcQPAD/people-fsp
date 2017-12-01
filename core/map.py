#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from tile import Tile
from tile_value_enum import TileValueEnum
import random

from core.obstacle import Obstacle
from person import Person
from core.display import Display


MAP_X = 512
MAP_Y = 128

NAME_MAP = "map.txt"

'''
    Class to describe the map
'''


class Map:

    def __init__(self, loadedMap, display=None) :
        self.obstacleList = []
        self.display = display
        self.map = [[Tile(TileValueEnum.empty) for y in range(MAP_Y + 2)] for x in range(MAP_X + 2)]
        self.loadedMap = loadedMap

        self.fillMap()
        self.draw()

    '''
    Returns true if the given cell contains a person
    '''

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

    '''
    Returns true if the given cell has the given person in it
    '''

    def hasPerson(self, person):
        return self.map[person.x][person.y].hasPerson(person)

    '''
    Returns true if the given person has reached an exit cell correspond
    to an exit cell
    '''

    def isAtExit(self, person):
        return self.map[person.x][person.y].isAtExit()

    '''
    Returns true if the given Tile has an obstacle
    '''

    def isObstacle(self, x, y):
        return self.map[x][y].isObstacle()

    '''
    Returns true if the given Tile is an exit
    '''

    def isExit(self, x, y):
        return self.map[x][y].isExit()

    '''
    Moves the person at the given cell to the new AVAILABLE cell
    that MINIMIZES the distance from (x,y) to the TileValueEnum.exit cells
    '''

    def movePerson(self, person):

        if not self.hasPerson(person):
            raise IndexError("No person exists in the provided cell : (%d, %d)", person.x, person.y)

        else:
            # empty the cell
            self.map[person.x][person.y].setContent(TileValueEnum.empty)
            if person.x > 0 and person.y > 0:
                self.choosePersonNextCase(person)
            if not self.isAtExit(person):
                self.map[person.x][person.y].setContent(person)


    '''
    Choose a person's next case to avoid obstacles
    '''

    def choosePersonNextCase(self, person):
        if not self.isObstacle(person.x - 1, person.y - 1):
            person.x = person.x - 1
            person.y = person.y - 1
        else:
            if not self.isObstacle(person.x - 1, person.y):
                person.x = person.x - 1
            else:
                if not self.isObstacle(person.x, person.y - 1):
                    person.y = person.y - 1

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
        '''
        On mets les bordures nord et sud
        '''
        for y in range(MAP_Y + 2):
            self.map[0][y] = Tile(TileValueEnum.obstacle)

        for y in range(MAP_Y + 2):
            self.map[511][y] = Tile(TileValueEnum.obstacle)

        '''
        On mets les bordures ouest et est
        '''

        for x in range(1, MAP_X + 1):
            self.map[x][0] = Tile(TileValueEnum.obstacle)
        for x in range(1, MAP_X + 1):
            self.map[x][127] = Tile(TileValueEnum.obstacle)

    def createExit(self):
        self.map[0][0] = Tile(TileValueEnum.exit)
        self.map[0][1] = Tile(TileValueEnum.exit)
        self.map[1][0] = Tile(TileValueEnum.exit)
        self.map[1][1] = Tile(TileValueEnum.exit)

    def createObstacle(self):
        numberObstacleToGenerate = random.randint(3, 5)
        i = 0

        while (i  < numberObstacleToGenerate ):
            x1 = random.randint(2, MAP_X / 2)
            x2 = random.randint(x1, MAP_X - 3)

            y1 = random.randint(4, MAP_Y / 2)
            y2 = random.randint(y1, MAP_Y - 2)

            obstacle = Obstacle(x1, x2, y1, y2)

            if not self.checkCoordonnee(obstacle):
                i = i + 1
                self.obstacleList.append(obstacle)

    def fillArea(self, x1, y1, x2, y2) :
        for x in range (x1, x2):
            for y in range(y1, y2):
                self.map[x][y] = Tile(TileValueEnum.obstacle)

    def printMap(self):
        for x in range(MAP_X):
            for y in range(MAP_Y):
                print(self.map[x][y].value, end='')
            print('\n', end='')

    def checkCoordonnee(self, obstacle):
        if not self.obstacleList:
            return False

        for oneObstacle in self.obstacleList:
            if obstacle.isInside(oneObstacle) :
                return True

        return False

    def saveMap(self, persons):
        file = open(NAME_MAP, "w")

        for obstacle in self.obstacleList:
            file.write(str(obstacle.x1) + " " + str(obstacle.x2) + " " + str(obstacle.y1) + " " + str(obstacle.y2) + "\n")

        file.write("#\n")

        for person in persons:
            file.write(str(person._x) + " " + str(person._y) + "\n")

        file.close()

    def loadMap(self):
        file = open(NAME_MAP, "r")
        line = file.readline()

        parseObstacle = True

        personList = []


        while line:
            if(line == "#\n"):
                parseObstacle = False
                line = file.readline()
                continue

            coordonnee = line.split(' ')
            if(parseObstacle):
                self.obstacleList.append(Obstacle(int(coordonnee[0]), int(coordonnee[1]),  int(coordonnee[2]), int(coordonnee[3])))
            else :
                personList.append(Person(None, int(coordonnee[0]), int(coordonnee[1]), None))

            line = file.readline()
        file.close()


    def draw(self):
        print("Draw " + str(len(self.obstacleList)) + " obstacle(s)")

        for obstacle in self.obstacleList:
            self.fillArea(obstacle.x1, obstacle.x2, obstacle.y1, obstacle.y2)

            if self.display != None :
                self.display.drawObstacle(obstacle.x1, obstacle.y1, obstacle.x2, obstacle.y2)


