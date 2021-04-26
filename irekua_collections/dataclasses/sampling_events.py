import datetime
from typing import Optional
from typing import Any
from dataclasses import dataclass

from .base import BaseMetaclass


@dataclass
class SamplingEvent(metaclass=BaseMetaclass):
    sampling_event_type: Optional[str] = None
    site_id: Optional[int] = None
    started_on: Optional[datetime.datetime] = None
    ended_on: Optional[datetime.datetime] = None
    metadata: Optional[Any] = None
    parent_id: Optional[int] = None

    relations = [
        ("site", "Site"),
        ("parent", "SamplingEvent"),
    ]
