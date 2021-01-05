from functools import reduce
from typing import Tuple, Sequence

import numpy as np

from table import Table


class SelectionFromTableGroup:

    def __init__(self, template: Table, available: int):
        self._template = template
        self._available = available
        self._translations = []
        self._rotations = []

    def add(self, translation: Tuple[float, float] = (0, 0), rotation: float = 0):
        if self._available == 0:
            return

        self._translations.append(translation)
        self._rotations.append(rotation)
        self._available -= 1

    def num_selected(self):
        return len(self._translations)

    def ppl_per_table(self):
        return self._template.chair_number()

    def num_ppl(self):
        return self.num_selected() * self.ppl_per_table()

    def translations(self):
        return tuple(self._translations)

    def rotations(self):
        return tuple(self._rotations)

    def chairs_xy(self):
        return reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]),
                      [
                          self._template.chairs_xy(
                              xoff=xoff,
                              yoff=yoff,
                              angle=angle,
                          )
                          for xoff, yoff, angle in zip(*zip(*self._translations), self._rotations)
                      ]
                      )

    def tables_xy(self):
        r = tuple(
            self._template.table_exterior_xy(
                xoff=xoff,
                yoff=yoff,
                angle=angle,
            ) for xoff, yoff, angle in zip(*zip(*self._translations), self._rotations))

        return r

    def visit(self, visitor):
        visitor(self)


class SelectionGrouped:
    def __init__(self, groups: Sequence[SelectionFromTableGroup]):
        self._groups = groups

    def num_ppl(self):
        return sum(group.num_ppl() for group in self._groups)

    def chairs_xy(self):
        return reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), [group.chairs_xy() for group in self._groups])

    def tables_xy(self):
        return reduce(lambda a, b: a + b, [group.tables_xy() for group in self._groups])

    def mask_same_table(self):
        total = self.num_ppl()
        mask = np.zeros((total, total), dtype=bool)

        offset = 0
        for group in self._groups:
            ppl_in_group = group.num_ppl()
            tables_in_group = group.num_selected()
            per_table = group.ppl_per_table()

            mask[offset:offset + ppl_in_group, offset:offset + ppl_in_group] = np.kron(
                np.eye(tables_in_group, dtype=bool),
                np.ones((per_table, per_table), dtype=bool))

            offset += ppl_in_group
        return mask

