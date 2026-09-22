"""Deterministic product image alt-text generation for MVQueen."""

from __future__ import annotations

import re


def generate_alt_text(base_title: str, handle: str) -> str:
    """Describe the product without inventing color, material, or lifestyle claims."""
    title = re.sub(r"\s+", " ", str(base_title or "")).strip()
    title = re.sub(r"(?i)^mvqueen\s*[|:-]\s*", "", title)
    return f"{title} — MVQueen" if title else "MVQueen product image"
