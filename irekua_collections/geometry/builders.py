from irekua_collections.geometry.geometry import Point
from irekua_collections.geometry.geometry import Geometry
from irekua_collections.geometry.geometry import LineString
from irekua_collections.geometry.geometry import Polygon
from irekua_collections.geometry.geometry import MultiLineString
from irekua_collections.geometry.geometry import MultiPoint
from irekua_collections.geometry.geometry import MultiPolygon


__all__ = [
    "build_geometry",
]


def build_geometry(data) -> Geometry:
    if "x" in data:
        return _build_point(data)

    if "path" in data:
        return _build_linestring(data)

    if "exterior" in data:
        return _build_polygon(data)

    if "points" in data:
        return _build_multipoint(data)

    if "linestrings " in data:
        return _build_multilinestring(data)

    if "polygons" in data:
        return _build_multipolygon(data)

    raise NotImplementedError


def _build_point(data) -> Point:
    return Point(**data)


def _build_linestring(data) -> LineString:
    return LineString([Point(**p) for p in data["path"]])


def _build_polygon(data) -> Polygon:
    return Polygon(
        exterior=[Point(**p) for p in data["exterior"]],
        interior=[
            [Point(**p) for p in path] for path in data.get("interior", [])
        ],
    )


def _build_multipoint(data) -> MultiPoint:
    return MultiPoint(points=[_build_point(p) for p in data["points"]])


def _build_multilinestring(data) -> MultiLineString:
    return MultiLineString(
        linestrings=[_build_linestring(ls) for ls in data["linestrings"]]
    )


def _build_multipolygon(data) -> MultiPolygon:
    return MultiPolygon(
        linestrings=[_build_polygon(p) for p in data["polygons"]]
    )
