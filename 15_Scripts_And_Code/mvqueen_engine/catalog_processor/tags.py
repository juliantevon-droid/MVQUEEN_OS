"""Deterministic MVQueen tag construction."""
from __future__ import annotations

from collections.abc import Iterable, Mapping

BASE_TAGS = ("mvqueen", "curated")


def build_tags(data: Mapping[str, object], existing: Iterable[str] = ()) -> list[str]:
    """Merge existing tags with structured intelligence without duplicates."""
    values: list[str] = []
    seen: set[str] = set()

    def add(value: object) -> None:
        text = str(value or "").strip()
        if text and text.lower() not in seen:
            seen.add(text.lower())
            values.append(text)

    for value in existing:
        add(value)
    for value in BASE_TAGS:
        add(value)
    for key in ("category", "product_type", "persona", "vibe", "trend", "season", "material", "silhouette", "occasion", "fit"):
        add(data.get(key))
    for key in ("details", "benefits"):
        value = data.get(key, [])
        if isinstance(value, (list, tuple, set)):
            for item in value:
                add(item)
        else:
            add(value)
    return values


def tags_csv(data: Mapping[str, object], existing: Iterable[str] = ()) -> str:
    return ", ".join(build_tags(data, existing))
