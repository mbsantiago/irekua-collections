import os
from irekua_collections.storage import Storages
from irekua_collections import dataclasses


def build_field_property(field_name):
    def getter(self):
        return self.storage[field_name]

    return property(getter)


class Collection:
    fields = [
        "UserAnnotation",
        "Prediction",
        "Deployment",
        "Device",
        "EventType",
        "Item",
        "Organism",
        "OrganismCapture",
        "SamplingEvent",
        "Site",
        "Term",
    ]

    def get_fields(self):
        return self.fields

    def __init__(self, storage=None):
        if storage is None:
            storage = Storages(
                fields=self.get_fields(),
                name="collection",
            )

        self.storage = storage

    def __enter__(self):
        return self.storage.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.storage.__exit__(exc_type, exc_val, exc_tb)

    @classmethod
    def get_constructors(cls):
        return {
            "UserAnnotation": lambda data: dataclasses.UserAnnotation(**data),
            "Prediction": lambda data: dataclasses.Prediction(**data),
            "Deployment": lambda data: dataclasses.Deployment(**data),
            "Device": lambda data: dataclasses.Device(**data),
            "EventType": lambda data: dataclasses.EventType(**data),
            "Item": lambda data: dataclasses.Item(**data),
            "Organism": lambda data: dataclasses.Organism(**data),
            "OrganismCapture": lambda data: dataclasses.OrganismCapture(
                **data
            ),
            "SamplingEvent": lambda data: dataclasses.SamplingEvent(**data),
            "Site": lambda data: dataclasses.Site(**data),
            "Term": lambda data: dataclasses.Term(**data),
        }

    def get_config(self, fields=None):
        return self.storage.get_config()

    def dump(self, directory: str, config=None, fields=None) -> None:
        if config is None:
            config = self.get_config()

        if fields is None:
            fields = self.get_fields()

        if not os.path.exists(directory):
            os.makedirs(directory)

        self.storage.dump(
            directory,
            config=config,
            fields=fields,
        )

    @classmethod
    def load(
        cls,
        directory: str,
        name: str = "collection",
        config=None,
        constructors=None,
    ):
        if constructors is None:
            constructors = cls.get_constructors()

        return cls(
            Storages.load(
                directory,
                name=name,
                config=config,
                constructors=constructors,
            )
        )


for field in Collection.fields:
    setattr(Collection, field.lower(), build_field_property(field))
