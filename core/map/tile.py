#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Defines a new class Tile used by the map
to represent its cells.

A Tile has (x, y) coordinates, a value in
[|1, 3|] that represents the object present at the
Tile coordinates, and several methods that
are Thread-safe, in order to synchronize
all the people on the map (where each person
is actually represented by a Thread).
"""

from threading import Lock  # to synchronize threads

from abstract_tile import AbstractTile
from core.constants.tile_value_enum import TileValueEnum


class Tile(AbstractTile):
    """
    contentEnum can be one of the following :
    empty = 0
    obstacle = 1
    exit = 2
    it can also be a Person object, but at initialization time,
    contentEnum can only be one of the previous value.
    """

    def __init__(self, contentEnum):
        """
        The object that will do the magic to synchronize the calling threads,
        i.e., the Person objects.
        """
        super(Tile, self).__init__(contentEnum)
        self.tileLock = Lock()

    """
    Returns the content of this Tile
    """
    def getContent(self):
        self.tileLock.acquire()
        tmp = self.content
        self.tileLock.release()
        return tmp

    """
    Sets the content of this Tile to the given value
    """

    def setContent(self, contentEnum):
        self.tileLock.acquire()
        self.content = contentEnum
        self.tileLock.release()

    """
    Returns true if the given person has reached the exit cell
    """

    def isAtExit(self):
        self.tileLock.acquire()
        tmp = self.content == TileValueEnum.exit
        self.tileLock.release()
        return tmp

    """
    Returns true if the given cell contains a person
    """

    def isCellTaken(self):
        self.tileLock.acquire()
        tmp = self.content != TileValueEnum.empty and self.content != TileValueEnum.obstacle
        self.tileLock.release()
        return tmp

    """
    Returns true if a person can be placed in this Tile
    """
    def canPlacePerson(self):
        self.tileLock.acquire()
        tmp = (self.content == TileValueEnum.empty)
        self.tileLock.release()
        return tmp

    """
    Returns true if the given Tile has an obstacle
    """

    def isObstacle(self):
        self.tileLock.acquire()
        tmp = self.content == TileValueEnum.obstacle
        self.tileLock.release()
        return tmp

    """
    Returns true if the given Tile is an exit
    """

    def isExit(self):
        self.tileLock.acquire()
        tmp = self.content == TileValueEnum.exit
        self.tileLock.release()
        return tmp
