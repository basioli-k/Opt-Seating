import numpy as np

from dataclasses import dataclass

from util import with_backing_field


@dataclass(frozen=True)
class SeatingPlan:
    tables: np.ndarray
    used_tables_mask: np.ndarray
    room_y: float

    def used_tables(self):
        return sum(self.used_tables_mask)

    def __hash__(self):
        ys = [table.offset_y for table in self.tables[self.used_tables_mask]]
        hist = np.histogram(ys, bins=10, range=(-self.room_y // 2, self.room_y // 2))
        return int(sum(d * 10 ** i for i, d in enumerate(hist[0][::-1])))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()