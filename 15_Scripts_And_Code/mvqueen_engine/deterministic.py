# mvqueen_engine/deterministic.py
"""Deterministic, dependency-free helpers for MVQUEEN catalog tooling."""
from __future__ import annotations

import hashlib
import random
from typing import Iterable, Sequence, TypeVar

T = TypeVar("T")


def seed_from_text(text: str) -> list[int]:
    """Generate a stable array of integer seeds from arbitrary text."""
    if not isinstance(text, str):
        text = str(text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return [int(digest[i:i + 8], 16) for i in range(0, 64, 8)]


def deterministic_seed(text: str) -> int:
    """Return one stable integer seed for older deterministic engine modules."""
    return seed_from_text(text)[0]


def _salted_seed(seed: int, salt: str = "") -> int:
    payload = f"{int(seed)}::{salt}"
    return int(hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16], 16)


def deterministic_choice(seed: int, pool: Sequence[T], *, salt: str = "") -> T | None:
    """Choose from a sequence without depending on process-global randomness."""
    if not pool:
        return None
    rng = random.Random(_salted_seed(seed, salt))
    return pool[rng.randrange(len(pool))]


def deterministic_shuffle(seed: int, values: Iterable[T], *, salt: str = "") -> list[T]:
    """Return a stable shuffled copy."""
    output = list(values)
    random.Random(_salted_seed(seed, salt)).shuffle(output)
    return output


def pick_from_pool(pool: Sequence[T], seed: int) -> T | str:
    """Legacy deterministic list selection."""
    if not pool:
        return ""
    return pool[int(seed) % len(pool)]


def pick_multiple(pool: Sequence[T], seeds: Sequence[int], count: int = 3) -> list[T]:
    """Pick multiple stable values while preserving legacy semantics."""
    if not pool:
        return []
    return [pool[int(seed) % len(pool)] for seed in list(seeds)[:count]]


def truncate(text: str, max_len: int) -> str:
    """Truncate to a character limit while preferring a whole-word boundary."""
    if not isinstance(text, str):
        text = str(text)
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(" ", 1)[0] or text[:max_len]
    return cut.rstrip() + "…"


__all__ = [
    "seed_from_text",
    "deterministic_seed",
    "deterministic_choice",
    "deterministic_shuffle",
    "pick_from_pool",
    "pick_multiple",
    "truncate",
]
