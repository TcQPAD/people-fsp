#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from random import randint, choice

from concurrency.barrier import Barrier
from core.algo.algo import Algorithm
from core.threads.person_first_scenario import PersonFirstScenario

DEFAULT_PEOPLE_NUMBER = 4

'''
Class that holds the algorithm to move to the exit
of the map
'''


class FirstScenario(Algorithm):

    def __init__(self, map, peopleNumber=DEFAULT_PEOPLE_NUMBER, queue=None, loadMap=False):
        Algorithm.__init__(self, map, peopleNumber, queue, loadMap)

        # a barrier for all the people,
        # that will ensure that all people work at the same time!
        self.barrier = Barrier(self.peopleNumber)

    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    Distributes the persons across the map
    '''

    def setUpMap(self):
        i = 0
        print("Creating and placing people")
        # generates a list of random tuples representing random (x, y) coordinates
        if not self.loadMap:
            randomCoordinates = [(randint(0, self.map.getSizeX() - 1), randint(0, self.map.getSizeY() - 1)) for k in range(int(self.peopleNumber))]
            while i < self.peopleNumber:

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

                self.persons.append(PersonFirstScenario(self, randomPickCoord[0], randomPickCoord[1], i, self.barrier))
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
