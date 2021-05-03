from typing import Optional
from typing import Any
from typing import Iterable
from typing import TypedDict

from irekua_collections.types.annotations import UserAnnotation


class Item(TypedDict):
    path: str
    item_type: Optional[str]
    ready: bool = False
    labels: Iterable[UserAnnotation]
    media_info: Optional[Any]
    owner: Optional[str]
    parent_id: Optional[int]
    site_id: Optional[int]
    sampling_event_id: Optional[int]
    device_id: Optional[int]
    deployment_id: Optional[int]
    organism_id: Optional[int]
    organism_capture_id: Optional[int]
    metadata: Optional[Any]
