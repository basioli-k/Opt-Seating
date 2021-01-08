import itertools
from dataclasses import dataclass
from typing import Tuple

import numpy as np
from scipy.linalg import block_diag
from shapely.geometry import Polygon

from room import Room
from seating_plan import SeatingPlan
from table import Table


def harmonic_mean(arr: np.ndarray) -> float:
    return arr.size / np.sum(1 / arr)


def harmonic_mean_of_worst(arr: np.ndarray, worst_ratio: float = 0.1) -> float:
    return harmonic_mean(np.sort(arr)[:int(round(worst_ratio * arr.size))])


def chairs_np(tables: Tuple[Table, ...]) -> np.ndarray:
    return np.array(tuple(xy for table in tables for xy in table.chairs_xy))


def calculate_mask_different_table(tables: Tuple[Table, ...]):
    return np.logical_not(
        block_diag(*(
            np.ones((number_of_chairs, number_of_chairs), dtype='bool')
            for number_of_chairs in (table.number_of_chairs for table in tables)
        ))
    )


@dataclass(frozen=True)
class Evaluator:
    room: Room
    chair_distance_threshold: float = 200

    def __call__(self, seating_plan: SeatingPlan) -> float:
        chair_distance_fitness = self._chair_distance_fitness(seating_plan)

        tables_in_room_fitness = self._tables_room_distance_fitness(seating_plan)

        tables_not_overlapping_fitness = 0  # self._tables_distance_fitness(seating_plan)

        return chair_distance_fitness + tables_in_room_fitness + tables_not_overlapping_fitness

    def _tables_room_distance_fitness(self, seating_plan: SeatingPlan) -> float:
        return sum(map(lambda x: x, map(self._table_room_distance_fitness, seating_plan.tables)))

    def _table_room_distance_fitness(self, table: Table) -> float:
        room_poly = self.room.poly
        convex_hull = table.convex_hull
        if room_poly.contains(convex_hull):
            return 0
        if room_poly.intersects(convex_hull):
            ioa = room_poly.intersection(convex_hull).area / convex_hull.area
            assert 0 < ioa < 1
            fitness = -self.chair_distance_threshold * (2 - ioa)
            assert -2 * self.chair_distance_threshold < fitness < -self.chair_distance_threshold
            return fitness
        return -2 * self.chair_distance_threshold - room_poly.distance(convex_hull)

    def _chair_distance_fitness(self, seating_plan: SeatingPlan) -> float:
        mask_different_table = calculate_mask_different_table(seating_plan.tables)
        chairs = chairs_np(seating_plan.tables)

        distances = np.sqrt(np.sum(np.square(np.expand_dims(chairs, axis=0) - np.expand_dims(chairs, axis=1)), axis=-1))

        closest_distances = np.min(np.where(mask_different_table, distances, np.inf), axis=-1)

        # after 2m everything is OK
        closest_distances = np.minimum(closest_distances, self.chair_distance_threshold)

        closest_distances = harmonic_mean(closest_distances)
        return closest_distances - self.chair_distance_threshold

    def _tables_distance_fitness(self, seating_plan: SeatingPlan) -> float:
        chs = [table.convex_hull for table in seating_plan.tables]
        return sum(
            self._table_table_distance_fitness(ch1, ch2) for ch1, ch2 in itertools.combinations(chs, 2)
        )

    def _table_table_distance_fitness(self, ch1: Polygon, ch2: Polygon) -> float:
        if not ch1.intersects(ch2):
            return 0
        intersection = ch1.intersection(ch2).area
        return -self.chair_distance_threshold * (2 - intersection / ch1.area) if intersection > 0 else 0
