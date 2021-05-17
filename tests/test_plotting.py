import matplotlib.pyplot as plt

from irekua_collections.geometry import Point
from irekua_collections.geometry import Polygon
from irekua_collections.geometry import LineString
from irekua_collections.geometry import MultiPoint
from irekua_collections.geometry import MultiPolygon
from irekua_collections.geometry import MultiLineString
from irekua_collections.geometry import plot_geometry


def test_plot_point():
    ax = None
    ax = plot_geometry(Point(x=0, y=0), ax=ax)
    ax = plot_geometry(Point(x=1, y=0), ax=ax)
    ax = plot_geometry(Point(x=1, y=1), ax=ax)
    ax = plot_geometry(Point(x=0, y=1), ax=ax)
    plt.show()


def test_plot_linestring():
    linestring = LineString(
        path=[
            Point(x=0, y=0),
            Point(x=1, y=0),
            Point(x=1, y=1),
            Point(x=0, y=1),
        ]
    )
    plot_geometry(linestring)
    plt.show()


def test_plot_polygon():
    polygon = Polygon(
        exterior=[
            Point(x=0, y=0),
            Point(x=1, y=0),
            Point(x=1, y=1),
            Point(x=0, y=1),
        ],
        interior=[
            [
                Point(x=0.2, y=0.2),
                Point(x=0.8, y=0.2),
                Point(x=0.8, y=0.8),
                Point(x=0.2, y=0.8),
            ]
        ],
    )
    plot_geometry(polygon)
    plt.show()
