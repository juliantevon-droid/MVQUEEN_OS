"""Tone rules for persona-aware editorial generation."""

from __future__ import annotations

from .profiles import get_persona_profile

TONE_RULES = {
    "soft_luxury": {"pace": "gentle", "intensity": "low", "style": "sensory"},
    "clinical_chic": {"pace": "precise", "intensity": "medium", "style": "minimal"},
    "modern_confident": {"pace": "direct", "intensity": "high", "style": "assertive"},
    "mvqueen_signature": {"pace": "polished", "intensity": "medium", "style": "luxury"},
    "miss_queen_style": {"pace": "playful", "intensity": "medium", "style": "feminine"},
    "editorial_couture": {"pace": "dramatic", "intensity": "high", "style": "editorial"},
    "minimalist_luxe": {"pace": "restrained", "intensity": "low", "style": "quiet-luxury"},
    "sensory_beauty": {"pace": "intimate", "intensity": "medium", "style": "tactile"},
    "runway_modernity": {"pace": "sharp", "intensity": "high", "style": "architectural"},
    "feminine_empowerment": {"pace": "uplifting", "intensity": "high", "style": "empowering"},
}


def get_persona_tone(persona: str | None) -> dict:
    """Return normalized tone controls for a persona."""
    profile = get_persona_profile(persona)
    key = profile["name"].lower().replace(" ", "_").replace(".", "")
    return dict(TONE_RULES.get(key, TONE_RULES["mvqueen_signature"]))
