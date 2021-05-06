from typing import Optional
from dataclasses import dataclass

from irekua_collections.storage import DBID
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class Term(BaseClass, metaclass=BaseMetaclass):
    value: str
    term_type: Optional[str] = None
    parent_id: Optional[int] = None
    id: Optional[DBID] = None

    relations = [("parent", "Term")]
