from typing import Optional
from typing import TypedDict
from typing import Any
from typing import Iterable

from irekua_collections.types.terms import Term
from irekua_collections.types.utils import union
from irekua_collections.dataclasses import annotations


@union(annotations.EventType)
class EventType(TypedDict):
    name: str
    parent_id: Optional[int]


@union(annotations.Annotation)
class Annotation(TypedDict):
    item_id: int
    event_type_id: Optional[int]
    annotation_type: Optional[str]
    labels: Iterable[Term]
    geometry: Optional[Any]


@union(annotations.UserAnnotation)
class UserAnnotation(Annotation):
    author: Optional[str]
    quality: Optional[str]


@union(annotations.Prediction)
class Prediction(Annotation):
    score: Optional[float]
