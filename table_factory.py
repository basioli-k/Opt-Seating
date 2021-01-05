from typing import Sequence, Tuple, Any

from shapely.geometry import Polygon, Point

from table import Table
from util import xy_combinations, with_dimensions


def create_rect(
        *,
        width: float,
        height: float,
        chairs: Sequence[Tuple[float, float]],
):
    return Table(
        table=Polygon(xy_combinations(
            x=width / 2,
            y=height / 2,
        )),
        chairs=tuple(Point(*xy) for xy in chairs),
    )


def create_2020(
        *,
        width: float,
        height: float,
        chair_offset: float = 30,
):
    return create_rect(
        width=width,
        height=height,
        chairs=xy_combinations(
            x=width / 4,
            y=height / 2 + chair_offset,
        ),
    )


def create_2222(
        *,
        width: float,
        height: float,
        chair_offset: float = 30,
):
    return create_rect(
        width=width,
        height=height,
        chairs=xy_combinations(
            x=width / 4,
            y=height / 2 + chair_offset,
        ) + xy_combinations(
            x=width / 2 + chair_offset,
            y=height / 4,
        ),
    )


@with_dimensions
def create(name: str, **kwargs: Any) -> Table:
    return globals()['create_' + name](**kwargs)


def create_multiple(n: int, name: str, **kwargs):
    return tuple(create(name, **kwargs) for _ in range(n))
