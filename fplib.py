"""Reusable, side-effect-free collection helpers."""

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")


def pipe(value: T, *functions: Callable[[Any], Any]) -> Any:
    """Pass a value through functions from left to right."""
    result: Any = value
    for function in functions:
        result = function(result)
    return result


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose functions so the rightmost function runs first."""
    def composed(value: Any) -> Any:
        result = value
        for function in reversed(functions):
            result = function(result)
        return result

    return composed


def map_items(items: Iterable[T], transform: Callable[[T], U]) -> list[U]:
    """Return a new list with transform applied to every item."""
    return [transform(item) for item in items]


def filter_items(items: Iterable[T], predicate: Callable[[T], bool]) -> list[T]:
    """Return a new list containing items that match predicate."""
    return [item for item in items if predicate(item)]


def sum_by(items: Iterable[T], selector: Callable[[T], int | float]) -> int | float:
    """Sum a numeric value selected from each item."""
    return sum(selector(item) for item in items)


def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group items by a key, preserving their original order."""
    groups: dict[K, list[T]] = {}
    for item in items:
        groups.setdefault(key(item), []).append(item)
    return groups


def unique_by(items: Iterable[T], key: Callable[[T], K]) -> list[T]:
    """Return the first item for each distinct key."""
    result: list[T] = []
    seen: set[K] = set()
    for item in items:
        item_key = key(item)
        if item_key not in seen:
            seen.add(item_key)
            result.append(item)
    return result


def sort_by(
    items: Iterable[T],
    key: Callable[[T], Any],
    reverse: bool = False,
) -> list[T]:
    """Return a new list sorted by key."""
    return sorted(items, key=key, reverse=reverse)
