from typing import Optional
from typing import Any
from typing import Iterable
from dataclasses import dataclass
from dataclasses import field

from irekua_collections.dataclasses.geometry import Geometry
from irekua_collections.dataclasses.terms import Term
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class Locality(BaseClass, metaclass=BaseMetaclass):
    name: Optional[str]
    locality_type: Optional[str] = None
    parent_id: Optional[int] = None

    relations = [
        ("parent", "Locality"),
    ]


@dataclass
class Site(BaseClass, metaclass=BaseMetaclass):
    geometry: Optional[Geometry] = None
    name: Optional[str] = None
    site_type: Optional[str] = None
    geometry_type: Optional[str] = None
    parent_id: Optional[int] = None
    metadata: Optional[Any] = None
    altitude: Optional[float] = None

    localities: Iterable[Locality] = field(default_factory=list)
    descriptors: Iterable[Term] = field(default_factory=list)

    relations = [
        ("parent", "Site"),
    ]
