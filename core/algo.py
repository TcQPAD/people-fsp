#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

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
        self.setUpMap()
        print("Finished setting up threads and distributing " + str(self.peopleNumber) + " persons in the map")

    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    Distributes the persons across the map
    '''
    @abstractmethod
    def setUpMap(self):
        pass

    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''
    @abstractmethod
    def simulate(self):
        pass
