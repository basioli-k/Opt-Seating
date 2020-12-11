from point import Point
from typing import Sequence
import numpy as np

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

    #function is always called by a table which cannot contain a room
    def containedIn(self, poly):

        """
        :param poly: polygon to check
        :return: is self contained in poly

        checks if a vertex from self iz contained in poly, if it isn't then it returns false

        checks if there is an intersection between between the sides of the two polygons, if they intersect return false

        if both tests are passed return true
        """

        for point in self.points:   #todo improve this?
            if point not in poly:
                return False
        i = 0
        j = self.point_cnt -1

        while i < self.point_cnt:
            x1 = self.points[i].x
            y1 = self.points[i].y
            x2 = self.points[j].x
            y2 = self.points[j].y
            k = 0
            
            l = poly.point_cnt -1
            while k < poly.point_cnt -1:
                x3 = poly.points[k].x
                y3 = poly.points[k].y
                x4 = poly.points[l].x
                y4 = poly.points[l].y
                
                A = [[x1-x2,x4-x3],[y1-y2,y4-y3]]
                B = [x4-x2,y4-y2]
                
                if(np.linalg.matrix_rank(A) == 2):
                    sol = np.linalg.solve(A,B)
                    if( 0 <= sol[0] and sol[0] <= 1 and 0 <= sol[1] and sol[1] <= 1):
                        return False
                
                l = k
                k+=1
            
            j=i
            i+=1
        
        return True
