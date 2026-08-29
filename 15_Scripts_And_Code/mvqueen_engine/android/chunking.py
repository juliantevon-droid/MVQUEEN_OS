"""Small, dependency-free chunking primitives."""
from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


def chunks(items: Iterable[T], size: int = 850) -> Iterator[list[T]]:
    if size < 1:
        raise ValueError("size must be positive")
    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch
