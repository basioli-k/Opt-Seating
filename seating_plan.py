from dataclasses import dataclass
from typing import Tuple
import numpy as np
from table import Table


@dataclass(frozen=True)
class SeatingPlan:
    tables: Tuple[Table, ...]
    used_tables_mask: np.array([])

    def no_of_used_tables(self):
        return np.count_nonzero(self.used_tables_mask)