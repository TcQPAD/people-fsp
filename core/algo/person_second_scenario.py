#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Lock  # to introduce parallelism

from core.algo.person_abstract import AbstractPerson

'''
Represents a person in the simulation. This class
doesn't extend the Thread class, because it will be the map that will be threaded.
This class is just a "shared resource" used by the different threads of the map
and thus should be thread safe
'''


class PersonSecondScenario(AbstractPerson):
    """
    Initializes this object, and the Thread
    that will be used to perform the simulation
    """

    def __init__(self, algorithm, x, y, threadId, barrier=None):
        AbstractPerson.__init__(self, algorithm, x, y, threadId)

        # place a barrier so this person
        # waits the other ones
        self.barrier = barrier
        self.lock = Lock()

    '''
    Returns the x coordinate of this person
    '''

    @property
    def x(self):
        self.lock.acquire()
        tmp = self._x
        self.lock.release()
        return tmp

    '''
    Returns the y coordinate of this person
    '''

    @property
    def y(self):
        self.lock.acquire()
        tmp = self._y
        self.lock.release()
        return tmp

    @property
    def algorithm(self):
        self.lock.acquire()
        tmp = self._algorithm
        self.lock.release()
        return tmp

    @algorithm.setter
    def algorithm(self, algorithm):
        self.lock.acquire()
        self._algorithm = algorithm
        self.lock.release()

    @x.setter
    def x(self, x):
        self.lock.acquire()
        self._x = x
        self.lock.release()

    @y.setter
    def y(self, y):
        self.lock.acquire()
        self._y = y
        self.lock.release()

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
