# ---------------------------------------------------------
# MVQUEEN OMNILUXE — TITLE ENGINE
# ---------------------------------------------------------

from mvqueen_engine.utils.deterministic import (
    deterministic_seed,
    deterministic_choice
)

from mvqueen_engine.brand_brain.brand_banks import ADJECTIVES
from mvqueen_engine.brand_brain.detection import (
    detect_category,
    detect_persona,
    detect_material,
    detect_silhouette,
    detect_details,
)
from mvqueen_engine.brand_brain.seo_keywords import generate_primary_seo

TITLE_PATTERNS = [
    "{adj} {material} {category}",
    "{adj} {silhouette} with {detail}",
    "{adj} {category} — {seo}",
    "{adj} {material} {category} for {persona} style",
]

def generate_title(text: str) -> str:
    seed = deterministic_seed(text)

    adj = deterministic_choice(seed, LUXURY_ADJECTIVES, salt="title_adj")
    category = detect_category(text).title()
    persona = detect_persona(text).title()
    material = detect_material(text).title()
    silhouette = detect_silhouette(text).title()
    detail = detect_details(text).title()
    seo = generate_primary_seo(text).title()

    pattern = deterministic_choice(seed, TITLE_PATTERNS, salt="title_pattern")

    return pattern.format(
        adj=adj.title(),
        category=category,
        persona=persona,
        material=material,
        silhouette=silhouette,
        detail=detail,
        seo=seo,
    )