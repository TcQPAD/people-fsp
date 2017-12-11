#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_tile import AbstractTile
from core.constants.tile_value_enum import TileValueEnum


class TileNotThreadSafe(AbstractTile):

    def __init__(self, contentEnum):
        super(TileNotThreadSafe, self).__init__(contentEnum)

    """
    Returns the content of this Tile
    """

    def getContent(self):
        return self.content

    """
    Sets the content of this Tile to the given value
    """

    def setContent(self, contentEnum):
        self.content = contentEnum

    """
    Returns true if the given person has reached the exit cell
    """

    def isAtExit(self):
        return self.content == TileValueEnum.exit

    """
    Returns true if the given cell contains a person
    """

    def isCellTaken(self):
        return self.content != TileValueEnum.empty and self.content != TileValueEnum.obstacle

    """
    Returns true if a person can be placed in this Tile
    """

    def canPlacePerson(self):
        return self.content == TileValueEnum.empty

    """
    Returns true if the given Tile has an obstacle
    """

    def isObstacle(self):
        return self.content == TileValueEnum.obstacle

    """
    Returns true if the given Tile is an exit
    """

    def isExit(self):
        return self.content == TileValueEnum.exit

    """
    Returns true since this class is the Tile class
    """

    def isOnTile(self):
        return False
