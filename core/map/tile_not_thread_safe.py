#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_tile import AbstractTile


class TileNotThreadSafe(AbstractTile):

    def __init__(self, contentEnum):
        super(TileNotThreadSafe, self).__init__(contentEnum)

    def getContent(self):
        pass

    def setContent(self, contentEnum):
        pass

    def isAtExit(self):
        pass

    def isCellTaken(self):
        pass

    def canPlacePerson(self):
        pass

    def isObstacle(self):
        pass

    def isExit(self):
        pass
