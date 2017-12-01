#!/usr/bin/python
# -*- coding: utf-8 -*-



class Obstacle:

    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def isInside(self, obstacle):
        x1Test = obstacle.x1
        x2Test = obstacle.x2
        y1Test = obstacle.y1
        y2Test = obstacle.y2

        if (self.x1 <= x1Test <= self.x2) or (self.x1 <= x2Test <= self.x2):
            return True
        if (self.y1 <= y1Test <= self.y2) or (self.y1 <= y2Test <= self.y2):
            return True

        return False