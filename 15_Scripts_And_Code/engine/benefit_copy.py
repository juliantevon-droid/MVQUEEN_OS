# mvqueen_engine/editorial/benefit_copy.py
"""
MVQueen Benefit Copy Generator — Enterprise Edition
---------------------------------------------------

Generates feminine, sensory, benefit-forward copy using:
- Detected benefits
- Emotional language
- Sensory language
- Movement language
- MVQueen luxury-hybrid editorial tone

Used for:
- Metafields
- Highlights
- Short-form bullets
- Product cards
- SEO snippets
"""

from typing import List
from mvqueen_engine.brand_brain.brand_banks.extra_banks import (
    EMOTIONAL_LANGUAGE,
    SENSORY_LANGUAGE,
    MOVEMENT_LANGUAGE,
)
from mvqueen_engine.utils import choose_safe


# ------------------------------------------------------------
# BENEFIT COPY TEMPLATES — Cinematic, Feminine, MVQueen-Aligned
# ------------------------------------------------------------
BENEFIT_COPY_TEMPLATES = [
    "Creates a {emotional} feel with {sensory} softness.",
    "Designed to {movement} while offering {benefit} comfort.",
    "Brings a {emotional} glow and {benefit} support.",
    "Feels {sensory} against the skin while enhancing {benefit}.",
    "A blend of {benefit} performance and {emotional} ease.",
]


# ------------------------------------------------------------
# GENERATOR FUNCTION — Sensory, Feminine, Benefit-Forward
# ------------------------------------------------------------
def generate_benefit_copy(benefits: List[str]) -> List[str]:
    """
    Generates MVQueen benefit copy lines.

    Returns:
        List[str]
    """

    if not benefits:
        return []

    lines = []

    for benefit in benefits:
        template = choose_safe(BENEFIT_COPY_TEMPLATES)
        line = template.format(
            benefit=benefit,
            emotional=choose_safe(EMOTIONAL_LANGUAGE),
            sensory=choose_safe(SENSORY_LANGUAGE),
            movement=choose_safe(MOVEMENT_LANGUAGE),
        )
        lines.append(line)

    return lines


__all__ = ["generate_benefit_copy"]