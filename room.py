from abc import ABC
from typing import Sequence

from table import Table
from shapely.geometry import Polygon, Point
from shapely.affinity import translate

import matplotlib.pyplot as plt


class Room(Polygon, ABC):
    """
            represents a room
    """

    def __init__(self, points: Sequence[Point]):
        Polygon.__init__(self, points)  # todo check if convex?
        self.tables = []

    def place(self, table: Polygon):
        centroid = (self.centroid.x, self.centroid.y)
        x, y = self.exterior.xy

        table = translate(table, *centroid)
        self.tables.append(table)

        #crtanje
        #t_x, t_y = table.exterior.xy
        #plt.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
        #plt.plot(t_x, t_y, color='grey', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
        #plt.scatter(self.centroid.x, self.centroid.y, color='red')
        #plt.show()

