import numpy as np

from dataclasses import dataclass
from typing import Tuple

from table import Table


@dataclass(frozen=True)
class SeatingPlan:
    tables: np.ndarray
    used_tables_mask: np.ndarray

    def used_tables(self):
        return sum(self.used_tables_mask)