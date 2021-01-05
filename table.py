from typing import Sequence, Tuple

from shapely.affinity import translate, rotate
from shapely.geometry import Polygon, Point

from util import aslist


class Table:
    def __init__(
            self,
            *,
            table: Polygon,
            chairs: Sequence[Point],
    ):
        self._table = table
        self._chairs = tuple(chairs)

    def visit(self, visitor):
        visitor(self)

    def table_exterior_xy(self, *, xoff: float = 0, yoff: float = 0, angle: float = 0):
        """
        :param xoff: translation offset on the x axis in cm
        :param yoff: translation offset on the y axis in cm
        :param angle: angle in degrees
        :return: x,y coordinates of points in the table
        """
        return tuple(map(aslist, translate(
            rotate(
                self._table,
                angle=angle,
                origin='centroid'
            ),
            xoff=xoff,
            yoff=yoff,
        ).exterior.xy))

    def chairs_xy(self, *, xoff: float = 0, yoff: float = 0, angle: float = 0):
        """
        :param xoff: translation offset on the x axis in cm
        :param yoff: translation offset on the y axis in cm
        :param angle: angle in degrees
        :return: x,y coordinates of all chairs associated with the table
        """
        transformed = tuple(
            translate(
                rotate(
                    chair,
                    angle=angle,
                    origin=self._table.centroid
                ),
                xoff=xoff,
                yoff=yoff,
            )
            for chair in self._chairs
        )

        return tuple(zip(*((chair.x, chair.y) for chair in transformed))) if transformed else ((), ())

    def chair_number(self):
        return len(self._chairs)
