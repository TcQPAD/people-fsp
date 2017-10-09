#!/usr/bin/python
# -*- coding: utf-8 -*-

import math   # To use math.pow(x,y) = x^y

from core.person import Person
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
    
    /!\ When calling this getter, use it as if it were a field of the class,
    i.e. : algorithm.getMap.blabla (no parenthesis !!)
    '''
    @property
    def getMap(self):
        return self.map

    '''
    Starts the algorithm
    '''
    def startAlgo(self) :
        print("Setting up algorithm parameters")
        self.setUp()
        print("Finished setting up algorithm actors and parameters.\nStarting simulation.")
        self.simulate()
        
    '''
    Sets up all the actors of the simulation
    '''
    def setUp(self) :
        p = math.pow(2, self.peopleNumber)
        print("Setting up %d threads and distributing %d persons", p, p)
        self.setUpMap()
        print("Finished setting up threads and distributing %d persons in the map", self.peopleNumber)

    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    Distributes the persons across the map
    '''
    def setUpMap(self) :
        i = 0
        nbP = math.pow(2, self.peopleNumber)
        while i < nbP :
            print("Creating and placing new person")
            randX = randint(0, self.map.getSizeX() - 1)
            randY = randint(0, self.map.getSizeY() - 1)

            if self.map.isCellTaken(randX, randY) :
                while self.map.isCellTaken(randX, randY) :
                    print("A person already exists at these coordinates (%d, %d). Generating new placement for given person.", randX, randY)
                    randX = randint(0, self.map.getSizeX() - 1)
                    randY = randint(0, self.map.getSizeY() - 1)
            
            person = Person(self, randX, randY)
            self.persons.append(person)
            self.map.setCell(randX, randY, person)
            i+=1

    
    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''
    def simulate(self) :    
        '''
        for x in range(0, self.map.getSizeX() - 1) :
            for y in range(0, self.map.getSizeY() - 1) :
                if self.map.getCell(x, y) != 0 :
                    print("Map[" + str(x) + "][" + str(y) + "] = ", self.map.getCell(x, y))
        '''
        for person in self.persons :
            person.run()
