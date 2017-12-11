#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading  # to introduce parallelism

"""
Multi-threaded zone of the map that will handle people movements
in the map of the simulation
"""


class MapZone(threading.Thread):

    def __init__(self, algorithm, zoneId, barrier=None):
        threading.Thread.__init__(self)
        self.persons = []
        self.algorithm = algorithm
        self.zoneId = zoneId
        self.barrier = barrier
        self.lock = threading.Lock()

    """
    Makes the current zone responsible of the given
    person
    """

    def handlePerson(self, person):
        self.persons.append(person)

    def discardPerson(self, person):
        self.persons.remove(person)

    def hasNoPerson(self):
        self.lock.acquire()
        is_empty = len(self.persons)
        self.lock.release()
        return is_empty == 0

    def run(self):
        # wait all people or the race is unfair!
        self.barrier.wait()

        # this person will move until he reaches the exit of the map :
        # (0,0), (0,1), (1,0), (1,1)
        while not self.algorithm.hasFinished():

            persons_to_discard = [person for person in self.persons if self.algorithm.getMap.isOnTile(person)]
            # person was on border
            # give it to another map zone
            for person in persons_to_discard:
                self.algorithm.changePersonZone(self.zoneId, person)

            # refreshes the array of persons if some persons were on a border
            self.persons = [person for person in self.persons if person not in persons_to_discard]

            # delete all people at exit if zone is zone 0 (containing the exit)
            if self.zoneId == 0:
                self.persons = [person for person in self.persons if not self.algorithm.getMap.isAtExit(person)]

            for person in self.persons:
                print "{0}\n".format("Moving person: " + str(person.x) + " , " + str(person.y))
                if not self.algorithm.getMap.isOnTile(person):
                    self.algorithm.getMap.movePerson(person)





