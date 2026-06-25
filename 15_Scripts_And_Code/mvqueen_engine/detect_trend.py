# mvqueen_engine/detection/detect_trend.py
"""
MVQueen Trend Detection — Enterprise Edition
--------------------------------------------

Cross-category trend intelligence for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories

Trends are interpreted through the MVQueen lens:
feminine, modern, editorial, sensory, cinematic, and luxury-hybrid.
"""

from typing import Optional
from mvqueen_engine.utils.normalization import normalize_for_detection
from mvqueen_engine.utils.helpers import first_match


# ------------------------------------------------------------
# TREND KEYWORD MAP — Expanded for Fashion + Home + Beauty
# ------------------------------------------------------------
TREND_KEYWORDS = {
    # Fashion + Interiors
    "quiet luxury": [
        "minimal", "clean", "refined", "neutral", "elevated",
        "soft structure", "simple", "polished", "understated",
        "modern lines", "architectural", "sleek",
    ],

    # Fashion
    "romantic revival": [
        "lace", "ruffle", "floral", "soft", "flowy",
        "romantic", "feminine", "dreamy",
    ],

    # Fashion
    "90s minimalism": [
        "slip dress", "bias cut", "satin", "silk",
        "straight neck", "spaghetti strap", "minimalist",
    ],

    # Beauty + Skincare
    "soft glam": [
        "glow", "luminous", "radiant", "soft-focus",
        "sheer", "glossy", "highlight", "shimmer",
    ],

    # Fashion + Athleisure
    "athleisure": [
        "leggings", "sports bra", "active", "performance",
        "stretch", "workout", "athletic",
    ],

    # Fashion + Home
    "cozy core": [
        "cozy", "knit", "sweater", "cushiony", "soft-touch",
        "loungewear", "warm", "plush", "deep seating",
    ],

    # Fashion + Interiors
    "statement structure": [
        "tailored", "structured", "sharp", "sculpted",
        "geometric", "architectural", "clean lines",
    ],

    # Home / Furniture
    "modern minimalism": [
        "modern", "sleek", "sculptural", "minimalist",
        "clean lines", "contemporary", "refined",
    ],

    # Home / Furniture
    "organic modern": [
        "curved", "rounded", "organic", "soft form",
        "natural texture", "earthy", "warm neutral",
    ],

    # Home / Furniture
    "plush comfort": [
        "plush", "velvet", "deep seating", "soft-touch",
        "cushioned", "comfort", "relaxed",
    ],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Cross-Category, Deterministic
# ------------------------------------------------------------
def detect_trend(text: str) -> Optional[str]:
    if not text:
        return None

    normalized = normalize_for_detection(text)
    trend = first_match(normalized, TREND_KEYWORDS)

    return trend


__all__ = ["detect_trend"]