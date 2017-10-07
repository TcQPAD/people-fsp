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
    def __init__(self, algorithm):
        Thread.__init__(self)
        self.algorithm = algorithm