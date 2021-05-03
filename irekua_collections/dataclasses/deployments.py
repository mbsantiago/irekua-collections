import datetime
from typing import Optional
from typing import Any
from dataclasses import dataclass

from irekua_collections.dataclasses.geometry import Point
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class Deployment(BaseClass, metaclass=BaseMetaclass):
    sampling_event_id: Optional[int] = None
    device_id: Optional[int] = None
    deployment_type: Optional[str] = None
    deployed_on: Optional[datetime.datetime] = None
    recovered_on: Optional[datetime.datetime] = None
    point: Optional[Point] = None
    metadata: Optional[Any] = None
    configuration: Optional[Any] = None

    relations = [
        ("sampling_event", "SamplingEvent"),
        ("device", "Device"),
    ]
