from typing import Tuple, Any, Iterable

from shapely.geometry import MultiPoint, Polygon

from table import Table, TableTemplate
from util import xy_combinations, with_dimensions


def _create_rect(
        *,
        width: float,
        height: float,
        chairs: Tuple[Tuple[float, float], ...],
):
    return TableTemplate(
        exterior=Polygon(xy_combinations(
            x=width / 2,
            y=height / 2,
        )),
        chairs=MultiPoint(chairs),
        width=width,
        height=height
    )


def fixed(
        *,
        length: float,
        number: int,
) -> Iterable[float]:
    if number == 0:
        return ()
    inc = length / (2 * number)
    initial = - length / 2
    return (initial + inc * i for i in range(1, 2 * number, 2))


def x_fixed(
        *,
        x,
        height: float,
        number: int,
) -> Iterable[Tuple[float, float]]:
    return ((x, y) for y in fixed(length=height, number=number))


def y_fixed(
        *,
        y,
        width: float,
        number: int,
) -> Iterable[Tuple[float, float]]:
    return ((x, y) for x in fixed(length=width, number=number))


def _create_ltrb(
        *,
        width: float,
        height: float,
        ltrb: str,
        chair_offset: float = 30,
):
    l, t, r, b = map(int, ltrb)
    return _create_rect(
        width=width,
        height=height,
        chairs=(
            *x_fixed(x=- width / 2 - chair_offset, height=height, number=l),
            *y_fixed(y=height / 2 + chair_offset, width=width, number=t),
            *reversed(tuple(x_fixed(x=width / 2 + chair_offset, height=height, number=r))),
            *reversed(tuple(y_fixed(y=- height / 2 - chair_offset, width=width, number=b))),
        )
    )


@with_dimensions
def create_template(name: str, **kwargs: Any) -> TableTemplate:
    return globals()['_create_' + name](**kwargs)


def create_table(
        name: str,
        **kwargs,
):
    return Table(template=create_template(name, **kwargs))


def create_multiple(
        n: int,
        name: str,
        **kwargs,
):
    return [create_table(name, **kwargs) for _ in range(n)]
