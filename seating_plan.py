from dataclasses import dataclass
from typing import Tuple
import numpy as np
from table import Table


@dataclass(frozen=True)
class SeatingPlan:
    tables: Tuple[Table, ...]
    used_tables_mask: np.array([])
    def used_tables(self):
        return np.sum(self.used_tables_mask)


