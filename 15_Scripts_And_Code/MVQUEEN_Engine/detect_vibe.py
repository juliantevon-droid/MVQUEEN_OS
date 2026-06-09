# mvqueen_engine/detection/detect_vibe.py
"""
MVQueen Vibe Detection — Enterprise Edition
-------------------------------------------

Cross-category emotional + aesthetic vibe detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories

Vibes are MVQueen editorial anchors:
- cinematic
- quiet luxury
- sensual
- modern
- cozy
- luminous
- romantic
"""

from typing import Optional
from mvqueen_engine.utils.normalization import normalize_for_detection
from mvqueen_engine.utils.helpers import first_match


# ------------------------------------------------------------
# VIBE KEYWORD MAP — Expanded for Fashion + Home + Beauty
# ------------------------------------------------------------
VIBE_KEYWORDS = {
    # Quiet Luxury / Minimal Interiors / Clean Lines
    "quiet luxury": [
        "minimal", "clean", "refined", "sleek", "neutral",
        "simple", "elevated", "polished", "architectural",
        "structured", "geometric", "modern lines",
    ],

    # Romantic / Feminine / Soft Apparel
    "romantic": [
        "romantic", "feminine", "soft", "flowy", "lace",
        "ruffle", "warm", "dreamy", "gentle",
    ],

    # Sensual / Velvet / Silky / Plush
    "sensual": [
        "sensual", "curve", "body-hugging", "silky", "velvet",
        "intimate", "soft edge", "seductive", "plush",
        "cashmere", "satin", "suede",
    ],

    # Editorial / High-Fashion / Dramatic
    "editorial": [
        "runway", "couture", "high-fashion", "dramatic",
        "cinematic", "bias cut", "statement", "avant-garde",
    ],

    # Modern / Sculptural / Interior Design
    "modern": [
        "modern", "structured", "sharp", "tailored",
        "geometric", "minimalist", "architectural",
        "sculptural", "clean lines",
    ],

    # Luminous / Glow / Radiant
    "luminous": [
        "glow", "luminous", "radiant", "soft-focus",
        "sheer", "light-catching", "glossy",
    ],

    # Cozy / Plush / Home Comfort
    "cozy": [
        "cozy", "soft knit", "warm", "loungewear",
        "sweater", "cushiony", "comfortable",
        "deep seating", "plush seating", "soft touch",
    ],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Cross-Category, Deterministic
# ------------------------------------------------------------
def detect_vibe(text: str) -> Optional[str]:
    if not text:
        return None

    normalized = normalize_for_detection(text)
    vibe = first_match(normalized, VIBE_KEYWORDS)

    return vibe


__all__ = ["detect_vibe"]