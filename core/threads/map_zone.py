#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading  # to introduce parallelism

"""
Multi-threaded zone of the map that will handle people movements
in the map of the simulation
"""


class MapZone(threading.Thread):

    def __init__(self, map, zoneId):
        threading.Thread.__init__(self)
        self.persons = []
        self.map = map
        self.zoneId = zoneId

    """
    Makes the current zone responsible of the given
    person
    """

    def handle_person(self, person):
        self.persons.append(person)

    def run(self):
        pass
