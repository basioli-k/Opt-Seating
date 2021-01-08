import random
from dataclasses import dataclass, replace
from typing import Iterable, Tuple

import numpy as np

from room import Room
from seating_plan import SeatingPlan
from table import Table
from visitor import visitor
from scipy.spatial import Voronoi


def most_distant_enclosed_points(xys):
    """
    :param xys: points in a plane
    :return: a selection of points sorted by decreasing distance from xys
    """
    candidates = Voronoi(xys).vertices

    distances = np.square(np.expand_dims(xys, axis=1) - np.expand_dims(candidates, axis=0)).sum(axis=-1)

    indices = distances.min(axis=0).argsort()[::-1]

    return zip(candidates[indices], distances.argmin(axis=0)[indices])


def table_centroids_np(tables: Tuple[Table, ...]) -> np.ndarray:
    """
    :param tables: tuple of tables
    :return: numpy array of (x,y) pairs of table centroid coordinates
    """
    return np.array(tuple((table.offset_x, table.offset_y) for table in tables))


def _move_away_from(seating_plan: SeatingPlan) -> np.ndarray:
    """
    :param seating_plan
    :return: for each table in the seating plan, returns the centroid of a table closest to it
    """
    centroids = table_centroids_np(seating_plan.tables)

    directions = np.expand_dims(centroids, axis=0) - np.expand_dims(centroids, axis=1)
    closest_distances_index = np.argmin(
        np.sum(
            np.square(directions),
            axis=-1
        ) + 100_000 * np.eye(directions.shape[0]),
        axis=-1
    )

    return directions[tuple(zip(*enumerate(closest_distances_index)))]


class Offsets:
    def __init__(self, seating_plan: SeatingPlan):
        self.offsets = _move_away_from(seating_plan)

    def __call__(self):
        yield from self.offsets


class Mutator:
    def __init__(self,
                 room: Room,
                 table_mutation_probability: float = 0.1,

                 table_mutation_offset_stdev: float = 30,
                 table_distancing_factor: float = 2,
                 prefer_gauss_move_ratio: float = .7,

                 table_mutation_angle_sigma: float = 10,

                 used_tables_mutation_probability: float = 0.01):
        """
        :param room:

        :param table_mutation_probability: probability of changing a table in the seating plan
        :param prefer_gauss_move_ratio: ratio of gauss moves (move in a randomly selected direction sampled from a random
                                            normal distribution) vs. moves away from closest table
        :param table_mutation_offset_stdev: standard deviation of a gaussian move
        :param table_distancing_factor: scale factor for table distancing from its nearest neighbour
        :param table_mutation_angle_sigma: standard deviation of table rotation change sampled from a random
                                            normal distribution

        :param used_tables_mutation_probability: unused,
            @todo add option to select a subset of tables to include in the seating plan
        """
        self.room = room

        self.table_mutation_probability = table_mutation_probability
        self.table_mutation_offset_stdev = table_mutation_offset_stdev
        self.table_distancing_factor = table_distancing_factor
        self.prefer_gauss_move_ratio = prefer_gauss_move_ratio

        self.table_mutation_angle_sigma = table_mutation_angle_sigma

        self.used_tables_mutation_probability = used_tables_mutation_probability

        self.offsets = None

    @visitor(SeatingPlan)
    def __call__(self, seating_plan: SeatingPlan) -> Iterable[SeatingPlan]:
        self.offsets = Offsets(seating_plan)
        yield from map(
            self.maybe_swap_tables,
            self.maybe_voronoi(
                replace(
                    seating_plan,
                    tables=tuple(
                        self._mv_table(table) if random.random() < self.table_mutation_probability else table
                        for table in seating_plan.tables
                    ),
                    used_tables_mask=tuple(
                        bit ^ (random.random() < self.used_tables_mutation_probability)
                        for bit in seating_plan.used_tables_mask
                    ),
                )
            )
        )

    def _mv_table(self, table: Table) -> Table:
        new_x, new_y = self._mv_gaussian(table) if random.random() < self.prefer_gauss_move_ratio \
            else self._mv_from_closest_table(table)

        return replace(
            table,
            offset_x=new_x,
            offset_y=new_y,
            angle=(
                (table.angle + random.normalvariate(0, self.table_mutation_angle_sigma)) % 360
                if random.random() < 0.95
                else (table.angle + random.randrange(0, 360, 45)) % 360
            )
        )

    def _mv_gaussian(self, table: Table) -> Tuple[float, float]:
        return table.offset_x + random.normalvariate(0, self.table_mutation_offset_stdev), \
               table.offset_y + random.normalvariate(0, self.table_mutation_offset_stdev)

    def _mv_from_closest_table(self, table: Table) -> Tuple[float, float]:
        mv_from_x, mv_from_y = next(self.offsets())

        if mv_from_x == table.offset_x or mv_from_x == table.offset_x:
            return self._mv_gaussian(table)

        ratio = self.table_distancing_factor
        new_x = (1 + ratio) * table.offset_x + (-ratio) * mv_from_x
        new_y = (1 + ratio) * table.offset_y + (-ratio) * mv_from_y

        return new_x, new_y

    def maybe_voronoi(self, seating_plan: SeatingPlan) -> Iterable[SeatingPlan]:
        """
        :param seating_plan
        :return: with 50% chance generate a new seating plan with a randomly selected table moved towards
                 a 'hole' in the seating plan closest to it
        """
        if random.random() < 0.5:
            yield seating_plan
            return

        xys = tuple(zip(*self.room.poly.exterior.xy)) + tuple(
            xy
            for interior in self.room.poly.interiors
            for xy in zip(*interior.xy)
        ) + tuple(
            xy
            for table in seating_plan.tables
            for xy in zip(*table.convex_hull.exterior.xy)
        )

        for _, ((x, y), table_idx) in zip(range(1), most_distant_enclosed_points(np.array(xys))):
            tables = seating_plan.tables
            i = random.randint(0, len(tables) - 1)
            yield replace(
                seating_plan,
                tables=tuple(
                    replace(
                        table,
                        offset_x=x,
                        offset_y=y,
                    ) if i == j else table
                    for j, table in enumerate(tables)
                ),
            )
            yield replace(
                seating_plan,
                tables=tuple(
                    replace(
                        table,
                        offset_x=table.offset_x * 0.9 + x * 0.1,
                        offset_y=table.offset_y * 0.9 + y * 0.1,
                    ) if table_idx == j else table
                    for j, table in enumerate(tables)
                )
            )

    def maybe_swap_tables(self, seating_plan: SeatingPlan) -> SeatingPlan:
        if not random.random() < 0.25:
            return seating_plan

        tables = seating_plan.tables
        j = random.randint(0, len(tables) - 1)
        k = random.randint(0, len(tables) - 1)
        return replace(
            seating_plan,
            tables=tuple(
                replace(
                    table,
                    template=tables[j if i == k else k].template,
                    angle=tables[j if i == k else k].angle,
                ) if i in (j, k) else table for i, table in enumerate(tables)
            )
        )
