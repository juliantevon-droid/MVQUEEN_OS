"""Detect explicitly named cosmetic/skincare ingredients."""
from __future__ import annotations

INGREDIENTS = ("retinol", "niacinamide", "vitamin c", "hyaluronic acid", "salicylic acid", "glycolic acid", "lactic acid", "ceramides", "peptides", "squalane", "jojoba", "shea butter", "aloe", "vitamin e", "collagen", "bakuchiol", "azelaic acid", "zinc oxide", "titanium dioxide")

def detect_ingredients(text: str) -> list[str]:
    value = str(text or "").lower()
    return [ingredient for ingredient in INGREDIENTS if ingredient in value]
