import json
import os
from irekua_collections.storage import Storages
from irekua_collections import dataclasses


def build_field_property(field_name):
    def getter(self):
        return self.storage[field_name]

    return property(getter)


class Collection:
    fields = [
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
            storage = Storages(self.get_fields())

        self.storage = storage

    def __enter__(self):
        return self.storage.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.storage.__exit__(exc_type, exc_val, exc_tb)

    @classmethod
    def get_constructors(cls):
        return {
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
        if fields is None:
            fields = self.fields

        return {
            "fields": fields,
            "directories": {
                key: key.lower().replace(" ", "_") for key in fields
            },
        }

    def save_config(self, directory, config=None):
        if config is None:
            config = self.get_config()

        path = os.path.join(directory, "collection.json")
        with open(path, "w") as jsonfile:
            json.dump(config, jsonfile)

    @staticmethod
    def load_config(directory):
        if not os.path.exists(directory):
            raise IOError(f"Directory does not exist {directory}")

        config_file = os.path.join(directory, "collection.json")

        if not os.path.exists(config_file):
            raise ValueError("No storage configuration file at directory")

        return load_json(config_file)

    def dump(self, directory: str, config=None, fields=None) -> None:
        if config is None:
            config = self.get_config()

        if fields is None:
            fields = self.get_fields()

        if not os.path.exists(directory):
            os.makedirs(directory)

        self.save_config(directory, config=config)

        self.storage.dump(
            directory,
            config=config,
            fields=fields,
        )

    @classmethod
    def load(cls, directory: str, config=None, constructors=None):
        if config is None:
            config = cls.load_config(directory)

        if constructors is None:
            constructors = cls.get_constructors()

        return cls(
            Storages.load(
                directory,
                config=config,
                constructors=constructors,
            )
        )


for field in Collection.fields:
    setattr(Collection, field.lower(), build_field_property(field))


def load_json(path):
    with open(path, "r") as jsonfile:
        return json.load(jsonfile)
