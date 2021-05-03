from typing import Union


def union(other_type):
    def decorator(type_hint):
        return Union[other_type, type_hint]

    return decorator
