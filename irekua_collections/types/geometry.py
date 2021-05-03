from typing import Optional
from typing import Union
from typing import List
from typing import Iterable
from typing import TypedDict


class Point(TypedDict):
    latitude: float
    longitude: float


Path = Iterable[Point]


class LineString(TypedDict):
    path: Path


class Polygon(TypedDict):
    exterior: Path
    interior: Optional[List[Path]]


class MultiPoint(TypedDict):
    points: Iterable[Point]


class MultiLineString(TypedDict):
    linestrings: Iterable[LineString]


class MultiPolygon(TypedDict):
    polygons: Iterable[Polygon]


Geometry = Union[
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
]
