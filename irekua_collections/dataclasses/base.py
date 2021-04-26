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
        value = getattr(self, f"{name}_id", None)

        if value is None:
            raise ValueError("No related object")

        storages = storage.get()

        if storages is None:
            raise ValueError("Not within a collection")

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
