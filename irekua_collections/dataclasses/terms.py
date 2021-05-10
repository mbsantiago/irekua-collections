from typing import Optional
from dataclasses import dataclass

from irekua_collections.storage import DBID
from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.dataclasses.base import BaseClass


@dataclass
class Term(BaseClass, metaclass=BaseMetaclass):
    value: Optional[str] = None
    term_type: Optional[str] = None

    parent_id: Optional[DBID] = None
    id: Optional[DBID] = None

    relations = [("parent", "Term")]
