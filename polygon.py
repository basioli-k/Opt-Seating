from matplotlib import path

from point import Point
from typing import Sequence, Union
import numpy as np


class Polygon:
    """
        represents the shape of a room
    """

    def __init__(self, points: Sequence[Point]):
        self.points = points
        self._convex = None

    @property
    def convex(self) -> bool:
        if self._convex is None:
            self._convex = self._check_convex()
        return self._convex

    def __len__(self):
        return len(self.points)

    def _check_convex(self) -> bool:
        """
        :return: True if polygon is convex

        Note: polygon must not have consecutive collinear sides
        """
        orient = None
        for ((x1, y1), (x2, y2), (x3, y3)) in zip(
                (*self.points[-2:], *self.points),
                (self.points[-1], *self.points),
                self.points
        ):
            dx1 = x2 - x1
            dy1 = y2 - y1
            dx2 = x3 - x2
            dy2 = y3 - y2

            new_orient = dx1 * dy2 - dy1 * dx2 > 0

            if orient is not None and orient != new_orient:
                return False
            orient = new_orient

        return True

    def __contains__(self, p: Union[Point, 'Polygon']) -> bool:
        if isinstance(p, Point):
            return self._contains_pt(p)

        if not all(pt in self for pt in p.points):  # checks if vertices are contained in self
            return False
        return self.convex or self._contains_poly(p)

    def _contains_pt(self, p: Point) -> bool:
        """
        :param p: point or polygon to check
        :return:  polygon contains p

        a semi-infinite horizontal line is taken from point p
        p is inside the polygon if the number of times the ray intersects the edges of the polygon is odd

        check for intersection:
            if p is above or below both endpoints of the edge the ray doesn't intersect it
            otherwise we check for the relationship between the slopes of the edge and a ray connecting
            the lower point of the edge with the point

        doesn't work for points on the edge of the polygon
        """

        """ 
        todo add or p in self.edges: // not implemented
        """
        return sum(
            (yi > p.y) != (yj > p.y) and p.x < (xj - xi) * (p.y - yi) / (yj - yi) + xi
            for (xi, yi), (xj, yj) in zip(self.points, (self.points[-1], *self.points))
        ) % 2 == 1 or p in self.points

    def _contains_poly(self, poly: 'Polygon') -> bool:
        """
        :param poly: polygon to check
        :return: is poly contained in self
        checks if there is an intersection between between the sides of the two polygons, if they intersect return false
        if both tests are passed return true
        """

        i = 0
        j = len(poly) - 1

        while i < len(poly):
            x1, y1 = tuple(poly.points[i])
            x2, y2 = tuple(poly.points[j])
            k = 0

            l = len(self) - 1
            while k < l:
                x3, y3 = tuple(self.points[k])
                x4, y4 = tuple(self.points[l])

                A = [[x1 - x2, x4 - x3], [y1 - y2, y4 - y3]]
                B = [x4 - x2, y4 - y2]

                if np.linalg.matrix_rank(A) == 2:
                    sol = np.linalg.solve(A, B)
                    if 0 <= min(sol) and max(sol) <= 1:
                        return False

                l = k
                k += 1

            j = i
            i += 1

        return True
