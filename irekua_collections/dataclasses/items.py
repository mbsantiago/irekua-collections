from typing import Optional
from typing import Any

from dataclasses import dataclass
from dataclasses import field

from irekua_collections.storage import DBID
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class Item(BaseClass, metaclass=BaseMetaclass):
    path: Optional[str] = None
    item_type: Optional[str] = None
    hash: Optional[str] = field(default=None, repr=False)

    # Labelling info
    ready: bool = False

    # Item media info
    media_info: Optional[Any] = field(default=None, repr=False)

    # Authorship info
    collection: Optional[str] = None
    owner: Optional[str] = None

    # Potential hierachical item structure
    parent_id: Optional[DBID] = field(default=None, repr=False)

    # Item metadata
    site_id: Optional[DBID] = None
    sampling_event_id: Optional[DBID] = None
    device_id: Optional[DBID] = None
    deployment_id: Optional[DBID] = None
    organism_id: Optional[DBID] = None
    organism_capture_id: Optional[DBID] = None

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

    def annotations(self):
        return self.storage["UserAnnotation"].filter(item_id=self.id)
