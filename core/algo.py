#!/usr/bin/python
# -*- coding: utf-8 -*-

import math   # To use math.pow(x,y) = x^y

from person import Person
from random import randint


DEFAULT_PEOPLE_NUMBER = 4

'''
Class that holds the algorithm to move to the exit
of the map
'''
class Algorithm :

    def __init__(self, map, peopleNumber=DEFAULT_PEOPLE_NUMBER, display=False):

        self.map = map
        self.peopleNumber = peopleNumber
        self.persons = []

    '''
    A getter for the map
    '''
    @property
    def x(self):
        return self.map

    '''
    Starts the algorithm
    '''
    def startAlgo(self) :
        self.setUp()
        self.simulate()
        
    '''
    Sets up all the actors of the simulation
    '''
    def setUp(self) :
        self.setUpThreads()
        self.setUpMap()

    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    '''
    def setUpThreads(self) :
        i = 0
        while i < math.pow(2, self.peopleNumber) :
            self.persons.append(Person(self))
            i+=1

    '''
    Distributes the persons across the map
    '''
    def setUpMap(self) :
        for person in self.persons :
            randX = randint(0, self.map.getSizeX() - 1)
            randY = randint(0, self.map.getSizeY() - 1)

            if self.map.hasPerson(randX, randY) :
                while self.map.hasPerson(randX, randY) :
                    randX = randint(0, self.map.getSizeX() - 1)
                    randY = randint(0, self.map.getSizeY() - 1)

            self.map.setCell(randX, randY, person)

    
    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''
    def simulate(self) :    
        for x in range(0, self.map.getSizeX() - 1) :
            for y in range(0, self.map.getSizeY() - 1) :
                if self.map.getCell(x, y) != 0 :
                    print("Map[" + str(x) + "][" + str(y) + "] = ", self.map.getCell(x, y))
