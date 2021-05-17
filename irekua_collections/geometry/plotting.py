from typing import Optional
from typing import Tuple
from typing import List

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.path import Path

from irekua_collections.geometry.geometry import Point
from irekua_collections.geometry.geometry import Geometry
from irekua_collections.geometry.geometry import Path as PointPath
from irekua_collections.geometry.geometry import LineString
from irekua_collections.geometry.geometry import Polygon
from irekua_collections.geometry.geometry import MultiLineString
from irekua_collections.geometry.geometry import MultiPoint
from irekua_collections.geometry.geometry import MultiPolygon


__all__ = [
    "plot_geometry",
]


def plot_geometry(
    geometry: Geometry,
    ax: Optional[Axes] = None,
    figsize: Tuple[float, float] = (10, 10),
    **kwargs,
) -> Axes:
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)

    if isinstance(geometry, Point):
        return _plot_point(geometry, ax=ax, **kwargs)

    if isinstance(geometry, LineString):
        return _plot_linestring(geometry, ax=ax, **kwargs)

    if isinstance(geometry, Polygon):
        return _plot_polygon(geometry, ax=ax, **kwargs)

    if isinstance(geometry, MultiPoint):
        return _plot_multipoint(geometry, ax=ax, **kwargs)

    if isinstance(geometry, MultiLineString):
        return _plot_multilinestring(geometry, ax=ax, **kwargs)

    if isinstance(geometry, MultiPolygon):
        return _plot_multipolygon(geometry, ax=ax, **kwargs)


def _plot_point(
    geometry: Point,
    ax: Axes,
    marker: str = "o",
    color="blue",
    **kwargs,
) -> Axes:
    ax.plot(
        [geometry.x],
        [geometry.y],
        marker=marker,
        color=color,
        **kwargs,
    )
    return ax


def _plot_linestring(
    geometry: LineString,
    ax: Axes,
    linewidth: float = 1,
    color="blue",
    linestyle: str = "-",
    **kwargs,
) -> Axes:
    X, Y = zip(*[(p.x, p.y) for p in geometry.path])
    ax.plot(
        X,
        Y,
        color=color,
        linewidth=linewidth,
        linestyle=linestyle,
        **kwargs,
    )
    return ax


def _create_linearring_path(
    points: PointPath,
) -> Tuple[List[Tuple[float, float]], List[str]]:
    path = [(p.x, p.y) for p in points] + [(points[0].x, points[0].y)]
    codes = [Path.LINETO for _ in path]
    codes[0] = Path.MOVETO
    codes[-1] = Path.CLOSEPOLY
    return path, codes


def _plot_polygon(
    geometry: Polygon,
    ax: Axes,
    alpha: float = 1,
    fill: bool = True,
    edgecolor: Optional[str] = "none",
    facecolor: Optional[str] = "blue",
    **kwargs,
) -> Axes:
    vertices, codes = _create_linearring_path(geometry.exterior)

    for interior in geometry.interior:
        ivertices, icodes = _create_linearring_path(interior[::-1])
        vertices += ivertices
        codes += icodes

    path = Path(vertices, codes)
    patch = PathPatch(
        path,
        alpha=alpha,
        fill=fill,
        edgecolor=edgecolor,
        facecolor=facecolor,
        **kwargs,
    )
    ax.add_patch(patch)
    ax.autoscale_view()
    return ax


def _plot_multipoint(
    geometry: MultiPoint,
    ax: Axes,
    **kwargs,
) -> Axes:
    for point in geometry.points:
        ax = _plot_point(point, **kwargs)

    return ax


def _plot_multilinestring(
    geometry: MultiLineString,
    ax: Axes,
    **kwargs,
) -> Axes:
    for linestring in geometry.linestrings:
        ax = _plot_linestring(linestring, **kwargs)

    return ax


def _plot_multipolygon(
    geometry: MultiPolygon,
    ax: Axes,
    **kwargs,
) -> Axes:
    for polygon in geometry.polygons:
        ax = _plot_polygon(polygon, ax, **kwargs)

    return ax
