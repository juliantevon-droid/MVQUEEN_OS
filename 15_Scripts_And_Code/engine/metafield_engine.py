# mvqueen_engine/metafields/metafield_engine.py
"""
PHASE 2 — METAFIELDS ENGINE

Generates FULL curated metafields for every product:
- Persona flavor
- Sensory language
- Fashion vocabulary
- Fit / Style / Material / Occasion
- Emotional micro-phrases
- Luxury finishers
- Keyword stack (focus, secondary, tertiary)
- Highlights + benefits
- Texture / scent / finish
- Routine step
- Who it's for
- Results
- Certifications / trust badges
- FAQ
- Brand story
- Care instructions
- Return policy
- Default metafields

Always overwrites all metafields (Mode A).
"""

from mvqueen_engine.brand_brain.brand_language import (
    select_persona_from_handle,
    get_persona_profile,
    select_sensory_word,
    select_fashion_term,
    select_occasion,
    select_fit,
    select_material,
    select_style,
    select_emotional_phrase,
    select_luxury_finisher,
)

from mvqueen_engine.brand_brain.seo_keywords import get_keyword_stack
from mvqueen_engine.brand_brain.brand_banks import (
    TRUST_BADGES_BY_CATEGORY,
    DEFAULT_METAFIELDS,
)

from mvqueen_engine.utils.deterministic import seed_from_text, pick_multiple, pick_from_pool


def generate_metafields(base_title: str, handle: str, product_type: str = "General") -> dict:
    """
    FULL ENTERPRISE METAFIELD ENGINE
    Always overwrites all metafields (Mode A).
    """

    persona = select_persona_from_handle(handle)
    profile = get_persona_profile(persona)
    seeds = seed_from_text(handle + "_metafields")

    # -----------------------------
    # KEYWORD STACK
    # -----------------------------
    kw = get_keyword_stack(handle)
    focus_kw = kw["focus"]
    secondary_kw = kw["secondary"]
    tertiary_kw = kw["tertiary"]

    # -----------------------------
    # SENSORY / FASHION / FIT / STYLE / MATERIAL / OCCASION
    # -----------------------------
    sensory = select_sensory_word(handle)
    fashion_term = select_fashion_term(handle)
    occasion = select_occasion(handle)
    fit = select_fit(handle)
    material = select_material(handle)
    style = select_style(handle)

    # -----------------------------
    # EMOTIONAL + LUXURY FINISHER
    # -----------------------------
    emotion = select_emotional_phrase(handle)
    finisher = select_luxury_finisher(handle)

    # -----------------------------
    # BENEFITS / HIGHLIGHTS
    # -----------------------------
    bullet_pool = profile.get("bullets", [])
    benefits = pick_multiple(bullet_pool, seeds[3:], count=4)
    highlights = "; ".join(benefits)

    # -----------------------------
    # TRUST BADGES
    # -----------------------------
    trust = TRUST_BADGES_BY_CATEGORY.get(product_type, "Cruelty-Free")

    # -----------------------------
    # BUILD METAFIELD PAYLOAD
    # -----------------------------
    metafields = {
        # CORE DESCRIPTIONS
        "custom.short_description": (
            f"{persona} interpretation of {base_title}. {emotion}."
        ),

        "custom.long_description": (
            f"{persona} crafted luxury designed for modern confidence. "
            f"Featuring a {sensory} feel, {fashion_term}-focused {fit.lower()} silhouette, "
            f"and {material.lower()} construction — {finisher}."
        ),

        # BENEFITS
        "custom.key_benefits": "; ".join(benefits),
        "custom.highlights": highlights,

        # SENSORY
        "custom.texture": sensory,
        "custom.scent": sensory,
        "custom.finish": fashion_term,

        # RESULTS
        "custom.results": (
            "Visible enhancement in presence, silhouette, and confidence."
        ),

        # WHO IT'S FOR
        "custom.who_its_for": (
            "Women seeking elevated style, luxury, and confidence."
        ),

        # ROUTINE / USAGE
        "custom.how_to_use": "Wear with intention. Pair with confidence.",
        "custom.when_to_use": occasion,
        "custom.routine_step": f"Step {seeds[1] % 5 + 1}",

        # PRODUCT ATTRIBUTES
        "custom.fit": fit,
        "custom.material": material,
        "custom.style": style,
        "custom.occasion": occasion,

        # SIZE / ORIGIN / SHELF LIFE
        "custom.size": "Standard",
        "custom.origin": "MVQueen Studio",
        "custom.shelf_life": "24 months",

        # CERTIFICATIONS / BADGES
        "custom.certifications": trust,
        "custom.badge": "Best Seller",

        # FAQ
        "custom.faq": (
            f"Q: Who is this designed for? A: Women seeking {persona.lower()} luxury. "
            f"Q: What makes it special? A: {sensory} feel and {fashion_term} finish."
        ),

        # SEO
        "seo.focus_keyword": focus_kw,
        "seo.secondary_keywords": f"{secondary_kw}, {tertiary_kw}",

        # TRUST
        "trust_badges": trust,
    }

    # Add default metafields (brand story, care, returns)
    metafields.update(DEFAULT_METAFIELDS or {})

    return metafields