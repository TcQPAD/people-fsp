#!/usr/bin/python
# -*- coding: utf-8 -*-

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
