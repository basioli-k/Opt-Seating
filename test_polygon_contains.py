from point import Point
from polygon import Polygon

if __name__ == "__main__":
    q = Polygon([Point(20, 10),
                 Point(50, 125),
                 Point(125, 90),
                 Point(150, 10)])

    # Test 1: Point inside of polygon
    p1 = Point(75, 50)
    assert q.__contains__(p1)

    # Test 2: Point outside of polygon
    p2 = Point(200, 50)
    assert not q.__contains__(p2)

    # Test 3: Point at same height as vertex
    p3 = Point(35, 90)
    assert not q.__contains__(p3)

    # Test 4: Point on bottom line of polygon
    p4 = Point(50, 10)
    assert q.__contains__(p4)
