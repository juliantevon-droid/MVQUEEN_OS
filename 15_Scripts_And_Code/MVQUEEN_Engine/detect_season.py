# mvqueen_engine/detection/detect_season.py
"""
MVQueen Season Detection — Enterprise Edition
---------------------------------------------

Season detection identifies the seasonal alignment of a product using:

- MVQueen sensory language
- Material signals
- Silhouette cues
- Texture + finish language
- Emotional tone
- Trend alignment
- Fashion + beauty + skincare hybrid logic

This is NOT generic "summer/winter" logic.
This is MVQueen seasonal intelligence:
feminine, editorial, atmospheric, luxury-hybrid.
"""

from typing import Optional
from mvqueen_engine.utils import normalize_for_detection


# ------------------------------------------------------------
# SEASON KEYWORD MAP — Deep, Editorial, MVQueen-Aligned
# ------------------------------------------------------------
SEASON_KEYWORDS = {
    "spring": [
        "floral", "lightweight", "bloom", "soft pastel", "airy",
        "flowy", "romantic", "lace", "sheer", "breeze",
    ],
    "summer": [
        "breathable", "cooling", "light", "sun", "heat",
        "vacation", "resort", "linen", "tank", "mini",
    ],
    "fall": [
        "warm", "cozy", "autumn", "rich tone", "earthy",
        "knit", "sweater", "layering", "structured",
    ],
    "winter": [
        "cold", "insulated", "puffer", "coat", "thermal",
        "heavy knit", "wool", "holiday", "evening glam",
    ],
}


# ------------------------------------------------------------
# MATERIAL-BASED SEASONAL SIGNALS
# ------------------------------------------------------------
MATERIAL_SEASON_MAP = {
    "linen": "summer",
    "cotton": "spring",
    "silk": "spring",
    "satin": "summer",
    "velvet": "winter",
    "wool": "winter",
    "knit": "fall",
    "mesh": "summer",
    "leather": "fall",
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Cinematic, Feminine, Deterministic
# ------------------------------------------------------------
def detect_season(text: str) -> Optional[str]:
    """
    Determines the MVQueen seasonal alignment of a product.

    Returns:
        str or None
    """
    if not text:
        return None

    normalized = normalize_for_detection(text)

    # 1. Direct keyword match
    for season, keywords in SEASON_KEYWORDS.items():
        if any(k in normalized for k in keywords):
            return season

    # 2. Material-based inference
    for material, season in MATERIAL_SEASON_MAP.items():
        if material in normalized:
            return season

    return None


__all__ = ["detect_season"]