from typing import Optional
from typing import Any
from typing import TypedDict


from irekua_collections.types.geometry import Geometry


class Site(TypedDict):
    geometry: Geometry
    name: Optional[str]
    site_type: Optional[str]
    geometry_type: Optional[str]
    metadata: Optional[Any]
    parent: Optional[int]
