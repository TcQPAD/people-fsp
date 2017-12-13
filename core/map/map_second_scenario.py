#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_map import AbstractMap
from concurrency.barrier import Barrier
from core.algo.person_second_scenario import PersonSecondScenario
from core.constants.tile_value_enum import TileValueEnum
from core.map.obstacle import Obstacle

from tile import Tile
from tile_not_thread_safe import TileNotThreadSafe

NAME_MAP = "map.txt"

"""
A map for the second scenario, that will create the data structure
representing the map, and store all the objects in it : people, obstacles, etc...
"""


class MapSecondScenario(AbstractMap):

    def __init__(self, nbP, loadedMap=False, queue=None):
        super(MapSecondScenario, self).__init__(loadedMap, queue)
        self.map = [[TileNotThreadSafe(TileValueEnum.empty) for y in range(self.MAP_Y + 2)] for x in
                    range(self.MAP_X + 2)]
        self.loadedMap = loadedMap
        self.queue = queue
        self.peopleNumber = nbP
        self.barrier = Barrier(4)
        self.fillMap()
        self.draw()
        self.lockBorderTiles()

    """
    Locks the Tiles that are common to 2 MapZone objects
    in order to make them thread safe 

    We can use the Tile class because it has the same interface than 
    TileNotThreadSafe class
    """

    def lockBorderTiles(self):
        # vertical "re-typing"
        x = self.getSizeX() / 2
        y = 0

        # Tile is a thread safe class
        # we can reuse it to behave like a TileNotThreadSafe because
        # they have the exact same interface which is AbstractTile
        while y < self.getSizeY() - 1:
            self.map[x][y] = Tile(self.map[x][y].getContent())
            y += 1

        # horizontal "re-typing"
        x = 0
        y = self.getSizeY() / 2

        while x < self.getSizeX() - 1:
            self.map[x][y] = Tile(self.map[x][y].getContent())
            x += 1

    """
    Returns true if the person needs to be given to another zone,
    i.e., if he's on a Tile on a border
    """
    def isOnTile(self, person):
        return self.map[person.x][person.y].isOnTile()

    def saveMap(self, persons):
        fileMap = open(NAME_MAP, "w")

        for obstacle in self.obstacleList:
            fileMap.write(
                str(obstacle.x1) + " " + str(obstacle.x2) + " " + str(obstacle.y1) + " " + str(obstacle.y2) + "\n")

        fileMap.write("#\n")

        for person in persons:
            fileMap.write(str(person.x) + " " + str(person.y) + " " + str(person.threadId) + "\n")

        fileMap.close()

    '''
    Load a .txt file containing a map. This file gets the informations about the position of the obstacles and the persons
    '''

    def loadMap(self):
        fileMap = open(NAME_MAP, "r")
        line = fileMap.readline()

        parseObstacle = True

        while line:
            if line == "#\n":
                parseObstacle = False
                line = fileMap.readline()
                continue

            coordonnee = line.split(' ')
            if parseObstacle:
                self.obstacleList.append(
                    Obstacle(int(coordonnee[0]), int(coordonnee[1]), int(coordonnee[2]), int(coordonnee[3])))
            else:
                self.personList.append(PersonSecondScenario(None, int(coordonnee[0]), int(coordonnee[1]), int(coordonnee[2]), self.barrier))

            line = fileMap.readline()
        fileMap.close()
