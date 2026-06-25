# mvqueen_engine/detection/detect_textures.py
"""
MVQueen Texture Detection — Enterprise Edition
----------------------------------------------

Cross-category texture detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories

Textures shape:
- Editorial descriptions
- SEO
- Persona routing
- Metafields
- Tag generation
"""

from typing import List
from mvqueen_engine.utils.normalization import normalize_for_detection


# ------------------------------------------------------------
# TEXTURE KEYWORD MAP — Expanded for All MVQueen Domains
# ------------------------------------------------------------
TEXTURE_KEYWORDS = {
    # --------------------------------------------------------
    # FASHION + BEAUTY TEXTURES
    # --------------------------------------------------------
    "silky": ["silky", "silk-like", "smooth-touch", "liquid-soft"],
    "buttery": ["buttery", "butter-soft", "butter smooth"],
    "velvety": ["velvety", "velvet-soft", "plush"],
    "cloud-soft": ["cloud-soft", "cloudlike", "pillowy", "cushiony"],
    "weightless": ["weightless", "light-as-air", "barely-there"],
    "ribbed": ["ribbed", "rib knit", "textured rib"],
    "smooth": ["smooth", "sleek", "polished"],
    "soft-structured": ["soft structure", "soft-structured", "gentle structure"],

    # --------------------------------------------------------
    # HOME / FURNITURE TEXTURES
    # --------------------------------------------------------
    "boucle": ["boucle", "nubby", "looped yarn"],
    "woven": ["woven", "basket weave", "textured weave"],
    "chenille": ["chenille", "soft chenille"],
    "performance weave": ["performance fabric", "durable weave"],
    "brushed": ["brushed", "brushed texture"],
    "matte": ["matte", "matte finish"],
    "polished": ["polished", "polished metal", "polished stone"],
    "grain": ["wood grain", "natural grain"],
    "low-pile": ["low pile", "low-pile"],
    "high-pile": ["high pile", "high-pile", "shaggy"],

    # --------------------------------------------------------
    # SKINCARE + BEAUTY TEXTURES
    # --------------------------------------------------------
    "gel": ["gel", "gel texture", "cooling gel"],
    "cream": ["cream texture", "rich cream"],
    "balm": ["balm", "balmy"],
    "whipped": ["whipped", "mousse-like"],
    "serum-like": ["serum-like", "fluid texture"],
    "oil": ["oil texture", "silky oil"],

    # --------------------------------------------------------
    # ACCESSORY / HARD MATERIAL TEXTURES
    # --------------------------------------------------------
    "metallic": ["metallic", "brushed metal", "polished metal"],
    "glossy": ["glossy", "high-shine"],
    "matte-metal": ["matte metal", "brushed steel"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Returns MULTIPLE textures
# ------------------------------------------------------------
def detect_textures(text: str) -> List[str]:
    """
    Detects all MVQueen textures present in the product.

    Returns:
        List[str]
    """
    if not text:
        return []

    normalized = normalize_for_detection(text)
    found = []

    for texture, keywords in TEXTURE_KEYWORDS.items():
        if any(k in normalized for k in keywords):
            found.append(texture)

    return found


__all__ = ["detect_textures"]