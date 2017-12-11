#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_map import AbstractMap
from core.threads.map_zone import MapZone

"""
A map for the second scenario, that will create create the data structure
representing the map, and store all the objects in it : people, obstacles, etc...
"""


class MapSecondScenario(AbstractMap):

    def __init__(self):
        super(MapSecondScenario, self).__init__()
        self.nb_zones = 4
        self.map_zones = []

    def setUpMap(self):
        for i in enumerate(1, 4):
            self.map_zones.append(MapZone(self, i))
