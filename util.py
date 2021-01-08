import math
from typing import Union, Callable, TypeVar, Any, Tuple

import numpy as np

# --------------------------------------------- GENERATING POINTS ------------------------------------------------------
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



# ---------------------------------------------------- WRAPPERS -------------------------------------------------------
T = TypeVar('T')


def with_dimensions(fn: Callable[..., T]) -> Callable[..., T]:
    """
    :param fn: function
    :return: converts function parameters from meters to centimeters
    """

    def wrapper(name: str, **kwargs: Any):
        return fn(name, **{k: to_cm(v) for k, v in kwargs.items()})

    return wrapper


def qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    return obj.__module__ + '.' + obj.__qualname__


def declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = qualname(obj)
    return name[:name.rfind('.')]


def with_backing_field(fn):
    backing_field_name = '_' + fn.__qualname__

    def wrapper(self):
        if backing_field_name not in self.__dict__:
            self.__dict__[backing_field_name] = fn(self)
        return self.__dict__[backing_field_name]

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


# ------------------------------------------------- VISUALIZATIONS ----------------------------------------------------

def draw_mask(mask):
    print('\n'.join(''.join(row) for row in np.where(mask, *'█░')))


# ------------------------------------------------- HELPERS ----------------------------------------------------

def aslist(a):
    return a.tolist()
