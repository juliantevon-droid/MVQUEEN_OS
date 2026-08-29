"""Canonical casing, spacing, and Unicode normalization for MVQueen."""
from __future__ import annotations
import re
import unicodedata


def normalize_text(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    text = text.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_key(value: object) -> str:
    text = normalize_text(value).casefold()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text

__all__ = ["normalize_text", "normalize_key"]
