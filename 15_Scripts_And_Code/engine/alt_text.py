# mvqueen_engine/brand_brain/alt_text.py
"""
PHASE 1 — ALT TEXT ENGINE

Generates curated, persona-aware alt text for product images.
"""

from mvqueen_engine.config import BRAND_NAME
from mvqueen_engine.brand_brain.brand_language import (
    select_persona_from_handle,
    select_sensory_word,
    select_fashion_term,
    select_occasion,
)
from mvqueen_engine.utils.deterministic import seed_from_text, truncate

def generate_alt_text(base_title: str, handle: str, product_type: str = "Outfit") -> str:
    persona = select_persona_from_handle(handle)
    sensory = select_sensory_word(handle)
    fashion_term = select_fashion_term(handle)
    occasion = select_occasion(handle)

    raw = (
        f"{BRAND_NAME} {base_title} {product_type.lower()} on model, "
        f"showing {sensory} {fashion_term} details for {occasion.lower()}."
        f" Styled in {persona.lower()} mood."
    )
    return truncate(raw, 120)