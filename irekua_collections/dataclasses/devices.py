from typing import Optional
from typing import Any
from dataclasses import dataclass

from .base import BaseMetaclass


@dataclass
class Device(metaclass=BaseMetaclass):
    device_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    metadata: Optional[Any] = None
