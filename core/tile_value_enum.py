#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Defines an enum with the different values a Tile can take
as its content
"""

from enum import Enum


class TileValueEnum(Enum):
    empty = 0
    obstacle = 1
    exit = 2
