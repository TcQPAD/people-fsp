#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from abc import ABCMeta, abstractmethod

from core.algo.person_second_scenario import PersonSecondScenario
from core.constants.tile_value_enum import TileValueEnum
from core.map.obstacle import Obstacle
from core.threads.person_first_scenario import PersonFirstScenario

NAME_MAP = "map.txt"

"""
Gère la sauvegarde et le chargement d'une carte au format .txt
"""


class SaveLoadMap:

    def __init__(self):
        self.obstacleList = []
        self.personList = []


    """
    Permet de sauvegarder la carte générée dans un fichier .txt
    Il est composé de deux parties. La première correspond aux coordonnées des obstacles et la deuxième correspond
    aux coordonnées des personnes. Ces parties sont séparés par un "#"
    """

    def saveMap(self, map, persons):
        fileMap = open(NAME_MAP, "w")

        for obstacle in map.obstacleList:
            fileMap.write(
                str(obstacle.x1) + " " + str(obstacle.x2) + " " + str(obstacle.y1) + " " + str(obstacle.y2) + "\n")

        fileMap.write("#\n")

        for person in persons:
            fileMap.write(str(person.x) + " " + str(person.y) + " " + str(person.threadId) + "\n")

        fileMap.close()

    '''
    Load a .txt file containing a map. This file gets the informations about the position of the obstacles and the persons
    '''

    def loadMap(self, scenario):
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
                if scenario == 0:
                    self.personList.append(PersonFirstScenario(None, int(coordonnee[0]), int(coordonnee[1]), int(coordonnee[2]), self.barrier))
                else:
                    self.personList.append(PersonSecondScenario(None, int(coordonnee[0]), int(coordonnee[1]), int(coordonnee[2]), self.barrier))


            line = fileMap.readline()
        fileMap.close()