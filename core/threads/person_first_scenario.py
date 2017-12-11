#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading  # to introduce parallelism

from core.algo.person_abstract import AbstractPerson

'''
Represents a person in the simulation. This class
extends the Thread class, in order to make all persons
in the simulation move independently and at the same time.
'''


class PersonFirstScenario(threading.Thread, AbstractPerson):
    """
    Initializes this object, and the Thread
    that will be used to perform the simulation
    """

    def __init__(self, algorithm, x, y, threadId, barrier=None):
        AbstractPerson.__init__(self, algorithm, x, y, threadId)
        threading.Thread.__init__(self)

        # place a barrier so this person
        # waits the other ones
        self.barrier = barrier

    '''
    Returns the x coordinate of this person
    '''

    @property
    def x(self):
        return self._x

    '''
    Returns the y coordinate of this person
    '''

    @property
    def y(self):
        return self._y

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm):
        self._algorithm = algorithm

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    '''
    Defines the behaviour of this Thread, i.e.,
    the code to execute in this thread while it's alive.

    This Thread is charged to leave the map contained by the given algorithm,
    and it is supposed to run SAFELY (i.e., no concurrency problems on shared map)

    This is the function to override to start a thread. However, you need to call
    start() to make this class run
    '''

    def run(self):

        # wait all people or the race is unfair!
        self.barrier.wait()

        # this person will move until he reaches the exit of the map :
        # (0,0), (0,1), (1,0), (1,1)
        while not self._algorithm.getMap.isAtExit(self):
            # print "{0}\n".format("Moving person... " + str(self.threadId)),
            '''
            print "{0}\n".format(
                "\tCoordinates: " + str(self._x) + ", " + str(self._y)),
            '''

            '''
            #Uncomment to desactivate trace    
            if self.algorithm.getDisplay != None :
                self.algorithm.getDisplay.erasePerson(self._x, self._y)
            '''
            self._algorithm.getMap.movePerson(self)
            if self._algorithm.getDisplay is not None:
                self._algorithm.getDisplay.drawPerson(self._x, self._y)

        if not self._algorithm.getMap.isAtExit(self):
            print "{0}\n".format(
                "Person not at exit: " + str(self.threadId) + "\t, coordinates: " + str(self._x) + ", " + str(self._y)),
            raise Exception("Some persons didn't reach the exit of the map")
        else:
            print "{0}\n".format("Simulation was successful for person " + str(self.threadId)),

        print "{0}\n".format("Reached exit, stopping this thread... " + str(self.threadId)),