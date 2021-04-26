from typing import Optional
from dataclasses import dataclass

from .base import BaseMetaclass


@dataclass
class Term(metaclass=BaseMetaclass):
    value: str
    term_type: Optional[str] = None
    parent_id: Optional[int] = None

    relations = [("parent", "Term")]
