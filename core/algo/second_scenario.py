#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from random import randint, choice
from threading import Lock

from concurrency.barrier import Barrier
from core.algo.algo import Algorithm
from core.algo.person_second_scenario import PersonSecondScenario
from core.threads.map_zone import MapZone

DEFAULT_PEOPLE_NUMBER = 4

'''
Class that holds the algorithm to move to the exit
of the map
'''


class SecondScenario(Algorithm):

    def __init__(self, map, peopleNumber=DEFAULT_PEOPLE_NUMBER, display=None, loadMap=False):
        Algorithm.__init__(self, map, peopleNumber, display, loadMap)
        self.nb_zones = 4
        self.map_zones = []
        self.barrier = Barrier(self.nb_zones)
        self.lock = Lock()
        self.scenario = 1
        # init map zones
        i = 1
        while i <= self.nb_zones:
            self.map_zones.append(MapZone(self, i - 1, self.barrier))
            i += 1

        i = 0

    def createPerson(self, algorithm, x, y, threadId, barrier):
        newPerson = PersonSecondScenario(self, x, y, threadId, barrier)
        self.defineZoneForPerson(newPerson)


    def defineZoneForPerson(self, person):
        # defines which zone is responsible of the person
        zone = self.defineZone(person.x, person.y)
        person.threadId = zone
        self.persons.append(person)

        # give it to the corresponding zone
        self.map_zones[zone].handlePerson(self.persons[len(self.persons) - 1])
        self.map.setCell(person.x, person.y, person)

    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''

    def simulate(self):
        for map_zone in self.map_zones:
            # we call start method to run the thread (run() method is called by start())
            map_zone.start()

        try:
            # waits the end of the threads execution in order to check the results after they finished
            # executing (if not, an exception will be raised before the simulation starts)
            for map_zone in self.map_zones:
                map_zone.join()
        except(KeyboardInterrupt, SystemExit):
            print '\n! Received keyboard interrupt, quitting threads.\n'
            sys.exit()

    """
    Places the person with the given coordinate in a zone.
    
    A zone is noted from 0 to 3, and are placed as this :
    
    _________________________
    
    |           |           |
    |    0      |     1     |
    |           |           |
    | --------------------- |
    |           |           |
    |    2      |     3     |
    |           |           |
    _________________________
    """

    def defineZone(self, xPerson, yPerson):
        if 0 < xPerson <= self.map.getSizeX() / 2:
            if 0 < yPerson < self.map.getSizeY() / 2:
                return 0
            else:
                return 2
        elif 0 < yPerson < self.map.getSizeY() / 2:
            return 1
        else:
            return 3

    """
    Transfers the given person from its zone to the new zone
    
    This is called when a person is on a Tile (not a TileNotThreadSafe)
    """

    def changePersonZone(self, zoneId, person):
        self.lock.acquire()

        # remove the person from the current map zone
        self.map_zones[zoneId].discardPerson(person)

        # then, add it to its new zone
        if person.x <= self.map.getSizeX() / 2:
            if person.y <= self.map.getSizeY() / 2:
                if not self.map_zones[0].hasPerson(person):
                    self.map_zones[0].handlePerson(person)
            else:
                if self.map_zones[2].hasPerson(person):
                    self.map_zones[2].handlePerson(person)

        elif person.y <= self.map.getSizeY() / 2:
            if self.map_zones[1].hasPerson(person):
                self.map_zones[1].handlePerson(person)
        else:
            if self.map_zones[3].hasPerson(person):
                self.map[3].handlePerson(person)

        self.lock.release()

    def hasFinished(self):
        self.lock.acquire()

        cpt = 0
        for map_zone in self.map_zones:
            if map_zone.hasNoPerson():
                cpt += 1

        b = cpt == 4
        self.lock.release()
        return b


    def specificLoad(self, person):
        self.defineZoneForPerson(person)