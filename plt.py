from io import BytesIO
from pathlib import Path
from typing import Tuple, Dict

import cv2
import numpy as np
from matplotlib import pyplot as plt

from room import Room
from seating_plan import SeatingPlan
from table import Table
from util import aslist
from visitor import visitor


# def visualize_solution_OLD(room: Room, seating_plan: SeatingPlan, *, show=True, save: str = None):
#     with MatplotlibDrawer() as drawer:
#         drawer(room)
#         drawer(seating_plan)
#         # if save:
#         #     drawer.save(save)
#         if show:
#             buffer = BytesIO()
#             plt.savefig(buffer, format='png')
#             buffer.seek(0)
#             img = cv2.imdecode(np.fromstring(buffer.read(), dtype='uint8'), cv2.IMREAD_UNCHANGED)
#             cv2.imshow('yay', img)
#             cv2.waitKey(delay=1)
#             # drawer.show()

def animate():
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    video = cv2.VideoWriter('./data/animation.avi', fourcc, 2, (600, 600))

    p = Path('data')

    for path in p.glob('*.png'):
        img = cv2.imread(str(path))
        video.write(img)
    video.release()


def visualize_solution(room: Room, seating_plan: SeatingPlan, *, show=True, save: str = None):
    with MatplotlibDrawer() as drawer:
        drawer(room)
        drawer(seating_plan)
        if save:
            drawer.save(save)
        if show:
            drawer.show()


class OpenCVDrawer:
    def __init__(self, **kwargs):
        self.background = kwargs.get('background_bgr', (223, 225, 234))
        self.room_fill = kwargs.get('room_fill', (229, 227, 218))
        self.room_stroke = kwargs.get('room_stroke', self.room_fill)
        self.table_fill = kwargs.get('table_fill', (86, 94, 84))
        self.table_stroke = kwargs.get('table_stroke', (49, 54, 48))
        self.chair_fill = kwargs.get('chair_fill', (146, 148, 183))

        self.canvas = np.full((600, 600, 3), self.background, dtype=np.uint8)

    def _translate_for_cv2(self, xys):
        x_offset = self.canvas.shape[0] // 2 + 1
        y_offset = - self.canvas.shape[1] // 2 - 1

        return tuple((xy[0] / 2 + x_offset, xy[1] / 2 - y_offset) for xy in xys)

    @visitor(Room)
    def __call__(self, room: Room):
        xy = self._translate_for_cv2(room.exterior_xy)
        self.poly(xy, fill=self.room_fill)

        for xy in room.interiors_xy:
            xy = self._translate_for_cv2(xy)
            self.poly(xy, fill=self.background)

    @visitor(SeatingPlan)
    def __call__(self, seating_plan: SeatingPlan):
        for i in range(len(seating_plan.tables)):
            if seating_plan.used_tables_mask[i]:
                self(seating_plan.tables[i])

    @visitor(Table)
    def __call__(self, table: Table):
        xy = self._translate_for_cv2(table.xy)
        self.poly(xy, stroke=self.table_stroke, fill=self.table_fill)

        xy = self._translate_for_cv2(table.chairs_xy)
        self.scatter(xy, color=self.chair_fill)

    def scatter(self, xy, color=(0, 0, 0)):
        for pt in xy:
            cv2.circle(self.canvas, (int(round(pt[0])), int(round(pt[1]))),
                       radius=5,
                       color=color,
                       thickness=-1,
                       lineType=cv2.LINE_AA)

    def poly(self, xy, *, stroke=None, fill=None):
        if stroke:
            cv2.polylines(self.canvas, [np.array(xy, dtype=np.int32)], True, color=stroke, lineType=cv2.LINE_AA)

        if fill:
            cv2.fillPoly(self.canvas, [np.array(xy, dtype=np.int32)], color=fill, lineType=cv2.LINE_AA)

    def show(self):
        cv2.imshow('yay', self.canvas)

    def save(self, path='./data/img.png'):
        cv2.imwrite(path, self.canvas)

    def close(self):
        cv2.waitKey(delay=1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class MatplotlibDrawer:
    def __init__(self):
        self._ax = plt.axes()
        self._ax.set_aspect('equal')

    @visitor(Room)
    def __call__(self, room: Room):
        xy = room.exterior_xy
        self.poly(xy, fill='#dae3e5')

        for xy in room.interiors_xy:
            self.poly(xy, fill='white')

    @visitor(SeatingPlan)
    def __call__(self, seating_plan: SeatingPlan):
        for table in seating_plan.tables:
            self(table)

    @visitor(Table)
    def __call__(self, table: Table):
        x, y = tuple(map(aslist, table._transformed_table.exterior.xy))
        self.poly(list(zip(x, y)), stroke='#303631', fill='#545e56')

        x, y = zip(*table.chairs_xy)
        self.scatter(x, y, color='#b79492')

    def scatter(self, x, y, color: str = 'black'):
        self._ax.scatter(x, y, color=color, zorder=3, s=2)

    def poly(self, xy, *, stroke: str = None, fill: str = None):
        if stroke:
            self._ax.plot(*list(zip(*xy)), color=stroke)
        if fill:
            self._ax.fill(*list(zip(*xy)), color=fill)

    def show(self):
        plt.show()

    def save(self, path='data/img.png'):
        plt.savefig(path)

    def close(self):
        plt.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
