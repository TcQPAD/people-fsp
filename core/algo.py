#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc

'''
Class that holds the algorithm to move to the exit
of the map
'''


class Algorithm:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    """
    Starts the algorithm
    """

    @abc.abstractmethod
    def startAlgo(self):
        pass
