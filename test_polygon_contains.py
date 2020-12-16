from point import Point
from polygon import Polygon

from unittest import TestCase


class PolygonContainsTest(TestCase):
    q1 = Point(20, 10)
    q2 = Point(50, 125)
    q3 = Point(125, 90)
    q4 = Point(150, 10)

    q = Polygon([q1, q2, q3, q4])

    sq = Polygon([Point(50, 20),
                 Point(50, 50),
                 Point(60, 50),
                 Point(60, 20)])

    p1 = Point(75, 50)  # point inside of polygon
    p2 = Point(200, 50)  # point outside of polygon
    p3 = Point(35, 90)  # point at same height as vertex
    p4 = Point(50, 10)  # point on edge of polygon

    def test_point_inside(self):
        assert self.p1 in self.q

    def test_point_outside(self):
        assert self.p2 not in self.q

    def test_point_at_same_height_as_vertex(self):
        assert self.p3 not in self.q

    def test_point_on_edge_of_polygon(self):
        assert self.p4 in self.q

    def test_q_convex(self):
        assert self.q.convex

    def test_sq_convex(self):
        assert self.sq.convex

    def test_polygon_in_convex_polygon(self):
        assert self.sq in self.q

    def test_vertex_in_polygon(self):
        assert self.q1 in self.q and self.q2 in self.q and self.q3 in self.q and self.q4 in self.q

    # # Test 8: points on edge of polygon
    # doesn't pass
    # p5 = Point(50, 25)
    # p6 = Point(60, 25)
    # p7 = Point(55, 20)
    # p8 = Point(55, 50)
    # sq.draw(title='points in sq', points=[p5, p6, p7, p8])
    # assert p5 in sq
    # assert p6 in sq
    # assert p7 in sq
    # assert p8 in sq


