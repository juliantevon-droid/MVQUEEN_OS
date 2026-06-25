# mvqueen_engine/detection/detect_finishes.py
"""
MVQueen Finish Detection — Enterprise Edition
---------------------------------------------

Cross-category finish detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories

Finishes shape:
- Editorial descriptions
- SEO
- Persona routing
- Metafields
- Tag generation
"""

from typing import List
from mvqueen_engine.utils.normalization import normalize_for_detection


# ------------------------------------------------------------
# FINISH KEYWORD MAP — Expanded for All MVQueen Domains
# ------------------------------------------------------------
FINISH_KEYWORDS = {
    # --------------------------------------------------------
    # BEAUTY + SKINCARE FINISHES
    # --------------------------------------------------------
    "luminous": ["luminous", "glow", "glowing", "radiant", "light-catching"],
    "matte": ["matte", "soft matte", "velvet matte"],
    "satin": ["satin finish", "satin sheen", "soft sheen"],
    "glossy": ["glossy", "high-shine", "shine", "gloss"],
    "soft-focus": ["soft-focus", "diffused", "blurred", "airbrushed"],
    "sheer": ["sheer", "semi-sheer", "translucent"],
    "dewy": ["dewy", "fresh glow"],

    # --------------------------------------------------------
    # FASHION FINISHES
    # --------------------------------------------------------
    "polished": ["polished", "refined finish", "clean finish"],
    "textured": ["textured finish", "rich texture"],

    # --------------------------------------------------------
    # HOME / FURNITURE FINISHES
    # --------------------------------------------------------
    "matte wood": ["matte wood", "matte finish wood"],
    "natural grain": ["natural grain", "wood grain"],
    "oiled wood": ["oiled wood", "oil finish"],
    "lacquered": ["lacquered", "lacquer finish"],
    "brushed metal": ["brushed metal", "brushed steel"],
    "polished metal": ["polished metal", "chrome finish"],
    "brass finish": ["brass finish", "gold-tone metal"],
    "powder-coated": ["powder coated", "powder-coated"],
    "honed stone": ["honed", "honed stone"],
    "polished stone": ["polished stone", "gloss stone"],

    # --------------------------------------------------------
    # ACCESSORY / PACKAGING FINISHES
    # --------------------------------------------------------
    "metallic": ["metallic", "metallic sheen"],
    "frosted": ["frosted", "frosted glass"],
    "clear": ["clear finish", "transparent"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Returns MULTIPLE finishes
# ------------------------------------------------------------
def detect_finishes(text: str) -> List[str]:
    """
    Detects all MVQueen finishes present in the product.

    Returns:
        List[str]
    """
    if not text:
        return []

    normalized = normalize_for_detection(text)
    found = []

    for finish, keywords in FINISH_KEYWORDS.items():
        if any(k in normalized for k in keywords):
            found.append(finish)

    return found


__all__ = ["detect_finishes"]