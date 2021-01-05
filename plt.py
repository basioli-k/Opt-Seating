from typing import Union, Tuple

from room import Room
from table import Table
from table_group import SelectionFromTableGroup, SeatingPlan

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
                SelectionFromTableGroup,
                SeatingPlan,
            ],
            translation: Tuple[float, float] = (0, 0),
            rotation: float = 0
    ):
        if isinstance(obj, SeatingPlan):
            for group in obj._groups:  # todo eskopelja FIX!!!
                self.__call__(group)
            return

        if isinstance(obj, SelectionFromTableGroup):
            for t, r in zip(obj.translations, obj.rotations):
                self.__call__(obj._template, translation=t, rotation=r) # todo eskopelja FIX!!!
            return

        if isinstance(obj, Room):
            x, y = obj.exterior_xy()
            self._ax.fill(x, y, color='#dae3e5')

            for x, y in obj.interiors_xy():
                self._ax.fill(x, y, color='white')

        elif isinstance(obj, Table):
            t_x, t_y = obj.table_exterior_xy(xoff=translation[0],
                                             yoff=translation[1],
                                             angle=rotation)
            self._ax.plot(t_x, t_y, color='#303631')
            self._ax.fill(t_x, t_y, color='#545e56')

            x, y = obj.chairs_xy(xoff=translation[0],
                                 yoff=translation[1],
                                 angle=rotation)
            self._ax.scatter(x, y, color='#b79492', zorder=3, s=20)

        else:
            raise NotImplementedError(f"Don't know how to draw {type(obj)}")

    def scatter(self, x, y, color: str = 'black'):
        self._ax.scatter(x, y, color=color, zorder=3, s=50)

    def plot(self, x, y, *, stroke: str = 'black', fill: str = 'grey'):
        self._ax.plot(x, y, color=stroke)
        self._ax.fill(x, y, color=fill)

    def show(self):
        plt.show()
