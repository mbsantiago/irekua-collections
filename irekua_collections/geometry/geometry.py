from typing import Union
from typing import List
from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class Point:
    x: float
    y: float


Path = List[Point]


@dataclass
class LineString:
    path: Path


@dataclass
class Polygon:
    exterior: Path
    interior: List[Path] = field(default_factory=list)


@dataclass
class MultiPoint:
    points: List[Point]


@dataclass
class MultiLineString:
    linestrings: List[LineString]


@dataclass
class MultiPolygon:
    polygons: List[Polygon]


Geometry = Union[
    Point,
    LineString,
    Polygon,
    MultiPoint,
    MultiLineString,
    MultiPolygon,
]
