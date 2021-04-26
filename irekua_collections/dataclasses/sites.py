from typing import Optional
from typing import Any
from dataclasses import dataclass

from irekua_collections.geometry import Geometry
from .base import BaseMetaclass


@dataclass
class Site(metaclass=BaseMetaclass):
    geometry: Geometry
    name: Optional[str] = None
    site_type: Optional[str] = None
    geometry_type: Optional[str] = None
    metadata: Optional[Any] = None
    parent_id: Optional[int] = None

    relations = [
        ("parent", "Site"),
    ]
