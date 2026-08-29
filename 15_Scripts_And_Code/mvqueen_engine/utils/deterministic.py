"""Deterministic helpers for reproducible MVQueen processing."""
from __future__ import annotations
import hashlib
import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def seed_for(value: object, seed: int | str = 0) -> int:
    raw = f"{seed}:{value}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")


def choice(items: Sequence[T], key: object = "", seed: int | str = 0) -> T:
    if not items:
        raise ValueError("choice requires at least one item")
    return items[random.Random(seed_for(key, seed)).randrange(len(items))]


def multi(items: Sequence[T], count: int, key: object = "", seed: int | str = 0) -> list[T]:
    if count < 0:
        raise ValueError("count cannot be negative")
    if count > len(items):
        raise ValueError("count cannot exceed item count")
    rng = random.Random(seed_for(key, seed))
    return rng.sample(list(items), count)

__all__ = ["seed_for", "choice", "multi"]
