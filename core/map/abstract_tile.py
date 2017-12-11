#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class AbstractTile:
    __metaclass__ = ABCMeta

    def __init__(self, contentEnum):
        self.content = contentEnum

    """
    Returns the content of this Tile
    """
    @abstractmethod
    def getContent(self):
        pass

    """
    Sets the content of this Tile to the given value
    """
    @abstractmethod
    def setContent(self, contentEnum):
        pass

    """
    Returns true if the given person has reached the exit cell
    """
    @abstractmethod
    def isAtExit(self):
        pass

    """
    Returns true if the given cell contains a person
    """
    @abstractmethod
    def isCellTaken(self):
        pass

    """
    Returns true if a person can be placed in this Tile
    """
    @abstractmethod
    def canPlacePerson(self):
        pass

    """
    Returns true if the given Tile has an obstacle
    """
    @abstractmethod
    def isObstacle(self):
        pass

    """
    Returns true if the given Tile is an exit
    """
    @abstractmethod
    def isExit(self):
        pass
