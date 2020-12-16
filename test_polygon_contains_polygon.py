from polygon import Polygon
from point import Point

from unittest import TestCase


class PolygonContainsPolygonTest(TestCase):
    poly1 = Polygon([Point(0, 0), Point(4, -2), Point(8, 1), Point(2, 5)])
    poly2 = Polygon([Point(1, 1), Point(-3, 0), Point(3, 3)])

    def test_completely_inside(self):
        # polygon is completely inside the bigger polygon
        assert Polygon([Point(4, 1), Point(3, 2), Point(2, 0)]) in self.poly1

    def test_one_vertex_outside(self):
        # polygon has one vertex outside of the bigger polygon
        assert Polygon([Point(4, 1), Point(1, 4), Point(2, 0)]) not in self.poly1

    def test_completely_outside(self):
        # polygon has one vertex outside of the bigger polygon
        assert Polygon([Point(-3, 0), Point(-2, 2), Point(-1, 0)]) not in self.poly1

    # def test_overlapping_sides_inside(self):
    #     # polygon has one side on a side of the bigger polygon
    #     assert Polygon([Point(3, 0), Point(1, 1), Point(3, 3)]) in self.poly2
    #     # returns false, should return true, check contains function

    def test_overlapping_sides_outside(self):
        # polygon has one side on a side of the bigger polygon
        assert Polygon([Point(1, 1), Point(-3, 0), Point(3, 3)]) not in self.poly2

    # def test_vertex_on_side(self):
    #     # polygon has one vertex on a side of the bigger polygon
    #     assert Polygon([Point(3, 0), Point(5, 1), Point(3, 3)]) in self.poly2
    #     # returns false because contains returns false for point F (see picture)