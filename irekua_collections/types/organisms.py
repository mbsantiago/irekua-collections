from typing import Optional
from typing import Any
from typing import List
from typing import TypedDict

from irekua_collections.types.terms import Term


class Organism(TypedDict):
    name: Optional[str]
    organism_type: Optional[str]
    identification_info: Optional[Any]
    metadata: Optional[Any]
    labels: List[Term]


class OrganismCapture(TypedDict):
    organism_id: int
    deployment_id: Optional[int]
    metadata: Optional[Any]
