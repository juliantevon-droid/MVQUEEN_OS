# mvqueen_engine/detection/detect_silhouette.py
"""
MVQueen Silhouette Detection — Enterprise Edition
-------------------------------------------------

Cross-category silhouette detection for:
- Fashion
- Home / Furniture
- Beauty (shape-based packaging)
- Accessories

Silhouettes influence:
- Editorial descriptions
- Persona routing
- SEO
- Metafields
- Tag generation
"""

from typing import Optional
from mvqueen_engine.utils.normalization import normalize_for_detection
from mvqueen_engine.utils.helpers import first_match


# ------------------------------------------------------------
# SILHOUETTE KEYWORD MAP — Fashion + Home + Beauty
# ------------------------------------------------------------
SILHOUETTE_KEYWORDS = {
    # -------------------------
    # FASHION SILHOUETTES
    # -------------------------
    "bodycon": [
        "bodycon", "curve-hugging", "fitted", "tight", "sculpted",
        "second-skin", "contoured",
    ],
    "a-line": [
        "a-line", "a line", "flared skirt", "fit and flare",
    ],
    "relaxed": [
        "relaxed", "loose", "easy fit", "soft drape", "flowy",
    ],
    "oversized": [
        "oversized", "boxy", "slouchy", "roomy",
    ],
    "tailored": [
        "tailored", "structured", "sharp lines", "precise fit",
    ],
    "cropped": [
        "cropped", "short length", "midriff",
    ],
    "flowy": [
        "flowy", "fluid", "drifts", "movement", "soft motion",
    ],
    "structured": [
        "structured", "architectural", "clean lines",
    ],

    # -------------------------
    # HOME / FURNITURE SILHOUETTES
    # -------------------------
    "sectional": [
        "sectional", "modular sectional", "l-shaped sectional",
        "u-shaped sectional", "modular seating",
    ],
    "sofa": [
        "sofa", "couch", "loveseat",
    ],
    "armchair": [
        "armchair", "chair", "accent chair", "lounge chair",
    ],
    "curved": [
        "curved", "rounded", "sculptural", "soft form",
    ],
    "low-profile": [
        "low profile", "low-profile", "low slung", "grounded silhouette",
    ],
    "deep-seated": [
        "deep seating", "deep-seated", "plush seating",
    ],
    "bench": [
        "bench", "entry bench", "bed bench",
    ],
    "table": [
        "table", "coffee table", "side table", "dining table",
    ],
    "bed": [
        "bed", "platform bed", "frame", "headboard",
    ],
    "rug": [
        "rug", "area rug", "woven rug",
    ],

    # -------------------------
    # BEAUTY / PACKAGING SHAPES
    # -------------------------
    "tube": ["tube", "squeeze tube"],
    "pump": ["pump bottle", "airless pump"],
    "jar": ["jar", "cream jar"],
    "stick": ["stick", "balm stick"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Cross-Category, Deterministic
# ------------------------------------------------------------
def detect_silhouette(text: str) -> Optional[str]:
    if not text:
        return None

    normalized = normalize_for_detection(text)
    silhouette = first_match(normalized, SILHOUETTE_KEYWORDS)

    return silhouette


__all__ = ["detect_silhouette"]