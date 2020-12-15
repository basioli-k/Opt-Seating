from polygon import Polygon
from point import Point

if __name__ == "__main__":
    poly = Polygon([Point(0, 0), Point(4, -2), Point(8, 1), Point(2, 5)])

    # test 1  polygon is completely inside the bigger polygon
    test1 = Polygon([Point(4, 1), Point(3, 2), Point(2, 0)])

    assert test1 in poly

    # test 2  polygon has one vertex outside of the bigger polygon
    test2 = Polygon([Point(4, 1), Point(1, 4), Point(2, 0)])

    assert test2 not in poly

    # test 3  polygon is completely outside the bigger polygon
    test3 = Polygon([Point(-3, 0), Point(-2, 2), Point(-1, 0)])

    assert test3 not in poly

    # test 4  polygon has one side on a side of the bigger polygon
    poly = Polygon([Point(0, 0), Point(4, -2), Point(8, 1), Point(4, 4)])
    test4 = Polygon([Point(3, 0), Point(1, 1), Point(3, 3)])

    assert test4 in poly
    # ------------------------ PROVJERI OVO, NIJE RADILO PRIJE ---------------
    # returns false, should return true, check contains function

    # test 5 polygon has one vertex on a side of the bigger polygon
    test5 = Polygon([Point(3, 0), Point(5, 1), Point(3, 3)])

    assert test5 in poly
    # ------------------------ PROVJERI OVO, NIJE RADILO PRIJE ---------------
    # returns false because contains returns false for point F (see picture)

    # test 6 polygon shares a side but is outside of the bigger polygon
    test6 = Polygon([Point(1, 1), Point(-3, 0), Point(3, 3)])

    assert test6 not in poly
