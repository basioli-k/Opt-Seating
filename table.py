from typing import Sequence, Tuple

from shapely.affinity import translate
from shapely.geometry import Polygon, Point


class Table:
    def __init__(
            self,
            *,
            table: Polygon,
            chairs: Sequence[Point],
    ):
        self._table = table
        self._chairs = tuple(chairs)

    def translate(self, x: float, y: float) -> 'Table':
        return self.__class__(
            table=translate(
                self._table,
                xoff=x,
                yoff=y,
            ),
            chairs=tuple(
                translate(
                    chair,
                    xoff=x,
                    yoff=y,
                )
                for chair in self._chairs
            ),
        )

    def visit(self, visitor):
        visitor(self)

    def table_exterior_xy(self):
        return self._table.exterior.xy

    def chairs_xy(self):
        return tuple(zip(*((chair.x, chair.y) for chair in self._chairs))) if self._chairs else ((), ())
