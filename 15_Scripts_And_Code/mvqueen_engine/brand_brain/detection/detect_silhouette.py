"""Fashion silhouette detection backed by the MVQueen brand vocabulary."""
from __future__ import annotations

import re

from ..brand_index import get_vocab


def _terms() -> tuple[str, ...]:
    """Return controlled silhouette terms from the fashion bank."""
    return tuple(
        dict.fromkeys(
            str(value).strip().lower()
            for value in get_vocab("fashion", "SILHOUETTES")
            if str(value).strip()
        )
    )


def detect_silhouette(text: str) -> str:
    """Return the first controlled silhouette found in source text."""
    value = str(text or "").casefold()
    for item in _terms():
        if re.search(rf"(?<!\\w){re.escape(item.casefold())}(?!\\w)", value):
            return item
    return "unspecified"


__all__ = ["detect_silhouette"]
