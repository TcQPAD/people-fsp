#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from random import randint, choice

from core.algo import Algorithm
from core.person_second_scenario import PersonSecondScenario

DEFAULT_PEOPLE_NUMBER = 4

'''
Class that holds the algorithm to move to the exit
of the map
'''


class SecondScenario(Algorithm):

    def __init__(self, map, peopleNumber=DEFAULT_PEOPLE_NUMBER, display=None, loadMap=False):
        Algorithm.__init__(self, map, peopleNumber, display, loadMap)

    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    Distributes the persons across the map
    '''

    def setUpMap(self):
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
                zone = self.defineZone(randomPickCoord[0], randomPickCoord[1])
                self.persons.append(PersonSecondScenario(self, randomPickCoord[0], randomPickCoord[1], i, zone))
                self.map.setCell(randomPickCoord[0], randomPickCoord[1], self.persons[i])
                i += 1

            self.map.saveMap(self.persons)

        else:
            self.persons = self.map.personList

            for (i, person) in enumerate(self.persons):
                person.algorithm = self

            print(str(len(self.persons)) + " person(s) loaded")

    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''

    def simulate(self):
        for person in self.persons:
            # we call start method to run the thread (run() method is called by start())
            person.start()

        try:
            # waits the end of the threads execution in order to check the results after they finished
            # executing (if not, an exception will be raised before the simulation starts)
            for person in self.persons:
                person.join()
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
        if 0 < xPerson < self.map.getSizeX() / 2:
            if 0 < yPerson < self.map.getSizeY() / 2:
                return 0
            else:
                return 2
        elif 0 < yPerson < self.map.getSizeY() / 2:
            return 1
        else:
            return 3
