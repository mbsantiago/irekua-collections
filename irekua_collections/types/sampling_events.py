import datetime
from typing import Optional
from typing import Any
from typing import Union
from typing import TypedDict


class SamplingEvent(TypedDict):
    sampling_event_type: Optional[str]
    site_id: Optional[int]
    started_on: Optional[Union[datetime.datetime, str]]
    ended_on: Optional[Union[datetime.datetime, str]]
    metadata: Optional[Any]
    parent_id: Optional[int]
