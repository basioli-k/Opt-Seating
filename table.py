from abc import ABC
from shapely.geometry import Polygon, Point

#NE KORISTIMO OVO?
class Table(Polygon, ABC):
    """ represents a table """

    def __init__(self, length, width):
        try:
            Polygon.__init__(self, list(map(Point, [
                (-length / 2, -width / 2), (-length / 2, width / 2), (length / 2, width / 2), (length / 2, -width / 2) ]
                                            )
                                        )
            )
        except:
            try:
                Polygon.__init__(self, length)
            except:
                raise ValueError




