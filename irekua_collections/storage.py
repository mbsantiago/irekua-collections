import os
import json

from typing import NewType
from typing import Optional
from typing import Dict
from typing import Any
from typing import Generator
from typing import Iterator

from dataclasses import asdict
from itertools import count


class StorageError(Exception):
    """Errors from storing items"""


class ConfigurationError(StorageError):
    """Raised when storages are not available or incorrectly configured"""


class DoesNotExist(StorageError):
    """The object you are looking for does not exist in the collection"""


class MultipleMatches(StorageError):
    """The object you are looking for does not exist in the collection"""


def satisfies_query(obj, query):
    for key, value in query.items():
        if not getattr(obj, key, None) == value:
            return False

    return True


DBID = NewType("DBID", str)


class Storage:
    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.objects: Dict[DBID, Any] = {}
        self.counter: Iterator[int] = count()

    def add(self, obj: Any, id: Optional[DBID] = None) -> None:
        if id is None and hasattr(obj, "id"):
            id = getattr(obj, "id")

        if id is None:
            id = DBID(str(next(self.counter)))

        obj.id = id
        self.objects[id] = obj

    def filter(self, **query) -> Generator[Any, None, None]:
        for obj in self.objects.values():
            if satisfies_query(obj, query):
                yield obj

    def __iter__(self) -> Generator[Any, None, None]:
        for obj in self.objects.values():
            yield obj

    def __contains__(self, key: DBID) -> bool:
        return key in self.objects

    def __len__(self) -> int:
        return len(self.objects)

    def count(self) -> int:
        return len(self.objects)

    def get_by_id(self, id: DBID) -> Any:
        try:
            return self.objects[id]

        except KeyError:
            raise DoesNotExist(f"No object with id {id} exists")

    def get(self, id: Optional[DBID] = None, **query) -> Any:
        if id is not None:
            return self.get_by_id(id)

        options = list(self.filter(**query))
        if len(options) > 1:
            raise MultipleMatches("Multiple matches")

        if len(options) == 0:
            raise DoesNotExist("Does not exist")

        return options[0]

    def all(self) -> list:
        return list(self.objects.values())

    def get_config(self):
        return {
            "name": self.name,
        }

    @classmethod
    def load(cls, directory, config=None, constructor=None):
        if constructor is None:
            constructor = _identity

        if config is None:
            config = {}

        name = config.get("name", "storage")
        path = os.path.join(directory, f"{name}.json")
        with open(path, "r") as jsonfile:
            objects = json.load(jsonfile)

        storage = cls(name=name)
        storage.objects = {
            key: constructor(value) for key, value in objects.items()
        }
        return storage

    def dump(self, directory, config=None, serializer=None):
        if config is None:
            config = self.get_config()

        if not os.path.exists(directory):
            os.makedirs(directory)

        if serializer is None:
            serializer = asdict

        path = os.path.join(directory, f"{self.name}.json")
        serialized = {
            key: serializer(value) for key, value in self.objects.items()
        }

        with open(path, "w") as jsonfile:
            json.dump(serialized, jsonfile, default=str)


class Storages:
    storage_class = Storage

    def __init__(self, fields=None, name: Optional[str] = "storages"):
        self.name = name

        if fields is None:
            fields = []
        self.fields = fields

        self.storages = {}

        for field in self.fields:
            self.storages[field] = self.storage_class(name=field)

    def __contains__(self, key) -> bool:
        return key in self.storages

    def __getitem__(self, key) -> Storage:
        if key not in self.storages:
            self.storages = self.storage_class(name=key)

        return self.storages[key]

    def __enter__(self):
        self.__current = get_storage()
        set_storage(self)

    def __exit__(self, *args):
        set_storage(self.__current)

    def get_config(self, fields=None):
        if fields is None:
            fields = list(self.storages.keys())

        return {
            "name": self.name,
            "storages": {
                field: self.storages[field].get_config() for field in fields
            },
        }

    def dump(self, directory: str, config=None, fields=None) -> None:
        if not os.path.exists(directory):
            os.makedirs(directory)

        if fields is None:
            fields = list(self.storages.keys())

        if config is None:
            config = self.get_config(fields=fields)

        # Save storages configuration
        config_file_path = os.path.join(directory, config["name"] + ".json")
        with open(config_file_path, "w") as jsonfile:
            json.dump(config, jsonfile)

        # Dump each internal storage
        fields = [f for f in config["storages"] if f in fields]
        for field in fields:
            self.storages[field].dump(
                directory,
                config=config["storages"][field],
            )

    @classmethod
    def load(
        cls,
        directory: str,
        name: str = "storages",
        config=None,
        constructors=None,
    ):
        if constructors is None:
            constructors = {}

        # Load configurations from file
        config_file_path = os.path.join(directory, f"{name}.json")
        with open(config_file_path, "r") as jsonfile:
            config = json.load(jsonfile)

        fields = config["storages"].keys()
        storages = cls(fields)
        for field in fields:
            storages.storages[field] = cls.storage_class.load(
                directory=directory,
                config=config["storages"][field],
                constructor=constructors.get(field),
            )

        return storages


_default: Optional[Storages] = None


def get_storage() -> Optional[Storages]:
    return _default


def set_storage(storage: Storages) -> None:
    global _default

    if storage is None:
        _default = None
        return

    if not isinstance(storage, Storages):
        raise ValueError

    _default = storage


def _identity(x):
    return x
