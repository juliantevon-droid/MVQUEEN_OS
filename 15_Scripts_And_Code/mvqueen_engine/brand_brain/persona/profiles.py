"""Canonical persona profiles for MVQueen editorial routing."""
from __future__ import annotations

PERSONA_PROFILES = {
    "modern_luxury_consumer": {
        "label": "Modern Luxury Consumer",
        "tone": "refined, confident, contemporary",
        "voice": "luxury-modern-elegant",
        "keywords": ("luxury", "premium", "elevated", "refined"),
    },
    "style_forward_individual": {
        "label": "Style-Forward Individual",
        "tone": "confident, expressive, polished",
        "voice": "statement-elegance",
        "keywords": ("style", "fashion", "trend", "statement"),
    },
    "quality_driven_customer": {
        "label": "Quality-Driven Customer",
        "tone": "precise, assured, quality-focused",
        "voice": "timeless-refinement",
        "keywords": ("quality", "craftsmanship", "durable", "premium"),
    },
    "elevated_lifestyle_shopper": {
        "label": "Elevated Lifestyle Shopper",
        "tone": "warm, composed, aspirational",
        "voice": "quiet-opulence",
        "keywords": ("lifestyle", "everyday", "comfort", "elevated"),
    },
}

DEFAULT_PERSONA = "modern_luxury_consumer"


def get_profile(persona: str | None) -> dict:
    return dict(PERSONA_PROFILES.get(persona or "", PERSONA_PROFILES[DEFAULT_PERSONA]))


__all__ = ["PERSONA_PROFILES", "DEFAULT_PERSONA", "get_profile"]
