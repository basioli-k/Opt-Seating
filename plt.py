from typing import Union

from room import Room
from table import Table

from matplotlib import pyplot as plt


class MatplotlibDrawer:
    def __init__(self):
        self._ax = plt.axes()
        self._ax.set_aspect('equal')

    def __call__(
            self,
            obj: Union[
                Room,
                Table,
            ],
    ):
        if isinstance(obj, Room):
            x, y = obj.exterior_xy()
            self._ax.plot(x, y, color='#6699cc')
            for x, y in obj.interiors_xy():
                self._ax.fill(x, y, color='#6699cc')

        elif isinstance(obj, Table):
            t_x, t_y = obj.table_exterior_xy()
            self._ax.plot(t_x, t_y, color='grey')

            x, y = obj.chairs_xy()
            self._ax.scatter(x, y, color='pink', zorder=3, s=3)

        else:
            raise NotImplementedError(f"Don't know how to draw {type(obj)}")

    def show(self):
        plt.show()
