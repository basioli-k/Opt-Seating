from io import BytesIO
from pathlib import Path
from typing import Union

import cairosvg
import svgwrite

from room import Room
from table import Table

from matplotlib import pyplot as plt

from PIL import Image


class Svg:
    def __init__(self, filename: str = 'test.svg'):
        self._dwg = svgwrite.Drawing(filename, size=('800px', '600px'))
        self._boundaries = (0, 0, 0, 0)

    def _update_boundaries(self, xs, ys):
        x1, y1, x2, y2 = self._boundaries
        for x, y in zip(xs, ys):
            x1 = min(x, x1)
            y1 = min(y, y1)
            x2 = max(x, x2)
            y2 = max(y, y2)
        self._boundaries = x1, y1, x2, y2

    def __call__(
            self,
            obj: Union[
                Room,
                Table,
            ],
    ):
        if isinstance(obj, Room):
            self._poly(*obj.exterior_xy(), stroke='#557177', fill='#dae3e5', stroke_width=3)

            for x, y in obj.interiors_xy():
                self._poly(x, y, stroke='#557177', fill='white', stroke_width=3)

        elif isinstance(obj, Table):
            self._poly(*obj.table_exterior_xy(), fill='#545e56', stroke='#303631', stroke_width=3)

            for x, y in zip(*obj.chairs_xy()):
                self._circle(x, y, r=20, fill='#b79492')

        else:
            raise NotImplementedError(f"Don't know how to draw {type(obj)}")

    def _poly(self, xs, ys, **kwargs):
        self._update_boundaries(xs, ys)
        self._dwg.add(self._dwg.polyline(zip(map(round, xs), map(round, ys)), **kwargs))

    def _circle(self, x, y, r: int, **kwargs):
        self._update_boundaries([x], [y])
        self._dwg.add(self._dwg.circle((round(x), round(y)), r=r, **kwargs))

    def save(self):
        x1, y1, x2, y2 = self._boundaries
        self._dwg['viewBox'] = f'{x1} {y1} {x2 - x1} {y2 - y1}'
        self._dwg.save()
        out = BytesIO()
        cairosvg.svg2png(url=self._dwg.filename, write_to=out)
        plt.imshow(Image.open(out))
        plt.show()
