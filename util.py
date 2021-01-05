import math
from typing import Union, Callable, TypeVar, Any


def xy_combinations(
        *,
        x: float,
        y: float,
):
    return (
        (-x, -y),
        (-x, y),
        (x, y),
        (x, -y),
    )


def circle_points(
        radius: float,
        num_points: int,
):
    return tuple(
        (
            radius * math.sin(angle),
            radius * math.cos(angle),
        )
        for angle in (
            i * 2 * math.pi / num_points
            for i in range(num_points)
        )
    )


T = TypeVar('T')


def aslist(a):
    return a.tolist()


def with_dimensions(fn: Callable[..., T]) -> Callable[..., T]:
    def wrapper(name: str, **kwargs: Any):
        return fn(name, **{k: to_cm(v) for k, v in kwargs.items()})

    return wrapper


def to_cm(x: Union[float, str]) -> float:
    if isinstance(x, (int, float)):
        return float(x)
    if not isinstance(x, str):
        return x
    if x.endswith('cm'):
        return float(x[:-2])
    if x.endswith('m'):
        return float(x[:-1]) * 100
    try:
        return float(x)
    except ValueError:
        pass
    raise ValueError(f'Cannot parse size: {x}')
