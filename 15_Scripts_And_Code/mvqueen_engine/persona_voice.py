# mvqueen_engine/editorial/persona_voice.py
"""
MVQueen Persona Voice Generator — Enterprise Edition
----------------------------------------------------

Generates persona-driven editorial voice overlays using:
- Persona tone
- Emotional language
- Sensory language
- Movement language
- MVQueen luxury-hybrid editorial tone

Persona voice overlays:
- shape the emotional tone of descriptions
- guide the editorial personality
- reinforce MVQueen's feminine, cinematic identity
"""

from typing import Optional
from mvqueen_engine.brand_brain.brand_banks.persona_banks import PERSONA_TONES
from mvqueen_engine.brand_brain.brand_banks.extra_banks import (
    EMOTIONAL_LANGUAGE,
    SENSORY_LANGUAGE,
    MOVEMENT_LANGUAGE,
)
from mvqueen_engine.utils import choose_safe


# ------------------------------------------------------------
# PERSONA VOICE TEMPLATES — Cinematic, Feminine, MVQueen-Aligned
# ------------------------------------------------------------
PERSONA_VOICE_TEMPLATES = [
    (
        "{persona_tone} This piece feels {emotional}, moves with "
        "{movement}, and brings a {sensory} presence to your wardrobe."
    ),
    (
        "{persona_tone} Designed for women who embrace {emotional} "
        "moments, it moves with {movement} and feels {sensory}."
    ),
    (
        "{persona_tone} A blend of {sensory} texture and {movement} "
        "motion, wrapped in a {emotional} aura."
    ),
]


# ------------------------------------------------------------
# GENERATOR FUNCTION — Cinematic, Emotional, Persona-Driven
# ------------------------------------------------------------
def generate_persona_voice(persona: Optional[str] = None) -> str:
    """
    Generates a persona-driven editorial voice overlay.

    Returns:
        str
    """

    persona_tone = PERSONA_TONES.get(persona, "A modern feminine tone.")

    template = choose_safe(PERSONA_VOICE_TEMPLATES)

    return template.format(
        persona_tone=persona_tone,
        emotional=choose_safe(EMOTIONAL_LANGUAGE),
        sensory=choose_safe(SENSORY_LANGUAGE),
        movement=choose_safe(MOVEMENT_LANGUAGE),
    ).strip()


__all__ = ["generate_persona_voice"]