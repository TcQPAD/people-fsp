#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from abstract_map import AbstractMap
from concurrency.barrier import Barrier
from core.constants.tile_value_enum import TileValueEnum
from core.map.obstacle import Obstacle
from core.threads.person_first_scenario import PersonFirstScenario
from tile import Tile

"""
Class to describe the map
"""
NAME_MAP = "map.txt"

'''
    Class to describe the map
'''


class MapFirstScenario(AbstractMap):

    def __init__(self, peopleNumber, loadedMap=False, queue=None):
        super(MapFirstScenario, self).__init__(loadedMap, queue)
        self.map = [[Tile(TileValueEnum.empty) for y in range(self.MAP_Y + 2)] for x in range(self.MAP_X + 2)]
        self.peopleNumber = peopleNumber
        self.barrier = Barrier(self.peopleNumber)
        self.queue = queue
        self.loadedMap = loadedMap
        self.fillMap()
        self.draw()

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
                self.personList.append(PersonFirstScenario(None, int(coordonnee[0]), int(coordonnee[1]), int(coordonnee[2]), self.barrier))

            line = fileMap.readline()
        fileMap.close()
