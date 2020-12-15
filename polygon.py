from point import Point
from typing import Sequence
import numpy as np


class Polygon:
    """
        represents the shape of a room
    """

    def __init__(self, points: Sequence[Point]):
        self.points = points
        self.convex = self.check_convex

    def __len__(self):
        return len(self.points)

    def check_convex(self):
        """
        :return: True if polygon is convex

        Note: polygon must not have consecutive collinear sides
        """
        orient = np.sign(np.cross(self.points[0], self.points[len(self) - 1]))

        for i in range(1, len(self)):
            tmp = np.cross(self.points[i], self.points[i - 1])

            if orient != np.sign(tmp):
                self.convex = False

        self.convex = True

    def __contains__(self, p):
        if isinstance(p, Point):
            return self._contains_pt(p)

        if not np.logical_and.reduce([pt in self for pt in p.points], 0):  # checks if vertices are contained in self
            return False
        elif self.convex:
            return True
        else:
            return self._contains_poly(p)

    def _contains_pt(self, p: Point):
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
        contains = False

        i = 0
        j = len(self) - 1
        while i < len(self):
            xi, yi = tuple(self.points[i])
            xj, yj = tuple(self.points[j])

            if (yi > p.y) != (yj > p.y) and p.x < (xj - xi) * (p.y - yi) / (yj - yi) + xi:
                contains = not contains

            j = i
            i += 1

        """
        ---> myb add later 

        if not contains:
            if p in self.points:
                return True
            if p in self.edges: // not implemented
                return True
        """
        return contains

    def _contains_poly(self, poly):
        """
        :param poly: polygon to check
        :return: is poly contained in self
        checks if there is an intersection between between the sides of the two polygons, if they intersect return false
        if both tests are passed return true
        """

        i = 0
        j = poly.point_cnt - 1

        while i < poly.point_cnt:
            x1 = poly.points[i].x
            y1 = poly.points[i].y
            x2 = poly.points[j].x
            y2 = poly.points[j].y
            k = 0

            l = len(self) - 1
            while k < len(self) - 1:
                x3 = self.points[k].x
                y3 = self.points[k].y
                x4 = self.points[l].x
                y4 = self.points[l].y

                A = [[x1 - x2, x4 - x3], [y1 - y2, y4 - y3]]
                B = [x4 - x2, y4 - y2]

                if np.linalg.matrix_rank(A) == 2:
                    sol = np.linalg.solve(A, B)
                    if 0 <= min(sol[0], sol[1]) and max(sol[0], sol[1]) <= 1:
                        return False

                l = k
                k += 1

            j = i
            i += 1

        return True
