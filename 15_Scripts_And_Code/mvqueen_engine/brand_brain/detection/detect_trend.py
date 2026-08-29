"""Fashion/beauty trend signal detection."""
from __future__ import annotations

TRENDS = ("quiet luxury", "old money", "minimalist", "clean girl", "coastal", "boho", "romantic", "streetwear", "athleisure", "90s", "y2k", "capsule wardrobe", "glazed", "dewy", "glass skin")

def detect_trend(text: str) -> str:
    value = str(text or "").lower()
    return next((trend for trend in TRENDS if trend in value), "timeless")
