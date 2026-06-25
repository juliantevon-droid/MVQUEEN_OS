# mvqueen_engine/editorial/title.py
"""
MVQueen Title Generator — Enterprise Edition
--------------------------------------------

Generates MVQueen titles using:
- Persona tone
- Vibe
- Trend
- Silhouette
- Material
- Finish
- Texture
- Emotional language
- MVQueen luxury-hybrid editorial tone
"""

from typing import Optional
from mvqueen_engine.brand_brain.brand_banks.persona_banks import PERSONA_TONES
from mvqueen_engine.brand_brain.brand_banks.extra_banks import (
    EMOTIONAL_LANGUAGE,
    FINISH_LANGUAGE,
    TEXTURE_LANGUAGE,
)
from mvqueen_engine.utils.helpers import choose_safe


TITLE_TEMPLATES = [
    "{silhouette} in {material} with a {finish} finish",
    "{persona} {silhouette} crafted in {material}",
    "{vibe} {silhouette} with {texture} texture",
    "{trend} {silhouette} in soft {material}",
    "{silhouette} with {emotional} presence",
]


def generate_title(
    persona: Optional[str] = None,
    silhouette: Optional[str] = None,
    material: Optional[str] = None,
    finish: Optional[str] = None,
    texture: Optional[str] = None,
    vibe: Optional[str] = None,
    trend: Optional[str] = None,
) -> str:

    template = choose_safe(TITLE_TEMPLATES)

    return template.format(
        persona=persona or "",
        silhouette=silhouette or "silhouette",
        material=material or "luxury fabric",
        finish=finish or choose_safe(FINISH_LANGUAGE),
        texture=texture or choose_safe(TEXTURE_LANGUAGE),
        vibe=vibe or "modern",
        trend=trend or "editorial",
        emotional=choose_safe(EMOTIONAL_LANGUAGE),
    ).strip().title()


__all__ = ["generate_title"]