# ---------------------------------------------------------
# MVQUEEN OMNILUXE — FULLY DETERMINISTIC TAG ENGINE
# ---------------------------------------------------------

from mvqueen_engine.utils.deterministic import (
    deterministic_seed,
    deterministic_shuffle
)

def generate_tags(
    text: str,
    category: str,
    product_types: str,
    persona: str,
    trend: str,
    season: str,
    vibe: str,
    material: str,
    silhouette: str,
    details: str,
) -> list:

    # -----------------------------------------
    # 1. Collect raw tags
    # -----------------------------------------
    raw_tags = [
        category,
        product_types,
        persona,
        trend,
        season,
        vibe,
        material,
        silhouette,
        details,
    ]

    # -----------------------------------------
    # 2. Normalize (remove empty + format)
    # -----------------------------------------
    clean = []
    for t in raw_tags:
        if not t:
            continue
        clean.append(t.replace("_", " ").title())

    # -----------------------------------------
    # 3. Deterministic ordering
    # -----------------------------------------
    seed = deterministic_seed(text)
    ordered = deterministic_shuffle(seed, clean, salt="tags")

    return ordered