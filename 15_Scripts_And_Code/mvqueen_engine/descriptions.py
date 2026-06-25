# mvqueen_engine/editorial/description.py
"""
MVQueen Description Generator — Enterprise Edition
--------------------------------------------------

Persona-aware, cinematic, atmospheric, and grammatically correct.
"""

from typing import List, Optional
from mvqueen_engine.brand_brain.brand_banks.extra_banks import (
    SENSORY_LANGUAGE,
    MOVEMENT_LANGUAGE,
    EMOTIONAL_LANGUAGE,
    ATMOSPHERIC_LANGUAGE,
)
from mvqueen_engine.utils import choose_safe


# ------------------------------------------------------------
# Verb Conjugation (3rd person singular)
# ------------------------------------------------------------
VERB_MAP = {
    "smooth": "smooths",
    "soften": "softens",
    "define": "defines",
    "sculpt": "sculpts",
    "refine": "refines",
    "wrap": "wraps",
    "release": "releases",
    "follow": "follows",
    "glow": "glows",
}

def conj(verb: str) -> str:
    return VERB_MAP.get(verb, verb + "s")


# ------------------------------------------------------------
# Description Templates (persona-aware)
# ------------------------------------------------------------
DESCRIPTION_TEMPLATES = [
    (
        "Inspired by {vibe}, this {silhouette} silhouette blends {material} "
        "with {texture} texture for a refined, feminine presence. Designed to "
        "{movement} with ease, it {verb_smooth} the lines softly. Finished "
        "with a {finish} glow, it {verb_glow} against the skin. {atmosphere}"
    ),
    (
        "This {trend}-inspired {silhouette} moves with {movement}, wrapped in "
        "{material} that feels {sensory}. It {verb_smooth} the silhouette and "
        "adds a {finish} finish for elevated clarity. {atmosphere}"
    ),
    (
        "A modern take on {vibe}, this {silhouette} pairs {material} with "
        "{texture} dimension. Designed to {movement}, it {verb_refine} the "
        "shape with feminine ease. Finished with a {finish} touch. "
        "{atmosphere}"
    ),
]


# ------------------------------------------------------------
# MAIN GENERATOR
# ------------------------------------------------------------
def generate_description(
    persona: Optional[dict] = None,
    silhouette: Optional[str] = None,
    material: Optional[str] = None,
    texture: Optional[str] = None,
    finish: Optional[str] = None,
    vibe: Optional[str] = None,
    trend: Optional[str] = None,
    details: Optional[List[str]] = None,
) -> str:

    template = choose_safe(DESCRIPTION_TEMPLATES)

    # Persona-aware movement + sensory
    persona_movement = persona.get("movement") if isinstance(persona, dict) else None
    persona_sensory = persona.get("sensory") if isinstance(persona, dict) else None

    detail_phrase = (
        ", ".join(details) if details else "soft, feminine detailing"
    )

    return template.format(
        silhouette=silhouette or "silhouette",
        material=material or "luxury fabric",
        texture=texture or "soft",
        finish=finish or "luminous",
        vibe=vibe or "modern minimalism",
        trend=trend or "editorial",
        details=detail_phrase,

        # Persona-aware language
        sensory=persona_sensory or choose_safe(SENSORY_LANGUAGE),
        movement=persona_movement or choose_safe(MOVEMENT_LANGUAGE),

        # Conjugated verbs
        verb_smooth=conj("smooth"),
        verb_glow=conj("glow"),
        verb_refine=conj("refine"),

        # Emotional + atmospheric
        emotional=choose_safe(EMOTIONAL_LANGUAGE),
        atmosphere=choose_safe(ATMOSPHERIC_LANGUAGE),
    ).strip()


__all__ = ["generate_description"]