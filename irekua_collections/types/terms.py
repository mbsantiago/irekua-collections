from typing import Optional
from typing import TypedDict


class Term(TypedDict):
    value: str
    term_type: Optional[str]
