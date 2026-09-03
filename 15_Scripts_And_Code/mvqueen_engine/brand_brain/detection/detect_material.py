"""Controlled material/fabric detection backed by the MVQueen brand vocabulary."""
from __future__ import annotations

import re

from ..brand_index import get_vocab


def _terms() -> tuple[str, ...]:
    """Return the union of material vocabularies in stable order."""
    values: list[str] = []
    for bank_name in ("fashion", "extra"):
        try:
            values.extend(get_vocab(bank_name, "MATERIALS"))
        except AttributeError:
            continue
    return tuple(dict.fromkeys(str(value).strip().lower() for value in values if str(value).strip()))


def detect_material(text: str) -> str:
    """Return the first controlled material found in source text."""
    value = str(text or "").casefold()
    for material in _terms():
        pattern = rf"(?<!\\w){re.escape(material.casefold())}(?!\\w)"
        if re.search(pattern, value):
            return material
    return "unspecified"


__all__ = ["detect_material"]
