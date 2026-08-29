"""Surface/cosmetic finish detection."""
from __future__ import annotations

FINISHES = ("matte", "satin", "satin-finish", "gloss", "glossy", "luminous", "radiant", "dewy", "natural finish", "soft matte", "metallic", "shimmer", "sparkle", "polished", "refined matte")

def detect_finishes(text: str) -> list[str]:
    value = str(text or "").lower()
    return [finish for finish in FINISHES if finish in value]
