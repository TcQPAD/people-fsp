#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread # to introduce parallelism

'''
Represents a person in the simulation. This class
extends the Thread class, in order to make all persons
in the simulation move independently and at the same time.
'''
class Person(Thread) :

    """
    Initializes this object, and the Thread
    that will be used to perform the simulation
    """
    def __init__(self, algorithm, x, y):
        Thread.__init__(self)
        self.algorithm = algorithm

        # Initial coordinates of this person
        self.x = x
        self.y = y

    '''
    Defines the behaviour of this Thread, i.e.,
    the code to execute in this thread while it's alive.

    This Thread is charged to leave the map contained by the given algorithm,
    and it is supposed to run SAFELY (i.e., no concurrency problems on shared map)
    '''
    def run(self) :
        while not self.algorithm.getMap.isAtExit(self.x, self.y) :
            print("Running... ", self)
        return 0
    