# persona/persona_rules.py
"""
MVQueen Persona Rules — Enterprise Edition
------------------------------------------

Two-layer persona intelligence system:

1. apply_persona_rules(profile) → returns full persona rule dict
2. route_persona(profile)       → returns persona key (handled in router.py)

This file now provides the persona emotional, tonal, sensory,
and movement signatures for each persona.
"""

from typing import Dict


# ------------------------------------------------------------
# PERSONA RULE DICTIONARY (full emotional + tonal identity)
# ------------------------------------------------------------
PERSONA_RULES = {
    "romantic": {
        "tone": "soft, feminine, atmospheric",
        "emotion": "warmth, tenderness, intimacy",
        "movement": "flowy, draped, effortless",
        "sensory": "soft-focus texture, airy light",
        "identity": "Romantic, expressive, dreamy.",
    },
    "bold": {
        "tone": "confident, striking, high-impact",
        "emotion": "power, intensity, presence",
        "movement": "sculpted, structured, directional",
        "sensory": "sharp contrast, defined edges",
        "identity": "Bold, commanding, unapologetic.",
    },
    "minimalist": {
        "tone": "clean, quiet, refined",
        "emotion": "calm, clarity, restraint",
        "movement": "sleek, linear, architectural",
        "sensory": "smooth surfaces, subtle texture",
        "identity": "Minimalist, modern, essential.",
    },
    "glam": {
        "tone": "luminous, radiant, luxurious",
        "emotion": "celebratory, elevated, glowing",
        "movement": "polished, fluid, spotlight-ready",
        "sensory": "shine, sparkle, glow",
        "identity": "Glamorous, radiant, high-shine.",
    },
    "editorial": {
        "tone": "artistic, moody, elevated",
        "emotion": "soft-focus emotion",
        "movement": "sculpted, directional motion",
        "sensory": "dimensional texture",
        "identity": "Cinematic, atmospheric, expressive.",
    },
    "soft": {
        "tone": "gentle, airy, cloudlike",
        "emotion": "comfort, ease, softness",
        "movement": "floaty, relaxed, breathable",
        "sensory": "pillowy texture, diffused light",
        "identity": "Soft, delicate, serene.",
    },
    "confident": {
        "tone": "sleek, modern, assertive",
        "emotion": "clarity, strength, focus",
        "movement": "structured, intentional, defined",
        "sensory": "smooth lines, crisp edges",
        "identity": "Confident, modern, empowered.",
    },
}


# ------------------------------------------------------------
# RULE ENGINE — Determines persona key
# ------------------------------------------------------------
def _route_persona_key(profile: Dict) -> str:
    """
    Internal routing logic (your original rules).
    Returns persona key as string.
    """

    vibe = profile.get("vibe", "")
    trend = profile.get("trend", "")
    silhouette = profile.get("silhouette", "")
    material = profile.get("material", "")
    product_type = profile.get("product_type", "")

    # 1. VIBE-BASED ROUTING
    if vibe in ["romantic", "soft", "feminine"]:
        return "romantic"
    if vibe in ["bold", "striking", "power"]:
        return "bold"
    if vibe in ["minimal", "clean", "quiet"]:
        return "minimalist"
    if vibe in ["glam", "luminous", "radiant"]:
        return "glam"
    if vibe in ["editorial", "moody", "cinematic"]:
        return "editorial"

    # 2. TREND-BASED ROUTING
    if trend in ["runway", "couture", "avant-garde"]:
        return "editorial"
    if trend in ["softcore", "airy", "cloud"]:
        return "soft"
    if trend in ["sleek", "structured", "modern"]:
        return "confident"

    # 3. SILHOUETTE-BASED ROUTING
    if silhouette in ["bodycon", "sculpted", "structured"]:
        return "bold"
    if silhouette in ["flowy", "draped", "soft"]:
        return "romantic"

    # 4. MATERIAL-BASED ROUTING
    if material in ["silk", "satin", "chiffon"]:
        return "romantic"
    if material in ["leather", "structured knit"]:
        return "confident"

    # 5. PRODUCT TYPE ROUTING
    if product_type in ["evening gown", "cocktail dress"]:
        return "glam"
    if product_type in ["basics", "essentials"]:
        return "minimalist"

    # DEFAULT
    return "editorial"


# ------------------------------------------------------------
# PUBLIC API — Returns full persona rule dict
# ------------------------------------------------------------
def apply_persona_rules(profile: Dict) -> Dict:
    """
    Returns the full persona rule dictionary for the routed persona.
    """
    persona_key = _route_persona_key(profile)
    return PERSONA_RULES.get(persona_key, PERSONA_RULES["editorial"])


__all__ = ["apply_persona_rules", "PERSONA_RULES"]