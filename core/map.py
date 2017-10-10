#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from threading import Lock
from enum import Enum
import random

from person import Person

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

        '''
        The object that will do the magic to synchronize the calling threads,
        i.e., the Person objects.
        '''
        self.sharedMapLock = Lock()

    '''
    Returns true if the given cell contains a person
    '''
    def isCellTaken(self, x, y) :
        return self.map[x][y] != Tile.empty and self.map[x][y] != Tile.obstacle

    def getCell(self, x, y):
        return self.map[x][y]

    def setCell(self, x, y, val) :
        self.map[x][y] = val

    def getSizeX(self) :
        return MAP_X

    def getSizeY(self) :
        return MAP_Y

    '''
    Returns true if the given cell has the given person in it
    '''
    def hasPerson(self, person) :
        return person == self.map[person.x][person.y]

    '''
    Returns true if the given person has reached an exit cell correspond
    to an exit cell
    '''
    def isAtExit(self, person) :
        return self.map[person.x][person.y] == Tile.exit

    '''
    Moves the person at the given cell to the new AVAILABLE cell
    that MINIMIZES the distance from (x,y) to the Tile.exit cells
    '''
    def movePerson(self, person) :
        self.sharedMapLock.acquire()

        if not self.hasPerson(person) :
            # we need to release the lock, or the thread throwing this error will keep this ressource
            # locked and we'll have deadlocks.
            self.sharedMapLock.release()
            raise IndexError("No person exists in the provided cell : (%d, %d)", person.x, person.y)

        else :
            # empty the cell
            self.map[person.x][person.y] = Tile.empty
            if person.x > 0 :
                person.x = person.x - 1
            if person.y > 0 :
                person.y = person.y - 1

                    # if person is not at the exit, we make it move and replace the cell
            if not self.isAtExit(person) :
                self.map[person.x][person.y] = person

        self.sharedMapLock.release()

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

