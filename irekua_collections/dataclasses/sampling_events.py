import datetime
from typing import Optional
from typing import Any
from dataclasses import dataclass

from irekua_collections.storage import DBID
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class SamplingEvent(BaseClass, metaclass=BaseMetaclass):
    name: Optional[str] = None
    sampling_event_type: Optional[str] = None
    started_on: Optional[datetime.datetime] = None
    ended_on: Optional[datetime.datetime] = None
    metadata: Optional[Any] = None
    site_id: Optional[DBID] = None
    parent_id: Optional[DBID] = None
    id: Optional[DBID] = None

    relations = [
        ("site", "Site"),
        ("parent", "SamplingEvent"),
    ]
