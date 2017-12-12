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

    def __init__(self, map, peopleNumber=DEFAULT_PEOPLE_NUMBER, display=None, loadMap=False):
        Algorithm.__init__(self, map, peopleNumber, display, loadMap)

        # a barrier for all the people,
        # that will ensure that all people work at the same time!
        self.barrier = Barrier(self.peopleNumber)
        self.scenario = 0




    def createPerson(self, algorithm, x, y, threadId, barrier):
        newPerson = PersonFirstScenario(self, x, y, threadId, barrier)
        self.persons.append(newPerson)


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
