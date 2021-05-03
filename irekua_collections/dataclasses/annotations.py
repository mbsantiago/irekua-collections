from typing import Optional
from typing import Any
from typing import Iterable
from dataclasses import dataclass
from dataclasses import field

from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass
from irekua_collections.dataclasses.terms import Term


@dataclass
class EventType(BaseClass, metaclass=BaseMetaclass):
    name: str
    parent_id: Optional[int] = None

    relations = [("parent", "EventType")]


@dataclass
class Annotation(BaseClass, metaclass=BaseMetaclass):
    item_id: int
    event_type_id: Optional[int] = None
    annotation_type: Optional[str] = None
    labels: Iterable[Term] = field(default_factory=list)
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
