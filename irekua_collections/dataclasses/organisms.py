from typing import Optional
from typing import Any
from typing import List

from dataclasses import dataclass
from dataclasses import field

from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass
from irekua_collections.dataclasses.terms import Term


@dataclass
class Organism(BaseClass, metaclass=BaseMetaclass):
    name: Optional[str] = None
    organism_type: Optional[str] = None
    identification_info: Optional[Any] = None
    metadata: Optional[Any] = None
    labels: List[Term] = field(default_factory=list)


@dataclass
class OrganismCapture(BaseClass, metaclass=BaseMetaclass):
    organism_id: int
    deployment_id: Optional[int] = None
    metadata: Optional[Any] = None

    relations = [
        ("deployment", "Deployment"),
        ("organism", "Organism"),
    ]
