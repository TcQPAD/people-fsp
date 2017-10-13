#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading # to introduce parallelism

'''
Represents a person in the simulation. This class
extends the Thread class, in order to make all persons
in the simulation move independently and at the same time.
'''
class Person(threading.Thread) :

    """
    Initializes this object, and the Thread
    that will be used to perform the simulation
    """
    def __init__(self, algorithm, x, y, threadId):
        threading.Thread.__init__(self)
        self.algorithm = algorithm
        self.threadId = threadId

        '''
        The object that will do the magic to synchronize the calling threads.
        '''
        self.sharedMapLock = threading.Lock()

        # Initial coordinates of this person
        self._x = x
        self._y = y

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


    @x.setter
    def x(self, x):
        self.sharedMapLock.acquire()
        self._x = x
        self.sharedMapLock.release()

    @y.setter
    def y(self, y):
        self.sharedMapLock.acquire()
        self._y = y
        self.sharedMapLock.release()

    
    '''
    Defines the behaviour of this Thread, i.e.,
    the code to execute in this thread while it's alive.

    This Thread is charged to leave the map contained by the given algorithm,
    and it is supposed to run SAFELY (i.e., no concurrency problems on shared map)

    This is the function to override to start a thread. However, you need to call
    start() to make this class run
    '''
    def run(self) :
        # this person will move until he reaches the exit of the map :
        # (0,0), (0,1), (1,0), (1,1)
        while not self.algorithm.getMap.isAtExit(self) :
            print "{0}\n".format("Moving person... " + str(self.threadId)),
            #self.algorithm.getDisplay.erasePerson(self._x, self._y) #Uncomment to desactivate trace
            self.algorithm.getMap.movePerson(self)
            self.algorithm.getDisplay.drawPerson(self._x, self._y)
    
        print "{0}\n".format("Reached exit, stopping this thread... " + str(self.threadId)),