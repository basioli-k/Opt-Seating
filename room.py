from shapely.geometry import Polygon
from util import aslist


class Room:
    """
        represents a room
    """

    def __init__(
            self,
            *,
            shape: Polygon,
            biggest_distance: float,
    ):
        self._shape = shape
        self._biggest_distance = biggest_distance

    @property
    def exterior_xy(self):
        """
        :return: tuple of ordered pairs of (x,y) coordinates for points in exterior polygon
        """
        return tuple(zip(*map(aslist, self._shape.exterior.xy)))

    @property
    def interiors_xy(self):
        """
        :return: tuple of tuples of coordinates (x,y) of points defining the interior for every interior of polygon
        """
        return tuple(tuple(zip(*map(aslist, interior.xy))) for interior in self._shape.interiors)

    @property
    def poly(self) -> Polygon:
        return self._shape
