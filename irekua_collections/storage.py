import os
import json

from typing import Optional
from typing import Union
from typing import Dict
from typing import Any
from typing import Generator
from typing import Iterator
from dataclasses import asdict
from collections import defaultdict
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


DBID = Union[str, int]


class Storage:
    def __init__(self):
        self.objects: Dict[DBID, Any] = {}
        self.counter: Iterator[int] = count()

    def add(self, obj: Any) -> None:
        if obj.id is None:
            id = next(self.counter)
            obj.id = id

        self.objects[obj.id] = obj

    def filter(self, **query) -> Generator[Any, None, None]:
        for obj in self.objects.values():
            if satisfies_query(obj, query):
                yield obj

    def __iter__(self) -> Generator[Any, None, None]:
        for obj in self.objects.values():
            yield obj

    def __len__(self) -> int:
        return len(self.objects)

    def count(self) -> int:
        return len(self.objects)

    def get_by_id(self, id: int) -> Any:
        try:
            return self.objects[id]

        except KeyError:
            raise DoesNotExist(f"No object with id {id} exists")

    def get(self, id: Optional[int] = None, **query) -> Any:
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

    @classmethod
    def load(cls, directory, constructor=None):
        if constructor is None:
            constructor = lambda x: x

        path = os.path.join(directory, "storage.json")
        with open(path, "r") as jsonfile:
            objects = json.load(jsonfile)

        storage = cls()
        storage.objects = {
            key: constructor(value) for key, value in objects.items()
        }
        return storage

    def dump(self, directory, serializer=None):
        if not os.path.exists(directory):
            os.makedirs(directory)

        if serializer is None:
            serializer = asdict

        path = os.path.join(directory, "storage.json")
        serialized = {
            key: serializer(value) for key, value in self.objects.items()
        }

        with open(path, "w") as jsonfile:
            json.dump(serialized, jsonfile)


class Storages:
    storage_class = Storage

    def __init__(self, fields=None):
        if fields is None:
            fields = []

        self.fields = fields
        self.storages = defaultdict(self.storage_class)
        for field in self.fields:
            self.storages[field]

    def __contains__(self, key) -> bool:
        return key in self.storages

    def __getitem__(self, key) -> Storage:
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
            "fields": fields,
            "directories": {
                key: key.lower().replace(" ", "_") for key in fields
            },
        }

    def dump(self, directory, config=None, fields=None):
        if not os.path.exists(directory):
            os.makedirs(directory)

        if config is None:
            config = self.get_config(fields=fields)

        fields = [f for f in config["fields"] if f in fields]
        for field in fields:
            subdir = config["directories"].get(field, field.lower())
            self.storages[field].dump(os.path.join(directory, subdir))

    @classmethod
    def load(cls, directory, config=None, constructors=None):
        if constructors is None:
            constructors = {}

        if config is None:
            config = cls.get_config()

        fields = config.get("fields", [])
        storages = cls(fields)

        directories = config.get("directories", {})
        for field in fields:
            path = os.path.join(
                directory, directories.get(field, field.lower())
            )
            if not os.path.exists(path):
                raise IOError("Storage is not complete")

            storage = cls.storage_class.load(
                path,
                constructor=constructors.get(field),
            )
            storages.storages[field] = storage

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


def load_json(path):
    with open(path, "r") as jsonfile:
        return json.load(jsonfile)
