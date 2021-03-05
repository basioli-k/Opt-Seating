from dataclasses import dataclass

import numpy as np
from shapely.affinity import translate, rotate
from shapely.geometry import Polygon, MultiPoint

from util import with_backing_field, aslist


@dataclass(frozen=True)
class TableTemplate:
    exterior: Polygon
    chairs: MultiPoint

    @property
    def number_of_chairs(self):
        return len(self.chairs)


@dataclass(frozen=True)
class Table:
    template: TableTemplate
    offset_x: float = 0
    offset_y: float = 0
    angle: float = 0

    @property
    @with_backing_field
    def xy(self) -> np.ndarray:
        """
        :return: tuple coordinates (x,y) of points defining the table
        """
        return np.array(
            tuple(
                zip(
                    *map(
                        aslist,
                        self._transformed_table.exterior.xy
                    )
                )
            )
        )

    @property
    @with_backing_field
    def chairs_xy(self):
        """
        :return: tuple of coordinates (x,y) of all chairs around that table
        """
        table_centroid = self.template.exterior.centroid

        return np.array(
            tuple(
                (chair.x, chair.y) for chair in translate(
                    rotate(
                        self.template.chairs,
                        angle=self.angle,
                        origin=table_centroid,
                    ),
                    xoff=self.offset_x,
                    yoff=self.offset_y,
                )
            )
        )

    @property
    @with_backing_field
    def convex_hull(self) -> Polygon:
        return self._transformed_table.union(Polygon(self.chairs_xy))

    @property
    @with_backing_field
    def _transformed_table(self) -> Polygon:
        """
        :return: a Polygon object defined by table_template centered at (self.offset_x, self.offset_y)
                 and rotated by self.angle degrees in positive direction
        """
        return translate(
            rotate(
                self.template.exterior,
                angle=self.angle,
                origin='centroid'
            ),
            xoff=self.offset_x,
            yoff=self.offset_y,
        )

    @property
    def number_of_chairs(self):
        return self.template.number_of_chairs
