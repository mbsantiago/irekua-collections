import json
import os
from dataclasses import dataclass

from irekua_collections.storage import Storage
from irekua_collections.storage import Storages


@dataclass
class TestObj:
    id: str


def test_storage_api():
    st = Storage(name="test")

    objs = [
        TestObj(id=1),
        TestObj(id=2),
        TestObj(id=3),
    ]

    # Can count the number of items
    assert st.count() == 0
    assert len(st) == 0

    for obj in objs:
        # Can add new objects
        st.add(obj)

    # Can iterate
    for obj in st:
        assert obj in objs

    # Can count the number of items
    assert st.count() == 3
    assert len(st) == 3

    # Can check if an element is present (by id)
    assert 1 in st

    # Get a list of all stored objects
    assert isinstance(st.all(), list)


def test_dump_storage(tmp_path):
    N = 100
    st = Storage(name="test")

    for n in range(N):
        st.add(TestObj(id=str(n)))

    st.dump(tmp_path)

    path = tmp_path / "test.json"
    with open(path, "r") as jsonfile:
        data = json.load(jsonfile)

    for n in range(N):
        n = str(n)
        assert n in data
        assert len(data[n]) == 1
        assert "id" in data[n]
        assert data[n]["id"] == n


def test_load_storage(tmp_path):
    test_data = {
        "1": {"id": "1"},
        "2": {"id": "2"},
        "3": {"id": "3"},
    }

    path = tmp_path / "test.json"
    with open(path, "w") as jsonfile:
        json.dump(test_data, jsonfile)

    st = Storage.load(tmp_path, {"name": "test"})

    assert st.get("1") == {"id": "1"}
    assert st.get("2") == {"id": "2"}
    assert st.get("3") == {"id": "3"}


def test_dump_storages(tmp_path):
    st = Storages(name="test", fields=["a", "b", "c"])

    config = st.get_config()
    assert config["name"] == "test"
    assert "a" in config["storages"]
    assert "b" in config["storages"]
    assert "c" in config["storages"]

    st.dump(tmp_path)

    config = tmp_path / "test.json"
    assert os.path.exists(config)

    with open(config, "r") as jsonfile:
        config = json.load(jsonfile)

    assert config.get("name") == "test"
    stores = config.get("storages")
    assert isinstance(stores, dict)
    assert "a" in stores
    assert "b" in stores
    assert "c" in stores


def test_load_storages(tmp_path):
    config = {
        "name": "storages",
        "storages": {
            "a": {
                "name": "a",
            },
            "b": {
                "name": "b",
            },
        },
    }

    test_data = {
        "1": {"id": "1"},
        "2": {"id": "2"},
        "3": {"id": "3"},
    }

    path = tmp_path / "a.json"
    with open(path, "w") as jsonfile:
        json.dump(test_data, jsonfile)

    path = tmp_path / "b.json"
    with open(path, "w") as jsonfile:
        json.dump(test_data, jsonfile)

    path = tmp_path / "storages.json"
    with open(path, "w") as jsonfile:
        json.dump(config, jsonfile)

    st = Storages.load(tmp_path)
    assert "a" in st
    assert "b" in st
    assert "1" in st["a"]
    assert "2" in st["a"]
    assert "3" in st["a"]
    assert "1" in st["b"]
    assert "2" in st["b"]
    assert "3" in st["b"]
