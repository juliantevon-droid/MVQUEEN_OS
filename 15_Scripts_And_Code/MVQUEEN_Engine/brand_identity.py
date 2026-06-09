# brand_brain/brand_index.py
"""
MVQueen Brand Index — Enterprise Edition
----------------------------------------

The central identity map of the MVQueen Omniluxe Engine.

This file unifies:
- Persona system
- Brand banks
- Editorial identity anchors
- Emotional + sensory vocabularies
- Fashion + beauty + skincare lexicons
- SEO language
- Business tiers
- Brand constants

This is the single source of truth for the brand brain.
"""

# Persona System
from .persona import (
    PERSONA_PROFILES,
    PERSONA_TONES,
    apply_persona_rules,
    route_persona,
)

# Brand Banks
from brand_brain.brand_banks import (
    extra_banks,
    fashion_banks,
    beauty_banks,
    skincare_banks,
    seo_banks,
    persona_banks,
    business_banks,
)


# ------------------------------------------------------------
# BRAND IDENTITY CONSTANTS
# ------------------------------------------------------------
BRAND_NAME = "MVQueen"
BRAND_TONE = "women-centered, cinematic, sensory, atmospheric, luxury-hybrid"
BRAND_PHILOSOPHY = (
    "A brand built on softness, confidence, movement, and feminine clarity."
)


# ------------------------------------------------------------
# BRAND INDEX — Unified Identity Map
# ------------------------------------------------------------
BRAND_INDEX = {
    "brand": {
        "name": BRAND_NAME,
        "tone": BRAND_TONE,
        "philosophy": BRAND_PHILOSOPHY,
    },

    "persona_system": {
        "profiles": PERSONA_PROFILES,
        "tones": PERSONA_TONES,
        "router": route_persona,
        "rules": apply_persona_rules,
    },

    "banks": {
        "extra": extra_banks,
        "fashion": fashion_banks,
        "beauty": beauty_banks,
        "skincare": skincare_banks,
        "seo": seo_banks,
        "persona": persona_banks,
        "business": business_banks,
    },
}

__all__ = ["BRAND_INDEX"]