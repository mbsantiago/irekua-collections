from typing import Optional
from dataclasses import asdict

from irekua_collections import storage


class BaseClass:
    def __post_init__(self):
        self.id: Optional[int] = None

        storages = storage.get()

        if storages is None:
            return

        store = storages[type(self).__qualname__]
        store.add(self)

    def asdict(self):
        return asdict(self)


def build_property(cls, name, model):
    def getter(self):
        storages = cls.storage

        value = getattr(self, f"{name}_id", None)

        if value is None:
            raise storage.DoesNotExist("No related object")

        return storages[model].get_by_id(value)

    def setter(self, value):
        if not hasattr(value, "id") or value.id is None:
            raise ValueError(f"Not an {model} object")

        setattr(self, f"{name}_id", value.id)

    return property(getter, setter)


class BaseMetaclass(type):
    def __new__(cls, name, bases, dct):
        if BaseClass not in bases:
            bases = (*bases, BaseClass)

        cls = super().__new__(cls, name, bases, dct)

        for name, model in getattr(cls, "relations", []):
            setattr(cls, name, build_property(cls, name, model))

        return cls

    @property
    def name(cls) -> str:
        return str(cls.__qualname__)

    @property
    def storage(cls) -> storage.Storages:
        storages = storage.get()

        if storages is None:
            raise storage.ConfigurationError("Not within a collection")

        return storages

    def get(cls, id=None, **query):
        return cls.storage[cls.name].get(id=id, **query)

    def get_or_create(cls, id=None, defaults=None, **query):
        if defaults is None:
            defaults = {}

        try:
            return cls.get(id=id, **query)

        except storage.DoesNotExist:
            return cls(**defaults, **query)
