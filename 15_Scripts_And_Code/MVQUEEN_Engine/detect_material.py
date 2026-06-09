# mvqueen_engine/detection/detect_material.py
"""
MVQueen Material Detection — Enterprise Edition
-----------------------------------------------

Cross-category material detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories

Materials are interpreted through MVQueen’s feminine,
sensory, atmospheric, luxury-hybrid lens.
"""

from typing import Optional
from mvqueen_engine.utils.normalization import normalize_for_detection
from mvqueen_engine.utils.helpers import first_match


# ------------------------------------------------------------
# MATERIAL KEYWORD MAP — Expanded for Fashion + Home + Beauty
# ------------------------------------------------------------
MATERIAL_KEYWORDS = {
    # Fashion fabrics
    "satin": ["satin", "satin finish", "soft sheen", "liquid shine"],
    "silk": ["silk", "silky", "silk-like", "smooth-touch"],
    "cotton": ["cotton", "soft cotton", "breathable cotton"],
    "linen": ["linen", "light linen", "air linen"],
    "denim": ["denim", "jean", "washed denim"],
    "leather": ["leather", "faux leather", "vegan leather"],
    "mesh": ["mesh", "sheer mesh", "soft mesh"],
    "jersey": ["jersey", "stretch jersey", "soft jersey"],
    "knit": ["knit", "rib knit", "soft knit", "sweater knit"],
    "wool": ["wool", "wool blend", "soft wool"],
    "velvet": ["velvet", "velvety", "plush velvet", "plush"],

    # Home / Furniture upholstery
    "boucle": ["boucle", "nubby texture", "looped yarn"],
    "performance fabric": ["performance fabric", "stain-resistant", "durable weave"],
    "microfiber": ["microfiber", "micro-suede"],
    "chenille": ["chenille", "soft chenille"],

    # Home / Furniture hard materials
    "wood": ["wood", "oak", "walnut", "pine", "hardwood"],
    "marble": ["marble", "stone top"],
    "metal": ["metal", "steel", "iron"],
    "brass": ["brass", "gold-tone metal"],
    "chrome": ["chrome", "polished metal"],
    "glass": ["glass", "tempered glass"],

    # Beauty / Skincare textures
    "gel": ["gel", "gel-cream", "cooling gel"],
    "cream": ["cream", "rich cream", "moisturizing cream"],
    "balm": ["balm", "solid balm"],
    "oil": ["oil", "face oil", "body oil"],
    "serum": ["serum", "treatment serum"],
    "mousse": ["mousse", "whipped texture"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Cross-Category, Deterministic
# ------------------------------------------------------------
def detect_material(text: str) -> Optional[str]:
    if not text:
        return None

    normalized = normalize_for_detection(text)
    material = first_match(normalized, MATERIAL_KEYWORDS)

    return material


__all__ = ["detect_material"]