#!/usr/bin/python
# -*- coding: utf-8 -*-

from person import Person

DEFAULT_PEOPLE_NUMBER = 4

'''
Class that holds the algorithm to move to the exit
of the map
'''
class Algorithm :

    def __init__(self, map, peopleNumber=DEFAULT_PEOPLE_NUMBER, display=False):

        self.map = map
        self.peopleNumber = peopleNumber
        self.persons = []

    '''
    A getter for the map
    '''
    @property
    def x(self):
        return self.map

    start(self) :
    
        self.result = self.simulate()
        return self.result

    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    '''
    setUpThreads(self) :
        i = 0
        while i < self.peopleNumber :
            self.persons.append(Person(self))

    
    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''
    simulate(self) :    

