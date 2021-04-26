from typing import Optional
from itertools import count


class DoesNotExist(Exception):
    """The object you are looking for does not exist in the collection"""


def satisfies_query(obj, query):
    for key, value in query.items():
        if not getattr(obj, key, None) == value:
            return False

    return True


class Storage:
    def __init__(self):
        self.objects = {}
        self.counter = count()

    def add(self, obj) -> None:
        id = next(self.counter)
        obj.id = id
        self.objects[id] = obj

    def filter(self, **query):
        for obj in self.objects.values():
            if satisfies_query(obj, query):
                yield obj

    def get_by_id(self, id):
        try:
            return self.objects[id]

        except KeyError:
            raise DoesNotExist(f"No object with id {id} exists")

    def get(self, id=None, **query):
        if id is not None:
            return self.get_by_id(id)

        options = list(self.filter(**query))
        if len(options) > 1:
            raise ValueError("Multiple matches")

        if len(options) == 0:
            raise ValueError("Does not exist")

        return options[0]


class Storages:
    storage_factory = Storage

    def __init__(self, fields=None):
        if fields is None:
            fields = []

        self.fields = fields
        self.storages = {field: self.storage_factory() for field in fields}

    def __contains__(self, key) -> bool:
        return key in self.storages

    def __getitem__(self, key) -> Storage:
        return self.storages[key]

    def __enter__(self):
        self.__current = get()
        set(self)

    def __exit__(self, *args):
        set(self.__current)


_default: Optional[Storages] = None


def get() -> Optional[Storages]:
    return _default


def set(storage: Storages) -> None:
    global _default

    if storage is None:
        _default = None
        return

    if not isinstance(storage, Storages):
        raise ValueError

    _default = storage
