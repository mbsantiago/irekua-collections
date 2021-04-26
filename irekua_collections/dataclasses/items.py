from typing import Optional
from typing import Any
from typing import List

from dataclasses import dataclass
from dataclasses import field

from .annotations import UserAnnotation
from .base import BaseMetaclass


@dataclass
class Item(metaclass=BaseMetaclass):
    path: str
    item_type: Optional[str] = None

    # Labelling info
    ready: bool = False
    labels: List[UserAnnotation] = field(default_factory=list)

    # Item media info
    media_info: Optional[Any] = None

    # Authorship info
    owner: Optional[str] = None

    # Potential hierachical item structure
    parent_id: Optional[int] = None

    # Item metadata
    site_id: Optional[int] = None
    sampling_event_id: Optional[int] = None
    device_id: Optional[int] = None
    deployment_id: Optional[int] = None
    organism_id: Optional[int] = None
    organism_capture_id: Optional[int] = None

    # Additional metadata
    metadata: Optional[Any] = None

    relations = [
        ("parent", "Item"),
        ("site", "Site"),
        ("device", "Device"),
        ("sampling_event", "SamplingEvent"),
        ("deployment", "Deployment"),
        ("organism", "Organism"),
        ("organism_capture", "OrganismCapture"),
    ]
