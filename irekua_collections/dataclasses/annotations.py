from typing import Optional
from typing import Any
from typing import Iterable
from dataclasses import dataclass
from dataclasses import field

from irekua_collections.storage import DBID
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass
from irekua_collections.dataclasses.terms import Term


@dataclass
class EventType(BaseClass, metaclass=BaseMetaclass):
    name: str
    parent_id: Optional[DBID] = None
    id: Optional[DBID] = None

    relations = [("parent", "EventType")]


@dataclass
class Annotation(BaseClass):
    item_id: Optional[DBID] = None
    event_type_id: Optional[DBID] = None
    annotation_type: Optional[str] = None
    labels: Iterable[Term] = field(default_factory=list)
    geometry: Optional[Any] = None
    id: Optional[DBID] = None

    relations = [
        ("item", "Item"),
        ("event_type", "EventType"),
    ]


@dataclass
class UserAnnotation(Annotation, metaclass=BaseMetaclass):
    author: Optional[str] = None
    quality: Optional[str] = None


@dataclass
class Prediction(Annotation, metaclass=BaseMetaclass):
    score: Optional[float] = None
