#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from abstract_map import AbstractMap
from concurrency.barrier import Barrier
from core.constants.tile_value_enum import TileValueEnum
from core.map.obstacle import Obstacle
from core.threads.person_first_scenario import PersonFirstScenario
from tile import Tile
'''
    Class to describe the map
'''


class MapFirstScenario(AbstractMap):

    def __init__(self, peopleNumber, loadedMap=False, display=None):
        super(MapFirstScenario, self).__init__(loadedMap, display)
        self.map = [[Tile(TileValueEnum.empty) for y in range(self.MAP_Y + 2)] for x in range(self.MAP_X + 2)]
        self.personList = []
        self.peopleNumber = peopleNumber
        self.barrier = Barrier(self.peopleNumber)
        self.display = display
        self.loadedMap = loadedMap
        self.fillMap()
        self.draw()

    @property
    def getPersons(self):
        return self.personList
