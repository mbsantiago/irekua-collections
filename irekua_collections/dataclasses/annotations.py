from typing import Optional
from typing import Any
from typing import List
from dataclasses import dataclass
from dataclasses import field

from .base import BaseMetaclass
from .terms import Term


@dataclass
class EventType(metaclass=BaseMetaclass):
    name: str
    parent_id: Optional[int] = None

    relations = [("parent", "EventType")]


@dataclass
class Annotation(metaclass=BaseMetaclass):
    item_id: int
    event_type_id: Optional[int] = None
    annotation_type: Optional[str] = None
    labels: List[Term] = field(default_factory=list)
    geometry: Optional[Any] = None

    relations = [
        ("item", "Item"),
        ("event_type", "EvenType"),
    ]


@dataclass
class UserAnnotation(Annotation):
    author: Optional[str] = None
    quality: Optional[str] = None


@dataclass
class Prediction(Annotation):
    score: Optional[float] = None
