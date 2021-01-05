from shapely.geometry import Polygon


class Room:
    """
        represents a room
    """

    def __init__(
            self,
            *,
            shape: Polygon,
    ):
        self._shape = shape

    def visit(self, visitor) -> None:
        visitor(self)

    def exterior_xy(self):
        return self._shape.exterior.xy

    def interiors_xy(self):
        return tuple(interior.xy for interior in self._shape.interiors)
