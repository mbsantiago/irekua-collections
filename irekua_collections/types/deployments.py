import datetime
from typing import Optional
from typing import Any
from typing import Union
from typing import TypedDict

from irekua_collections.types.geometry import Point


class Deployment(TypedDict):
    sampling_event_id: Optional[int]
    device_id: Optional[int]
    deployment_type: Optional[str]
    deployed_on: Optional[Union[datetime.datetime, str]]
    recovered_on: Optional[Union[datetime.datetime, str]]
    point: Optional[Point]
    metadata: Optional[Any]
    configuration: Optional[Any]
