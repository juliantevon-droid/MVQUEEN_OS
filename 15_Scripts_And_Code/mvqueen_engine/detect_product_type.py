# mvqueen_engine/detection/detect_product_type.py
"""
MVQueen Product Type Detection — Enterprise Edition
---------------------------------------------------

Cross-category product type detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories
- Haircare
- Bodycare
- Home fragrance

Product type is more granular than category and drives:
- Editorial tone
- SEO
- Metafields
- Collections
- Tags
- Persona routing
"""

from typing import Optional
from mvqueen_engine.utils.normalization import normalize_for_detection
from mvqueen_engine.utils.helpers import first_match


# ------------------------------------------------------------
# PRODUCT TYPE KEYWORD MAP — Expanded for All MVQueen Domains
# ------------------------------------------------------------
PRODUCT_TYPE_KEYWORDS = {
    # --------------------------------------------------------
    # FASHION — Dresses
    # --------------------------------------------------------
    "slip dress": ["slip dress", "bias cut", "satin slip", "silk slip"],
    "bodycon dress": ["bodycon", "curve-hugging dress", "fitted dress"],
    "maxi dress": ["maxi dress", "floor length dress"],
    "midi dress": ["midi dress", "mid length dress"],
    "mini dress": ["mini dress", "short dress"],

    # --------------------------------------------------------
    # FASHION — Tops
    # --------------------------------------------------------
    "corset top": ["corset", "bustier", "structured top"],
    "crop top": ["crop top", "cropped top"],
    "tank top": ["tank", "camisole", "cami"],
    "blouse": ["blouse", "button down", "button-up", "silk blouse"],

    # --------------------------------------------------------
    # FASHION — Bodysuits
    # --------------------------------------------------------
    "bodysuit": ["bodysuit", "body suit", "one-piece top"],

    # --------------------------------------------------------
    # FASHION — Skirts
    # --------------------------------------------------------
    "mini skirt": ["mini skirt", "short skirt"],
    "midi skirt": ["midi skirt", "mid length skirt"],
    "maxi skirt": ["maxi skirt", "long skirt"],

    # --------------------------------------------------------
    # FASHION — Pants
    # --------------------------------------------------------
    "wide-leg pants": ["wide leg", "wide-leg", "flowy pants"],
    "flare pants": ["flare pants", "flared pants"],
    "straight pants": ["straight leg pants", "straight pants"],

    # --------------------------------------------------------
    # FASHION — Denim
    # --------------------------------------------------------
    "denim jeans": ["jeans", "denim", "denim pants"],
    "denim jacket": ["denim jacket", "jean jacket"],

    # --------------------------------------------------------
    # FASHION — Outerwear
    # --------------------------------------------------------
    "blazer": ["blazer", "structured jacket"],
    "coat": ["coat", "trench", "overcoat"],
    "puffer": ["puffer", "puffer jacket"],

    # --------------------------------------------------------
    # FASHION — Intimates
    # --------------------------------------------------------
    "lingerie set": ["lingerie set", "bra and panty set"],
    "bralette": ["bralette", "soft bra"],
    "panty": ["panty", "thong", "brief"],

    # --------------------------------------------------------
    # FASHION — Activewear
    # --------------------------------------------------------
    "leggings": ["leggings", "active leggings"],
    "sports bra": ["sports bra", "workout bra"],

    # --------------------------------------------------------
    # FASHION — Loungewear
    # --------------------------------------------------------
    "loungewear set": ["loungewear set", "cozy set", "sweat set"],
    "hoodie": ["hoodie", "sweatshirt"],
    "joggers": ["joggers", "sweatpants"],

    # --------------------------------------------------------
    # FASHION — One-piece
    # --------------------------------------------------------
    "jumpsuit": ["jumpsuit", "one-piece outfit"],
    "romper": ["romper", "playsuit"],
    "two-piece set": ["set", "two-piece", "matching set"],

    # --------------------------------------------------------
    # ACCESSORIES
    # --------------------------------------------------------
    "bag": ["bag", "handbag", "shoulder bag"],
    "accessory": ["accessory", "belt", "scarf", "hat"],

    # --------------------------------------------------------
    # BEAUTY
    # --------------------------------------------------------
    "lipstick": ["lipstick", "lip color", "lip cream"],
    "foundation": ["foundation", "base makeup"],
    "concealer": ["concealer", "corrector"],
    "blush": ["blush", "cheek color"],
    "bronzer": ["bronzer", "contour powder"],
    "highlighter": ["highlighter", "glow powder"],
    "eyeshadow": ["eyeshadow", "shadow palette"],
    "mascara": ["mascara", "lash product"],

    # --------------------------------------------------------
    # SKINCARE
    # --------------------------------------------------------
    "serum": ["serum", "treatment serum"],
    "moisturizer": ["moisturizer", "cream", "hydrator"],
    "cleanser": ["cleanser", "face wash"],
    "toner": ["toner", "essence"],
    "mask": ["mask", "face mask"],

    # --------------------------------------------------------
    # HAIRCARE
    # --------------------------------------------------------
    "shampoo": ["shampoo"],
    "conditioner": ["conditioner"],
    "hair mask": ["hair mask", "deep conditioning"],
    "hair oil": ["hair oil", "hair serum"],

    # --------------------------------------------------------
    # BODYCARE
    # --------------------------------------------------------
    "body lotion": ["body lotion", "body cream"],
    "body wash": ["body wash", "shower gel"],
    "body scrub": ["body scrub", "exfoliating scrub"],

    # --------------------------------------------------------
    # HOME / FURNITURE
    # --------------------------------------------------------
    "sofa": ["sofa", "couch", "loveseat"],
    "sectional": ["sectional", "modular sectional", "l-shaped sectional"],
    "armchair": ["armchair", "chair", "accent chair"],
    "bench": ["bench", "entry bench"],
    "coffee table": ["coffee table"],
    "side table": ["side table", "end table"],
    "dining table": ["dining table"],
    "bed": ["bed", "platform bed", "headboard"],
    "dresser": ["dresser"],
    "nightstand": ["nightstand"],
    "rug": ["rug", "area rug"],
    "lamp": ["lamp", "table lamp", "floor lamp"],

    # --------------------------------------------------------
    # HOME FRAGRANCE
    # --------------------------------------------------------
    "candle": ["candle", "scented candle"],
    "diffuser": ["diffuser", "reed diffuser"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Cross-Category, Deterministic
# ------------------------------------------------------------
def detect_product_type(text: str) -> Optional[str]:
    if not text:
        return None

    normalized = normalize_for_detection(text)
    product_type = first_match(normalized, PRODUCT_TYPE_KEYWORDS)

    return product_type


__all__ = ["detect_product_type"]