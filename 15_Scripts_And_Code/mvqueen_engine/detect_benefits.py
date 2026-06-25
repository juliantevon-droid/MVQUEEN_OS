# mvqueen_engine/detection/detect_benefits.py
"""
MVQueen Benefit Detection — Enterprise Edition
----------------------------------------------

Cross-category benefit detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Bodycare
- Haircare

Benefits are interpreted through MVQueen’s feminine,
sensory, emotional, luxury-hybrid lens.
"""

from typing import List
from mvqueen_engine.utils.normalization import normalize_for_detection


# ------------------------------------------------------------
# BENEFIT KEYWORD MAP — Expanded for All MVQueen Domains
# ------------------------------------------------------------
BENEFIT_KEYWORDS = {
    # --------------------------------------------------------
    # BEAUTY + SKINCARE BENEFITS
    # --------------------------------------------------------
    "softening": ["softens", "soft-touch", "soft feel", "gentle", "smooth"],
    "smoothing": ["smooths", "refines texture", "even texture", "polished"],
    "brightening": ["brightening", "radiant", "glow", "luminous", "light-catching"],
    "hydrating": ["hydrating", "moisturizing", "dewy", "plumping", "supple"],
    "firming": ["firming", "tightening", "elasticity"],
    "clarifying": ["clarifying", "purifying", "refining"],
    "soothing": ["soothing", "calming", "redness reducing"],
    "anti-aging": ["anti-aging", "youthful", "fine lines", "wrinkles"],
    "exfoliating": ["exfoliating", "resurfacing", "renewing"],

    # --------------------------------------------------------
    # HAIRCARE BENEFITS
    # --------------------------------------------------------
    "strengthening": ["strengthening", "fortifying", "repairing"],
    "shine-enhancing": ["shine", "glossy", "radiant finish"],
    "frizz-control": ["frizz", "smooth control", "taming"],

    # --------------------------------------------------------
    # BODYCARE BENEFITS
    # --------------------------------------------------------
    "nourishing": ["nourishing", "rich moisture", "conditioning"],
    "softening skin": ["soft skin", "silky skin", "smooth skin"],

    # --------------------------------------------------------
    # FASHION BENEFITS
    # --------------------------------------------------------
    "sculpting": ["sculpts", "defines", "contours", "curve-hugging"],
    "comfort": ["comfortable", "breathable", "lightweight", "easy wear"],
    "movement": ["flows", "drifts", "moves with you", "fluid", "soft motion"],
    "confidence": ["confidence", "empowering", "feminine strength"],

    # --------------------------------------------------------
    # HOME / FURNITURE BENEFITS
    # --------------------------------------------------------
    "plush comfort": ["plush", "deep seating", "cushiony", "soft-touch"],
    "supportive": ["supportive", "ergonomic", "structured comfort"],
    "relaxing": ["relaxing", "soothing", "calming presence"],
    "durable": ["durable", "long-lasting", "stain-resistant", "performance fabric"],
    "inviting": ["inviting", "warm", "welcoming", "cozy"],
    "modern appeal": ["modern", "sleek", "clean lines", "contemporary"],
    "elevated presence": ["elevated", "refined", "quiet luxury"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Returns MULTIPLE benefits
# ------------------------------------------------------------
def detect_benefits(text: str) -> List[str]:
    """
    Detects all MVQueen benefits present in the product.

    Returns:
        List[str]
    """
    if not text:
        return []

    normalized = normalize_for_detection(text)
    found = []

    for benefit, keywords in BENEFIT_KEYWORDS.items():
        if any(k in normalized for k in keywords):
            found.append(benefit)

    return found


__all__ = ["detect_benefits"]