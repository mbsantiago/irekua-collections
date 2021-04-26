from typing import Optional
from typing import Any
from typing import List

from dataclasses import dataclass
from dataclasses import field

from .base import BaseMetaclass
from .terms import Term


@dataclass
class Organism(metaclass=BaseMetaclass):
    name: Optional[str] = None
    organism_type: Optional[str] = None
    identification_info: Optional[Any] = None
    metadata: Optional[Any] = None
    labels: List[Term] = field(default_factory=list)


@dataclass
class OrganismCapture(metaclass=BaseMetaclass):
    organism_id: int
    deployment_id: Optional[int] = None
    metadata: Optional[Any] = None

    relations = [
        ("deployment", "Deployment"),
        ("organism", "Organism"),
    ]
