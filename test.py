from room import Room
from table import Table


room = Room([(0, 3), (-1, 0), (0, -1), (1, 0)])
table = Table(0.5,0.5)

room.place(table)
