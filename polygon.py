from typing import Sequence
from point import Point

import numpy as np
import matplotlib.pyplot as plt


class Polygon:
    """
        represents the shape of a room
    """

    def __init__(self, points: Sequence[Point]):
        self.points = points
        self.point_cnt = len(points)
        self.convex = self.check_convex

    def __len__(self):
        return self.point_cnt

    def draw(self, title, points=None):
        pts = list(map(tuple, self.points))
        pts.append(tuple(self.points[0]))

        x, y = list(zip(*pts))

        fig, ax = plt.subplots()
        ax.plot(x, y)

        for x_i, y_i in zip(x, y):
            ax.text(x_i, y_i, f'({x_i},{y_i})')

        if points:
            ax.scatter(*list(zip(*points)), c='r')

        ax.title.set_text(title)
        plt.box(False)
        plt.axis('off')
        plt.show()

    def check_convex(self):
        """
        :return: True if polygon is convex

        Note: polygon must not have consecutive collinear sides
        """

        orient = np.sign(np.cross(self.points[0], self.points[self.point_cnt - 1]))

        for i in range(1, self.point_cnt):
            tmp = np.cross(self.points[i], self.points[i - 1])

            if orient != np.sign(tmp):
                self.convex = False

        self.convex = True

    def __contains__(self, p):
        """
        :param p: point or polygon to check
        :return:  polygon contains p

        a semi-infinite horizontal line is taken from point p
        p is inside the polygon if the number of times the ray intersects the edges of the polygon is odd

        check for intersection:
            if p is above or below both endpoints of the edge the ray doesn't intersect it
            otherwise we check for the relationship between the slopes of the edge and a ray connecting
            the lower point of the edge with the point
        """
        if isinstance(p, Point):
            return self._contains_pt(p)

        elif self.convex:
            return np.logical_and.reduce([pt in self for pt in p.points], 0)

        else:
            'todo'
            return False

    def _contains_pt(self, p: Point):
        """
        :param p: point to check
        :return: whether polygon contains p

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
