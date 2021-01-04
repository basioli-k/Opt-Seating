from abc import ABC
from shapely.geometry import Polygon, Point


class Table(Polygon, ABC):  # Za sad ne koristimo, ali radi ovako
    """ represents a table """

    def __init__(self, length, width, lw=False):
        if lw:
            super(Table, self).__init__([
                (-length / 2, -width / 2), (-length / 2, width / 2), (length / 2, width / 2), (length / 2, -width / 2)
                ]
            )
        else:  # initialize as a Polygon
            super(Table, self).__init__(length, width)