from abc import ABC
from typing import Sequence

from table import Table
from shapely.geometry import Polygon, Point


class Room(Polygon, ABC):
    " represents a room "

    def __init__(self, points: Sequence[Point]):
        Polygon.__init__(self, points)  # todo check if convex?

    def place(self, table: Table):
        centroid = (self.centroid.x, self.centroid.y)
        print(centroid)
        print(table.exterior.coords)
        #todo viditi kako translatirati poligon za neki vektor
