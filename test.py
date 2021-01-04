from room import Room
from table import Table
from shapely.geometry import Point, Polygon

if __name__ == '__main__':
    room = Room(list(map(Point, [(0, 3), (-1, 0), (0, -1), (1, 0)])))
    table = Polygon(list(map(Point, [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)])))

    room.place(table)
    room.plot()
