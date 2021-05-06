from typing import Optional
from typing import Any
from typing import List

from dataclasses import dataclass
from dataclasses import field

from irekua_collections.storage import DBID
from irekua_collections.dataclasses.annotations import UserAnnotation
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class Item(BaseClass, metaclass=BaseMetaclass):
    path: Optional[str] = None
    item_type: Optional[str] = None
    hash: Optional[str] = field(default=None, repr=False)

    # Labelling info
    ready: bool = False
    annotations: List[UserAnnotation] = field(default_factory=list, repr=False)

    # Item media info
    media_info: Optional[Any] = field(default=None, repr=False)

    # Authorship info
    collection: Optional[str] = None
    owner: Optional[str] = None

    # Potential hierachical item structure
    parent_id: Optional[int] = field(default=None, repr=False)

    # Item metadata
    site_id: Optional[int] = None
    sampling_event_id: Optional[int] = None
    device_id: Optional[int] = None
    deployment_id: Optional[int] = None
    organism_id: Optional[int] = None
    organism_capture_id: Optional[int] = None

    # Additional metadata
    metadata: Optional[Any] = field(default=None, repr=False)
    id: Optional[DBID] = None

    relations = [
        ("parent", "Item"),
        ("site", "Site"),
        ("device", "Device"),
        ("sampling_event", "SamplingEvent"),
        ("deployment", "Deployment"),
        ("organism", "Organism"),
        ("organism_capture", "OrganismCapture"),
    ]
