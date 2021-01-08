from dataclasses import dataclass
from typing import Tuple

from table import Table


@dataclass(frozen=True)
class SeatingPlan:
    tables: Tuple[Table, ...]
    used_tables_mask: Tuple[bool, ...]

