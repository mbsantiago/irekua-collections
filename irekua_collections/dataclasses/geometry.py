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


def _build_point(data):
    return Point(**data)


def _build_linestring(data):
    return LineString([Point(**p) for p in data["path"]])


def _build_polygon(data):
    return Polygon(
        exterior=[Point(**p) for p in data["exterior"]],
        interior=[
            [Point(**p) for p in path] for path in data.get("interior", [])
        ],
    )


def build_geometry(data) -> Geometry:
    if "x" in data:
        return _build_point(data)

    if "path" in data:
        return _build_linestring(data)

    if "exterior" in data:
        return _build_polygon(data)

    if "points" in data:
        return MultiPoint(points=[_build_point(p) for p in data["points"]])

    if "linestrings " in data:
        return MultiLineString(
            linestrings=[_build_linestring(ls) for ls in data["linestrings"]]
        )

    if "polygons" in data:
        return MultiLineString(
            linestrings=[_build_polygon(p) for p in data["polygons"]]
        )

    raise NotImplementedError
