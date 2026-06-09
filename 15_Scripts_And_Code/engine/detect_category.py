# mvqueen_engine/detection/detect_category.py
"""
MVQueen Category Detection — Enterprise Edition
----------------------------------------------

Deterministic, editorial-aware category detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories
- Bags
- Shoes
- Jewelry
"""

from typing import Optional
from mvqueen_engine.utils.normalization import normalize_for_detection


# ------------------------------------------------------------
# CATEGORY BANKS — MVQueen-Aligned
# ------------------------------------------------------------
HOME = [
    "sofa", "sectional", "couch", "chair", "armchair", "table",
    "coffee table", "side table", "lamp", "rug", "bed", "frame",
    "dresser", "nightstand", "stool", "bench",
]

BEAUTY = [
    "lipstick", "foundation", "concealer", "blush", "bronzer",
    "highlighter", "eyeshadow", "mascara", "liner", "makeup",
]

SKINCARE = [
    "serum", "moisturizer", "cleanser", "toner", "essence",
    "mask", "cream", "gel cream", "hydrator", "treatment",
]

ACCESSORIES = [
    "bag", "belt", "scarf", "hat", "earrings", "necklace",
    "bracelet", "accessory", "sunglasses",
]

SHOES = [
    "heel", "boot", "sneaker", "flat", "pump", "loafer",
]

BAGS = [
    "bag", "tote", "crossbody", "clutch", "shoulder bag",
]

JEWELRY = [
    "ring", "necklace", "bracelet", "earring", "jewelry",
]

FASHION = {
    "dress": ["dress", "gown", "slip", "maxi", "midi", "mini"],
    "top": ["top", "blouse", "tee", "corset", "tank", "camisole"],
    "bodysuit": ["bodysuit", "one-piece top"],
    "skirt": ["skirt"],
    "pants": ["pants", "trousers", "slacks"],
    "denim": ["jeans", "denim"],
    "outerwear": ["coat", "jacket", "blazer"],
    "lingerie": ["lingerie", "bra", "panty", "bralette"],
    "activewear": ["leggings", "sports bra"],
    "loungewear": ["sweatpants", "hoodie", "joggers"],
    "jumpsuit": ["jumpsuit"],
    "romper": ["romper"],
    "set": ["set", "two-piece"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION
# ------------------------------------------------------------
def detect_category(text: str) -> Optional[str]:
    if not text:
        return None

    t = normalize_for_detection(text)

    # HOME / FURNITURE
    if any(w in t for w in HOME):
        return "home"

    # BEAUTY
    if any(w in t for w in BEAUTY):
        return "beauty"

    # SKINCARE
    if any(w in t for w in SKINCARE):
        return "skincare"

    # SHOES
    if any(w in t for w in SHOES):
        return "shoes"

    # BAGS
    if any(w in t for w in BAGS):
        return "bags"

    # JEWELRY
    if any(w in t for w in JEWELRY):
        return "jewelry"

    # ACCESSORIES
    if any(w in t for w in ACCESSORIES):
        return "accessory"

    # FASHION (structured)
    for cat, words in FASHION.items():
        if any(w in t for w in words):
            return cat

    return None


__all__ = ["detect_category"]