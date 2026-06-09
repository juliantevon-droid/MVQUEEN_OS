# mvqueen_engine/detection/detect_ingredients.py
"""
MVQueen Ingredient Detection — Enterprise Edition
-------------------------------------------------

Cross-category ingredient detection for:
- Skincare
- Beauty
- Hybrid skincare-makeup
- Body care
- Hair care

Ingredients are interpreted through MVQueen’s sensory,
feminine, benefit-forward, luxury-hybrid lens.
"""

from typing import List
from mvqueen_engine.utils.normalization import normalize_for_detection


# ------------------------------------------------------------
# INGREDIENT KEYWORD MAP — Expanded for Beauty + Skincare
# ------------------------------------------------------------
INGREDIENT_KEYWORDS = {
    # Hydrators
    "hyaluronic acid": ["hyaluronic", "ha", "hydrating acid"],
    "glycerin": ["glycerin", "glycerine"],
    "squalane": ["squalane"],
    "aloe": ["aloe", "aloe vera"],

    # Brightening
    "vitamin c": ["vitamin c", "ascorbic"],
    "niacinamide": ["niacinamide", "vitamin b3"],
    "licorice root": ["licorice", "glycyrrhiza"],

    # Anti-aging / smoothing
    "retinol": ["retinol", "vitamin a"],
    "bakuchiol": ["bakuchiol"],
    "peptides": ["peptide", "peptides"],
    "ceramides": ["ceramide", "ceramides"],

    # Acids / exfoliants
    "aha": ["aha", "alpha hydroxy"],
    "bha": ["bha", "beta hydroxy"],
    "salicylic acid": ["salicylic"],
    "glycolic acid": ["glycolic"],
    "lactic acid": ["lactic"],
    "mandelic acid": ["mandelic"],

    # Oils
    "rosehip oil": ["rosehip"],
    "jojoba oil": ["jojoba"],
    "argan oil": ["argan"],
    "marula oil": ["marula"],
    "coconut oil": ["coconut oil"],

    # Botanicals / extracts
    "green tea": ["green tea", "camellia"],
    "chamomile": ["chamomile"],
    "centella asiatica": ["centella", "cica", "asiatica"],
    "algae": ["algae", "seaweed", "kelp"],

    # Beauty pigments / finish ingredients
    "mica": ["mica"],
    "titanium dioxide": ["titanium dioxide"],
    "iron oxides": ["iron oxide", "iron oxides"],
    "silica": ["silica"],
    "dimethicone": ["dimethicone", "silicone"],

    # Hair care actives
    "biotin": ["biotin"],
    "keratin": ["keratin"],
    "amino acids": ["amino acid", "amino acids"],

    # Body care
    "shea butter": ["shea"],
    "cocoa butter": ["cocoa butter"],
}


# ------------------------------------------------------------
# DETECTION FUNCTION — Returns MULTIPLE ingredients
# ------------------------------------------------------------
def detect_ingredients(text: str) -> List[str]:
    """
    Detects all MVQueen skincare/beauty ingredients present.

    Returns:
        List[str]
    """
    if not text:
        return []

    normalized = normalize_for_detection(text)
    found = []

    for ingredient, keywords in INGREDIENT_KEYWORDS.items():
        if any(k in normalized for k in keywords):
            found.append(ingredient)

    return found


__all__ = ["detect_ingredients"]