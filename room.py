from abc import ABC

from table import Table
from shapely.geometry import Polygon, Point
from shapely.affinity import translate

import matplotlib.pyplot as plt


class Room(Polygon, ABC):
    """
            represents a room
    """

    def __init__(self, points):
        super(Room, self).__init__(points)  # todo check if convex?
        self.tables = []

    def place(self, table: Polygon):
        centroid = self.centroid.coords[0]

        table = translate(table, *centroid)
        self.tables.append(table)

    def plot(self):
        x, y = self.exterior.xy
        plt.plot(x, y, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

        for t in self.tables:
            t_x, t_y = t.exterior.xy
            plt.plot(t_x, t_y, color='grey', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

        plt.scatter(self.centroid.x, self.centroid.y, color='red')
        plt.show()

