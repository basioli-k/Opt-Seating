from abc import ABC
from shapely.geometry import Polygon, Point


class Table(Polygon, ABC):
    " represents a table in a room "

    def __init__(self, length, width):
        Polygon.__init__(self,
                         [Point(-length / 2, -width / 2), Point(-length / 2, width / 2), Point(length / 2, width / 2),
                          Point(length / 2, -width / 2)])
