# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — OMNILUXE PROCESSOR (BLOCK H)
# Unified BRAND_BRAIN core
# ---------------------------------------------------------

from mvqueen_engine.utils.deterministic import deterministic_seed

# BRAND_BRAIN: detection (hybrid keyword + deterministic)
from mvqueen_engine.brand_brain.detection import (
    detect_category,
    detect_product_types,
    detect_trend,
    detect_season,
    detect_vibe,
    detect_material,
    detect_silhouette,
    detect_details,
    detect_persona,
)

# BRAND_BRAIN: editorial
from mvqueen_engine.brand_brain.brand_language import (
    generate_short_editorial,
    generate_medium_editorial,
    generate_long_editorial,
)

# BRAND_BRAIN: alt text
from mvqueen_engine.brand_brain.alt_text import (
    generate_alt_text_short,
    generate_alt_text_medium,
    generate_alt_text_long,
)

# BRAND_BRAIN: SEO core
from mvqueen_engine.brand_brain.seo_keywords import (
    generate_primary_seo,
    generate_secondary_seo,
)

# BRAND_BRAIN: tags + collections
from mvqueen_engine.brand_brain.tags import generate_tags
from mvqueen_engine.brand_brain.collections import generate_collections

# BRAND_BRAIN: title, handle, variants, price
from mvqueen_engine.brand_brain.title_engine import generate_title
from mvqueen_engine.brand_brain.handle_engine import generate_handle
from mvqueen_engine.brand_brain.variant_engine import generate_variants
from mvqueen_engine.brand_brain.pricing_engine import generate_price

# METAFIELDS
from mvqueen_engine.metafields.metafield_engine import generate_all_metafields


# ---------------------------------------------------------
# MASTER OMNILUXE PRODUCT PROCESSOR
# ---------------------------------------------------------

def process_product(text: str) -> dict:
    """
    Omniluxe core processor.
    Uses BRAND_BRAIN engines to build a deterministic product dictionary.
    """

    seed = deterministic_seed(text)

    # -----------------------------------------
    # DETECTION LAYER
    # -----------------------------------------
    category = detect_category(text)
    product_type = detect_product_type(text)
    persona = detect_persona(text)
    trend = detect_trend(text)
    season = detect_season(text)
    vibe = detect_vibe(text)
    material = detect_material(text)
    silhouette = detect_silhouette(text)
    detail = detect_detail(text)

    # -----------------------------------------
    # EDITORIAL LAYER (BRAND_BRAIN)
    # -----------------------------------------
    editorial_short = generate_short_editorial(text)
    editorial_medium = generate_medium_editorial(text)
    editorial_long = generate_long_editorial(text)

    # Reserved for future persona/category/SEO-specific editorial
    editorial_persona = None
    editorial_category = None
    editorial_seo = None

    # -----------------------------------------
    # ALT TEXT LAYER (BRAND_BRAIN)
    # -----------------------------------------
    alt_short = generate_alt_text_short(text)
    alt_medium = generate_alt_text_medium(text)
    alt_long = generate_alt_text_long(text)

    # Reserved for future persona/category/SEO-specific alt text
    alt_persona = None
    alt_category = None
    alt_seo = None

    # -----------------------------------------
    # SEO LAYER (BRAND_BRAIN)
    # -----------------------------------------
    seo_primary = generate_primary_seo(text)
    seo_secondary = generate_secondary_seo(text)

    # -----------------------------------------
    # TAG LAYER (BRAND_BRAIN)
    # -----------------------------------------
    tags = generate_tags(
        text=text,
        category=category,
        product_type=product_type,
        persona=persona,
        trend=trend,
        season=season,
        vibe=vibe,
        material=material,
        silhouette=silhouette,
        detail=detail,
    )

    # -----------------------------------------
    # COLLECTION LAYER (BRAND_BRAIN)
    # -----------------------------------------
    collections = generate_collections(
        text=text,
        category=category,
        product_type=product_type,
        persona=persona,
        trend=trend,
        season=season,
        vibe=vibe,
        material=material,
        silhouette=silhouette,
        detail=detail,
    )

    # -----------------------------------------
    # VARIANTS + PRICE (BRAND_BRAIN)
    # -----------------------------------------
    variants = generate_variants(text)
    price = generate_price(text)

    # -----------------------------------------
    # TITLE + HANDLE (BRAND_BRAIN)
    # -----------------------------------------
    title = generate_title(text)
    handle = generate_handle(text)

    # -----------------------------------------
    # METAFIELD LAYER
    # -----------------------------------------
    metafields = generate_all_metafields(text)

    # -----------------------------------------
    # FINAL OMNILUXE PRODUCT DICTIONARY
    # -----------------------------------------
    return {
        "input_text": text,
        "seed": seed,

        # Core identity
        "title": title,
        "handle": handle,

        # Detection
        "category": category,
        "product_type": product_type,
        "persona": persona,
        "trend": trend,
        "season": season,
        "vibe": vibe,
        "material": material,
        "silhouette": silhouette,
        "detail": detail,

        # Editorial
        "editorial_short": editorial_short,
        "editorial_medium": editorial_medium,
        "editorial_long": editorial_long,
        "editorial_persona": editorial_persona,
        "editorial_category": editorial_category,
        "editorial_seo": editorial_seo,

        # Alt Text
        "alt_text_short": alt_short,
        "alt_text_medium": alt_medium,
        "alt_text_long": alt_long,
        "alt_text_persona": alt_persona,
        "alt_text_category": alt_category,
        "alt_text_seo": alt_seo,

        # SEO
        "seo_primary": seo_primary,
        "seo_secondary": seo_secondary,

        # Tags + Collections
        "tags": tags,
        "collections": collections,

        # Variants + Price
        "variants": variants,
        "price": price,

        # Metafields
        "metafields": metafields,
    }


# ---------------------------------------------------------
# BATCH WRAPPER
# ---------------------------------------------------------

def process_texts(texts: list) -> list:
    """
    Convenience wrapper to process multiple texts.
    """
    return [process_product(t) for t in texts]