from room import Room
from table import Table
from shapely.geometry import Point, Polygon

if __name__ == '__main__':
    room = Room([(0, 3), (-1, 0), (0, -1), (1, 0)])
    table1 = Table([(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)])
    table2 = Table(0.2, 0.2, lw=True)

    room.place(table1)
    room.place(table2)
    room.plot()
