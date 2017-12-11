#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

"""
A person which is thread safe, used in the second
scenario of the algorithm
"""


class AbstractPerson:
    __metaclass__ = ABCMeta

    def __init__(self, algorithm, x, y, threadId):
        self._algorithm = algorithm
        self.threadId = threadId
        # Initial coordinates of this person
        self._x = x
        self._y = y

    '''
    Returns the x coordinate of this person
    '''

    @property
    @abstractmethod
    def x(self):
        pass

    '''
    Returns the y coordinate of this person
    '''

    @property
    @abstractmethod
    def y(self):
        pass

    @property
    @abstractmethod
    def algorithm(self):
        pass

    @algorithm.setter
    @abstractmethod
    def algorithm(self, algorithm):
        pass

    @x.setter
    @abstractmethod
    def x(self, x):
        pass

    @y.setter
    @abstractmethod
    def y(self, y):
        pass