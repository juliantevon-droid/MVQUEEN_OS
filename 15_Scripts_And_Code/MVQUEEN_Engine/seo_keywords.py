# mvqueen_engine/brand_brain/seo_keywords.py
"""
PHASE 1 — SEO KEYWORDS

Deterministic selection of focus + secondary + tertiary keywords.
"""

from mvqueen_engine.brand_brain.brand_banks import (
    PRIMARY_KEYWORDS,
    SECONDARY_KEYWORDS,
    KEYWORDS_900,
)
from mvqueen_engine.utils.deterministic import seed_from_text, pick_from_pool

def select_focus_keyword(handle: str) -> str:
    seeds = seed_from_text(handle + "_focus_kw")
    return pick_from_pool(PRIMARY_KEYWORDS, seeds[0])

def select_secondary_keyword(handle: str) -> str:
    seeds = seed_from_text(handle + "_secondary_kw")
    return pick_from_pool(SECONDARY_KEYWORDS, seeds[1])

def select_tertiary_keyword(handle: str) -> str:
    seeds = seed_from_text(handle + "_tertiary_kw")
    return pick_from_pool(KEYWORDS_900, seeds[2])

def get_keyword_stack(handle: str) -> dict:
    focus = select_focus_keyword(handle)
    secondary = select_secondary_keyword(handle)
    tertiary = select_tertiary_keyword(handle)
    return {
        "focus": focus,
        "secondary": secondary,
        "tertiary": tertiary,
        "combined": f"{focus}, {secondary}, {tertiary}",
    }