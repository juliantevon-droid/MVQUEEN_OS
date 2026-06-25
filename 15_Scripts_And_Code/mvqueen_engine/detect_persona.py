# mvqueen_engine/detection/detect_persona.py
"""
MVQueen Persona Detection
-------------------------

This module determines which MVQueen persona best aligns with the
product’s language, materials, silhouette, movement, and emotional tone.

Persona detection is built from:
- MVQueen persona banks
- Sensory language
- Movement language
- Texture + finish language
- Category + product type signals
- Emotional vocabulary
- Feminine, luxury-hybrid editorial logic

This is NOT random.
This is MVQueen persona intelligence.
"""

from typing import Optional
from mvqueen_engine.utils import normalize_for_detection, first_match
from mvqueen_engine.brand_brain.brand_banks.persona_banks import (
    PERSONA_NAMES,
    PERSONA_TONES,
)
from mvqueen_engine.brand_brain.brand_banks.extra_banks import (
    SENSORY_LANGUAGE,
    MOVEMENT_LANGUAGE,
    TEXTURE_LANGUAGE,
    FINISH_LANGUAGE,
    EMOTIONAL_LANGUAGE,
)


# ------------------------------------------------------------
# KEYWORD MAP — Persona-Specific Signals
# ------------------------------------------------------------
PERSONA_KEYWORDS = {
    "Runway Muse": [
        "runway", "couture", "editorial", "dramatic", "cinematic",
        "bias cut", "satin", "silk", "fluid", "movement",
        "catches the light", "high-fashion",
    ],
    "Soft Minimalist": [
        "minimal", "clean", "refined", "simple", "quiet luxury",
        "soft structure", "smooth", "sleek", "modern", "calm",
    ],
    "Romantic Visionary": [
        "romantic", "feminine", "soft", "flowy", "dreamy",
        "warm", "gentle", "lace", "ruffle", "floral",
    ],
    "Bold Architect": [
        "structured", "sharp", "tailored", "geometric",
        "sculpted", "defined", "strong lines", "precision",
    ],
    "Classic Strategist": [
        "timeless", "polished", "elegant", "classic",
        "refined", "enduring", "sophisticated",
    ],
    "Velvet Rebel": [
        "sensual", "undone", "intimate", "cool", "velvet",
        "body-hugging", "curve", "soft edge", "seductive",
    ],
    "Ethereal Siren": [
        "glow", "luminous", "ethereal", "soft-focus",
        "sheer", "light", "angelic", "radiant",
    ],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Feminine, Cinematic, Deterministic
# ------------------------------------------------------------
def detect_persona(text: str) -> Optional[str]:
    """
    Determines the MVQueen persona that best matches the product.

    Steps:
    1. Normalize text.
    2. Score each persona based on keyword presence.
    3. Add bonus scoring for sensory, movement, texture, finish,
       and emotional language.
    4. Return the persona with the highest score.

    Returns:
        str or None
    """
    if not text:
        return None

    normalized = normalize_for_detection(text)
    score_map = {persona: 0 for persona in PERSONA_NAMES}

    # Persona keyword scoring
    for persona, keywords in PERSONA_KEYWORDS.items():
        for k in keywords:
            if k in normalized:
                score_map[persona] += 3  # persona-specific signals are strong

    # Sensory language scoring
    for phrase in SENSORY_LANGUAGE:
        if phrase.split()[0] in normalized:
            score_map["Ethereal Siren"] += 2
            score_map["Runway Muse"] += 1

    # Movement language scoring
    for phrase in MOVEMENT_LANGUAGE:
        if phrase.split()[0] in normalized:
            score_map["Runway Muse"] += 2
            score_map["Romantic Visionary"] += 1

    # Texture scoring
    for word in TEXTURE_LANGUAGE:
        if word in normalized:
            score_map["Soft Minimalist"] += 2
            score_map["Velvet Rebel"] += 1

    # Finish scoring
    for word in FINISH_LANGUAGE:
        if word in normalized:
            score_map["Ethereal Siren"] += 2
            score_map["Runway Muse"] += 1

    # Emotional scoring
    for word in EMOTIONAL_LANGUAGE:
        if word.split()[0] in normalized:
            score_map["Romantic Visionary"] += 2
            score_map["Classic Strategist"] += 1

    # Determine winner
    best_persona = max(score_map, key=score_map.get)

    # If no meaningful score, return None
    if score_map[best_persona] == 0:
        return None

    return best_persona


__all__ = ["detect_persona"]