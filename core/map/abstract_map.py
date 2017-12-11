#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta

from core.constants.tile_value_enum import TileValueEnum
from tile import Tile

"""
Abstract map to handle the data structure, and common methods
"""


class AbstractMap:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.MAP_X = 512
        self.MAP_Y = 128
        self.map = [[Tile(TileValueEnum.empty) for y in range(self.MAP_Y + 2)] for x in range(self.MAP_X + 2)]
