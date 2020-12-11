from point import Point
from typing import Sequence


class Polygon:
    """
        represents the shape of a room
    """
    def __init__(self, points: Sequence[Point]):
        self.points = points
        self.point_cnt = len(points)

    """ 
    todo:
    def __is_convex__(self):
    """

    def __contains__(self, p: Point):
        """
        :param p: point to check
        :return:  polygon contains point p

        a semi-infinite horizontal line is taken from point p
        p is inside the polygon if the number of times the ray intersects the edges of the polygon is odd

        check for intersection:
            if p is above or below both endpoints of the edge the ray doesn't intersect it
            otherwise we check for the relationship between the slopes of the edge and a ray connecting
            the lower point of the edge with the point
        """
        contains = False

        i = 0
        j = self.point_cnt - 1

        while i < self.point_cnt:
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y

            if (y1 > p.y) != (y2 > p.y) and p.x < (x2-x1) * (p.y - y1) / (y2 - y1) + x1:
                contains = not contains

            j = i
            i += 1

        return contains

