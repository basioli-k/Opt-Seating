from abc import ABC
from typing import Sequence

from table import Table
from shapely.geometry import Polygon, Point
from shapely.affinity import translate


class Room(Polygon, ABC):
    " represents a room "

    def __init__(self, points: Sequence[Point]):
        Polygon.__init__(self, points)  # todo check if convex?
        self.tables = []

    def place(self, table: Table):
        centroid = (self.centroid.x, self.centroid.y)
        print(centroid)
        print(table.exterior.coords[:])
        #todo viditi kako translatirati poligon za neki vektor
        #table = translate(table, centroid[0], centroid[1])
        #print(table.exterior.coords[:])
        #self.table.append(table)

