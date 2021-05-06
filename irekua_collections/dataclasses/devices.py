from typing import Optional
from typing import Any
from dataclasses import dataclass

from irekua_collections.storage import DBID
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class Device(BaseClass, metaclass=BaseMetaclass):
    device_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    metadata: Optional[Any] = None
    id: Optional[DBID] = None
