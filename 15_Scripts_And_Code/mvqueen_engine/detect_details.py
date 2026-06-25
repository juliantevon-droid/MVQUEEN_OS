# mvqueen_engine/detection/detect_details.py
"""
MVQueen Detail Detection — Enterprise Edition
---------------------------------------------

Cross-category detail detection for:
- Fashion
- Beauty
- Skincare
- Home / Furniture
- Accessories

Details shape:
- Editorial descriptions
- SEO
- Persona routing
- Trend + vibe alignment
- Metafields
- Tag generation
"""

from typing import List
from mvqueen_engine.utils.normalization import normalize_for_detection


# ------------------------------------------------------------
# DETAIL KEYWORD MAP — Expanded for All MVQueen Domains
# ------------------------------------------------------------
DETAIL_KEYWORDS = {
    # --------------------------------------------------------
    # FASHION DETAILS
    # --------------------------------------------------------
    "lace": ["lace", "lace trim", "delicate lace"],
    "ruffle": ["ruffle", "ruffled", "frill"],
    "cutout": ["cutout", "cut-out", "open back", "open side"],
    "slit": ["slit", "side slit", "front slit"],
    "pleated": ["pleated", "pleat"],
    "ribbed": ["ribbed", "rib knit"],
    "mesh": ["mesh", "sheer mesh"],
    "sheer": ["sheer", "semi-sheer", "see-through"],
    "draped": ["draped", "drape", "soft drape"],
    "ruched": ["ruched", "ruching"],
    "wrap": ["wrap", "wrap front", "wrap style"],
    "bow": ["bow", "tie detail"],
    "buttons": ["button", "button-down", "button front"],
    "pockets": ["pocket", "pockets"],

    # --------------------------------------------------------
    # HOME / FURNITURE DETAILS
    # --------------------------------------------------------
    "tufted": ["tufted", "button tufting"],
    "channel-stitched": ["channel stitch", "channel-stitched", "channel tufting"],
    "piping": ["piping", "contrast piping"],
    "contrast trim": ["contrast trim", "contrast edge"],
    "sculptural": ["sculptural", "curved form", "rounded form"],
    "deep seating": ["deep seating", "deep-seated"],
    "modular": ["modular", "modular design"],
    "low profile": ["low profile", "low-profile"],
    "wood base": ["wood base", "wood frame"],
    "metal legs": ["metal legs", "steel legs", "brass legs"],
    "upholstered": ["upholstered", "fully upholstered"],

    # --------------------------------------------------------
    # BEAUTY / SKINCARE DETAILS
    # --------------------------------------------------------
    "glossy finish": ["glossy", "high-shine", "glass-like"],
    "matte finish": ["matte", "soft-matte"],
    "dewy finish": ["dewy", "fresh glow"],
    "radiant finish": ["radiant", "luminous finish"],
    "whipped texture": ["whipped", "mousse-like"],
    "gel texture": ["gel texture", "cooling gel"],

    # --------------------------------------------------------
    # ACCESSORY DETAILS
    # --------------------------------------------------------
    "gold hardware": ["gold hardware", "gold-tone"],
    "silver hardware": ["silver hardware", "silver-tone"],
    "chain strap": ["chain strap", "chain detail"],
    "quilted": ["quilted", "quilt stitching"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Returns MULTIPLE details
# ------------------------------------------------------------
def detect_details(text: str) -> List[str]:
    """
    Detects all MVQueen details present in the product.

    Returns:
        List[str]
    """
    if not text:
        return []

    normalized = normalize_for_detection(text)
    found = []

    for detail, keywords in DETAIL_KEYWORDS.items():
        if any(k in normalized for k in keywords):
            found.append(detail)

    return found


__all__ = ["detect_details"]