"""Seasonality detection."""
from __future__ import annotations

SEASONS = {"spring": ("spring", "floral", "pastel", "lightweight"), "summer": ("summer", "resort", "beach", "linen", "breezy"), "fall": ("fall", "autumn", "knit", "wool", "suede"), "winter": ("winter", "holiday", "faux fur", "cashmere", "velvet")}

def detect_season(text: str) -> str:
    value = str(text or "").lower()
    scores = {name: sum(term in value for term in terms) for name, terms in SEASONS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "year_round"
