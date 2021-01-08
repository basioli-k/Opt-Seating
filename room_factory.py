from typing import Any

from shapely.geometry import Polygon

from room import Room
from util import xy_combinations, circle_points, with_dimensions


def create_rect(
        *,
        width: float,
        height: float,
):
    return Room(
        shape=Polygon(xy_combinations(
            x=width / 2,
            y=height / 2,
        )),
    )


def create_L(
        *,
        width: float,
        height: float,
        smaller_width: float,
        smaller_height: float,
):
    return Room(
        shape=Polygon(
            (
                (- width / 2, -height / 2),
                (- width / 2, height / 2),
                (- width / 2 + smaller_width, height / 2),
                (- width / 2 + smaller_width, height / 2 - smaller_height),
                (width / 2, height / 2 - smaller_height),
                (width / 2, -height / 2),
            )
        ),
    )


def create_delta(
        width: float,
        height: float,
        skew: float = 0.5,
):
    return Room(
        shape=Polygon(
            (
                (-width / 2, - height / 2),
                (width * (skew - .5), height / 2),
                (width / 2, -height / 2),
            )
        ),
    )


def create_circle(
        width: float,
        num_slides: int = 64,
):
    return Room(
        shape=Polygon(
            circle_points(
                radius=width / 2,
                num_points=num_slides,
            ),
        ),
    )


def create_o(
        width: float,
        inner_width: float = None,
        num_slides: int = 64,
):
    inner_width = inner_width or width / 2
    return Room(
        shape=Polygon(
            shell=circle_points(
                radius=width / 2,
                num_points=num_slides,
            ),
            holes=(
                circle_points(
                    radius=inner_width / 2,
                    num_points=num_slides,
                ),
            )
        ),
    )


@with_dimensions
def create(name: str, **kwargs: Any) -> Room:
    return globals()['create_' + name](**kwargs)
