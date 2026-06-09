# mvqueen_engine/editorial/ingredient_copy.py
"""
MVQueen Ingredient Copy Generator — Enterprise Edition
------------------------------------------------------

Generates feminine, benefit-forward ingredient explanations using:
- Detected skincare/beauty ingredients
- Emotional language
- Sensory language
- MVQueen luxury-hybrid editorial tone

Used for:
- Metafields
- Highlights
- Ingredient callouts
- SEO
"""

from typing import List
from mvqueen_engine.brand_brain.brand_banks.extra_banks import (
    EMOTIONAL_LANGUAGE,
    SENSORY_LANGUAGE,
)
from mvqueen_engine.utils import choose_safe


# ------------------------------------------------------------
# INGREDIENT COPY TEMPLATES — Feminine, Beauty-Forward, MVQueen-Aligned
# ------------------------------------------------------------
INGREDIENT_COPY_TEMPLATES = [
    "{ingredient} helps create a {emotional} glow with {sensory} softness.",
    "{ingredient} supports a {emotional} finish and enhances natural radiance.",
    "Powered by {ingredient} for a {sensory}, {emotional} feel.",
    "{ingredient} brings gentle, {sensory} nourishment to the skin.",
    "A touch of {ingredient} adds {emotional} clarity and {sensory} comfort.",
]


# ------------------------------------------------------------
# GENERATOR FUNCTION — Beauty-Forward, Sensory, Feminine
# ------------------------------------------------------------
def generate_ingredient_copy(ingredients: List[str]) -> List[str]:
    """
    Generates MVQueen ingredient copy lines.

    Returns:
        List[str]
    """

    if not ingredients:
        return []

    lines = []

    for ingredient in ingredients:
        template = choose_safe(INGREDIENT_COPY_TEMPLATES)
        line = template.format(
            ingredient=ingredient,
            emotional=choose_safe(EMOTIONAL_LANGUAGE),
            sensory=choose_safe(SENSORY_LANGUAGE),
        )
        lines.append(line)

    return lines


__all__ = ["generate_ingredient_copy"]