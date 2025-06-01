#!/usr/bin/env python3
"""Utils module"""

from typing import Mapping, Sequence, Any, TypeVar, Callable
import requests

T = TypeVar('T')
Res = TypeVar('Res')


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """Get JSON from URL."""
    response = requests.get(url)
    return response.json()


def memoize(method: Callable[[T], Res]) -> Callable[[T], Res]:
    """Memoization decorator."""
    attr_name = "_{}".format(method.__name__)

    def wrapper(self: T) -> Res:
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
