#!/usr/bin/env python3
"""Utils module"""

from typing import Mapping, Sequence, Any, TypeVar, Callable
import requests

T = TypeVar('T')
Res = TypeVar('Res')

# Utility functions for accessing nested maps, fetching JSON, and memoization
def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

# Utility function to get JSON from a URL
def get_json(url: str) -> Any:
    """Get JSON from URL."""
    response = requests.get(url)
    return response.json()

# Utility function for memoization
def memoize(method: Callable[[T], Res]) -> Callable[[T], Res]:
    """Memoization decorator."""
    attr_name = "_{}".format(method.__name__)
#    """Decorator to cache method results."""
    def wrapper(self: T) -> Res:
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
