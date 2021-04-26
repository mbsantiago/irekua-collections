from typing import Optional
from dataclasses import dataclass

import pytest

from irekua_collections.dataclasses.base import BaseMetaclass
from irekua_collections.storage import Storages
from irekua_collections.storage import DoesNotExist


@dataclass
class A(metaclass=BaseMetaclass):
    a: int
    b: Optional[str] = None


@dataclass
class B(metaclass=BaseMetaclass):
    a: int
    b: Optional[str] = None

    parent_id: Optional[int] = None

    relations = [
        ("parent", "B"),
    ]


def test_baseclass():
    a = A(1)

    assert hasattr(a, "id")
    assert a.id is None

    st = Storages(["A", "B"])
    with st:
        a1 = A(1)
        assert a1.id == 0
        assert a1.a == 1

        a2 = A(2)
        assert a2.id == 1
        assert a2.a == 2

        b = B(3)
        assert b.id == 0

        assert "A" in st
        assert "B" in st
        assert len(st["A"].objects) == 2

        assert st["A"].get(id=0) == a1
        assert st["A"].get(id=1) == a2

        assert st["A"].get(a=2) == a2

        b2 = B(4, parent_id=b.id)
        assert b2.parent == b

        b3 = B(5, parent_id=929292)
        with pytest.raises(DoesNotExist):
            b3.parent

    with pytest.raises(ValueError):
        assert b2.parent == b

    a = A(1)
    assert a.id is None


def test_baseclass_relations():
    b0 = B(2)

    with pytest.raises(ValueError):
        b0.parent

    st = Storages(["A", "B"])
    with st:
        b1 = B(2)

        with pytest.raises(ValueError):
            b1.parent

        b2 = B(2, parent_id=3)

        with pytest.raises(DoesNotExist):
            b2.parent

        b3 = B(2, parent_id=0)
        assert b3.parent == b1

        with pytest.raises(ValueError):
            b3.parent = b0

        b2.parent = b1
        assert b2.parent_id == b1.id
        assert b2.parent == b1
