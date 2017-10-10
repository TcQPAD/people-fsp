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
        self.personNotAtExit = None

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
            
            person = Person(self, randX, randY, i)
            self.persons.append(person)
            self.map.setCell(randX, randY, person)
            i+=1


    '''
    Check that all persons have reached the exit of the map
    '''
    def checkResults(self) :
        for person in self.persons :
            if not self.getMap.isAtExit(person) :
                self.personNotAtExit = person
                return False

        return True
    
    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''
    def simulate(self) :
        for person in self.persons :
            # we call start method to run the thread (run() method is called by start())
            person.start()
        
        # waits the end of the threads execution in order to check the results after they finished
        # executing (if not, an exception will be raised before the simulation starts)
        for person in self.persons :
            person.join()

        # this code will be executed when all threads have finished running
        # since we called thread.join() after starting it
        if self.checkResults() :
            print("Simulation was successful")
        else :
            print("Person not at exit: ", self.personNotAtExit, self.personNotAtExit.x, self.personNotAtExit.y)
            raise Exception("Some persons didn't reach the exit of the map")