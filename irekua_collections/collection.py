from irekua_collections.storage import Storages


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
        "Prediction",
        "SamplingEvent",
        "Site",
        "Term",
        "UserAnnotation",
    ]

    def __init__(self):
        self.storage = Storages(self.fields)

    def __enter__(self):
        return self.storage.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.storage.__exit__(exc_type, exc_val, exc_tb)


for field in Collection.fields:
    setattr(Collection, field.lower(), build_field_property(field))
