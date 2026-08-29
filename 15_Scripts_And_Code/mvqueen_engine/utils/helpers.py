"""Small dependency-free helpers shared across MVQueen modules."""
from __future__ import annotations
from collections.abc import Iterable


def first_nonempty(*values):
    for value in values:
        if value is not None and str(value).strip():
            return value
    return ""


def unique_preserve(items: Iterable) -> list:
    result = []
    seen = set()
    for item in items:
        key = str(item).casefold().strip()
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def as_list(value) -> list:
    if value is None or value == "":
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [part.strip() for part in str(value).replace(";", ",").split(",") if part.strip()]

__all__ = ["first_nonempty", "unique_preserve", "as_list"]
