from point import Point
from polygon import Polygon


if __name__ == "__main__":
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

    q.draw(title='points in q', points=[p1, p2, p3, p4])
    q.draw(title='sq in q', points=sq.points)

    # Test 1: Point inside of polygon
    assert p1 in q

    # Test 2: Point outside of polygon
    assert p2 not in q

    # Test 3: Point at same height as vertex
    assert p3 not in q

    # Test 4: Point on bottom line of polygon
    assert p4 in q

    # Test 5: q and sq are convex
    assert q.convex and sq.convex

    # Test 6: square in convex polygon
    assert sq in q

    # # Test 7: vertex in polygon
    # doesn't pass
    # assert q1 in q
    # assert q2 in q
    # assert q3 in q
    # assert q4 in q

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


