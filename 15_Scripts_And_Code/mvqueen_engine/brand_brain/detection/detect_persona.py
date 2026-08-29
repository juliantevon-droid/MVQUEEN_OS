"""Audience/persona detection."""
from __future__ import annotations

PERSONAS = {
    "modern_luxury_consumer": ("luxury", "premium", "elevated", "designer", "prestige"),
    "style_forward_individual": ("style", "fashion", "trend", "statement", "chic"),
    "quality_driven_customer": ("quality", "craftsmanship", "durable", "long lasting", "premium"),
    "beauty_connoisseur": ("beauty", "skincare", "serum", "complexion", "glow", "cosmetic"),
}

def detect_persona(text: str) -> str:
    value = str(text or "").lower()
    scores = {name: sum(term in value for term in terms) for name, terms in PERSONAS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "modern_luxury_consumer"
