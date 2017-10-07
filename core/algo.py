#!/usr/bin/python
# -*- coding: utf-8 -*-

import math   # To use math.pow(x,y) = x^y

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

    '''
    Starts the algorithm
    '''
    def startAlgo(self) :
        self.setUpThreads()
        self.simulate()
        
    '''
    Creates N threads representing people,
    with N = self.peopleNumber
    '''
    def setUpThreads(self) :
        i = 0
        while i < math.pow(2, self.peopleNumber) :
            self.persons.append(Person(self))
            i+=1

    
    '''
    Simulates the movement of 
    2^peopleNumber persons to the upper left corner
    of the map.
    '''
    def simulate(self) :    
        for person in self.persons :
            print("Got a person : ", person)
