#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from random import randint, choice

from core.map.save_load_map import SaveLoadMap

DEFAULT_PEOPLE_NUMBER = 4

'''
Class that holds the algorithm to move to the exit
of the map
'''


class Algorithm:
    __metaclass__ = ABCMeta

    def __init__(self, map, peopleNumber=DEFAULT_PEOPLE_NUMBER, display=None, loadMap=False):
        self.loadMap = loadMap
        self.map = map
        self.peopleNumber = peopleNumber
        self.persons = []
        self.display = display
        self.saveLoadMap = SaveLoadMap()
        self.scenario = None

    '''
    A getter for the map

    /!\ When calling this getter, use it as if it were a field of the class,
    i.e. : algorithm.getMap.blabla (no parenthesis !!)
    '''

    @property
    def getMap(self):
        return self.map

    '''
    A getter for the display

    /!\ When calling this getter, use it as if it were a field of the class,
    i.e. : algorithm.getDisplay.blabla (no parenthesis !!)
    '''

    @property
    def getDisplay(self):
        return self.display

    '''
    Starts the algorithm
    '''

    def startAlgo(self):
        print("Setting up algorithm parameters")
        self.setUp()
        print("Finished setting up algorithm actors and parameters.\nStarting simulation.")
        self.simulate()

    '''
    Sets up all the actors of the simulation
    '''

    def setUp(self):
        print("Setting up " + str(self.peopleNumber) + " threads and distributing " + str(self.peopleNumber) + " persons")
        self.setUpMap(self.scenario)
        print("Finished setting up threads and distributing " + str(self.peopleNumber) + " persons in the map")

    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    Distributes the persons across the map
    '''
    def setUpMap(self, scenario):        # init map zones
        i = 0
        # generates a list of random tuples representing random (x, y) coordinates
        if not self.loadMap:
            randomCoordinates = [(randint(0, self.map.getSizeX() - 1), randint(0, self.map.getSizeY() - 1)) for k in
                                 range(int(self.peopleNumber))]
            while i < self.peopleNumber:
                print("Creating and placing new person")

                # picks a random tuple (x, y) from the list of random coordinates
                randomPickCoord = choice(randomCoordinates)
                # removes it so no other person will be placed here
                randomCoordinates.remove(randomPickCoord)

                if not self.map.canPlacePerson(randomPickCoord[0], randomPickCoord[1]):
                    while not self.map.canPlacePerson(randomPickCoord[0], randomPickCoord[1]):
                        # generate new coordinates in the list so we keep 1 tuple
                        # for each person
                        randomCoordinates.append(
                            (
                                randint(0, self.map.getSizeX() - 1),
                                randint(0, self.map.getSizeY() - 1)
                            )
                        )
                        randomPickCoord = choice(randomCoordinates)
                        randomCoordinates.remove(randomPickCoord)

                self.createPerson(self, randomPickCoord[0], randomPickCoord[1], i, None)
                i += 1

            self.saveLoadMap.saveMap(self.map, self.persons)

        else:
            self.saveLoadMap.loadMap(scenario)
            self.persons = self.saveLoadMap.personList

            for (i, person) in enumerate(self.persons):
                person.algorithm = self
                self.specificLoad(person)

            print(str(len(self.persons)) + " person(s) loaded")


    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''
    @abstractmethod
    def simulate(self):
        pass

    @abstractmethod
    def createPerson(self, algorithm, x, y, threadId, barrier):
        pass

    @abstractmethod
    def specificLoad(self, person):
        pass
