#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_map import AbstractMap
from core.constants.tile_value_enum import TileValueEnum

from tile import Tile
from tile_not_thread_safe import TileNotThreadSafe

"""
A map for the second scenario, that will create the data structure
representing the map, and store all the objects in it : people, obstacles, etc...
"""


class MapSecondScenario(AbstractMap):

    def __init__(self, loadedMap=False, display=None):
        super(MapSecondScenario, self).__init__(loadedMap, display)
        self.map = [[TileNotThreadSafe(TileValueEnum.empty) for y in range(self.MAP_Y + 2)] for x in
                    range(self.MAP_X + 2)]
        self.loadedMap = loadedMap
        self.display = display
        self.fillMap()
        self.draw()
        self.lockBorderTiles()

    """
    Locks the Tiles that are common to 2 MapZone objects
    in order to make them thread safe 

    We can use the Tile class because it has the same interface than 
    TileNotThreadSafe class
    """

    def lockBorderTiles(self):
        # vertical "re-typing"
        x = self.getSizeX() / 2
        y = 0

        # Tile is a thread safe class
        # we can reuse it to behave like a TileNotThreadSafe because
        # they have the exact same interface which is AbstractTile
        while y < self.getSizeY() - 1:
            self.map[x][y] = Tile(TileValueEnum.empty)
            y += 1

        # horizontal "re-typing"
        x = 0
        y = self.getSizeY() / 2

        while x < self.getSizeX() - 1:
            self.map[x][y] = Tile(TileValueEnum.empty)
            x += 1

    """
    Returns true if the person needs to be given to another zone,
    i.e., if he's on a Tile on a border
    """
    def isOnTile(self, person):
        return self.map[person.x][person.y].isOnTile()