"""Shared deterministic keyword detection primitives."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from ...utils.deterministic import pick_from_pool


def normalize_text(value: Any) -> str:
    """Normalize arbitrary product input for case-insensitive matching."""
    if value is None:
        return ""
    return " ".join(str(value).casefold().split())


def detect_one(text: Any, vocabulary: Mapping[str, Sequence[str]], *, seed: Any = "fallback") -> str:
    """Return the first keyword match, or a deterministic vocabulary fallback."""
    normalized = normalize_text(text)
    for label, keywords in vocabulary.items():
        for keyword in keywords:
            if normalize_text(keyword) in normalized:
                return label
    return str(pick_from_pool(list(vocabulary), normalized, seed)) if vocabulary else ""


def detect_many(text: Any, vocabulary: Mapping[str, Sequence[str]]) -> list[str]:
    """Return all matching labels in vocabulary order."""
    normalized = normalize_text(text)
    matches: list[str] = []
    for label, keywords in vocabulary.items():
        if any(normalize_text(keyword) in normalized for keyword in keywords):
            matches.append(label)
    return matches
