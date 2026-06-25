# ---------------------------------------------------------
# MVQUEEN OMNILUXE — FULL ENTERPRISE SHOPIFY METAFIELDS ENGINE
# ---------------------------------------------------------

from typing import Dict, List

# ---------------------------------------------------------
# DETECTION MODULES
# ---------------------------------------------------------

from brand_brain.detection.detect_category import detect_category
from brand_brain.detection.detect_product_type import detect_product_type
from brand_brain.detection.detect_trend import detect_trend
from brand_brain.detection.detect_season import detect_season
from brand_brain.detection.detect_vibe import detect_vibe
from brand_brain.detection.detect_material import detect_material
from brand_brain.detection.detect_silhouette import detect_silhouette
from brand_brain.detection.detect_details import detect_details
from brand_brain.detection.detect_persona import detect_persona

# ---------------------------------------------------------
# EDITORIAL + SEO MODULES
# ---------------------------------------------------------

from brand_brain.editorial.frames import generate_frames
from brand_brain.editorial.seo import generate_seo_block

# ---------------------------------------------------------
# ALT TEXT MODULES
# ---------------------------------------------------------

from brand_brain.editorial.alt_text import (
    generate_alt_text_short,
    generate_alt_text_medium,
    generate_alt_text_long,
)

# ---------------------------------------------------------
# SHOPIFY METAFIELD HELPER
# ---------------------------------------------------------

def mf(namespace: str, key: str, value, type_: str):
    """Creates a Shopify-native metafield entry."""
    return {f"{namespace}.{key}": {"value": value, "type": type_}}

# ---------------------------------------------------------
# MASTER METAFIELD BUILDER
# ---------------------------------------------------------

def generate_all_metafields(text: str) -> Dict:
    metafields = {}

    # -----------------------------------------------------
    # DETECTION OUTPUT
    # -----------------------------------------------------
    category = detect_category(text)
    product_type = detect_product_type(text)
    trend = detect_trend(text)
    season = detect_season(text)
    vibe = detect_vibe(text)
    material = detect_material(text)
    silhouette = detect_silhouette(text)
    detail = detect_details(text)
    persona = detect_persona(text)

    # -----------------------------------------------------
    # EDITORIAL OUTPUT
    # -----------------------------------------------------
    framed_description = generate_frames(text)
    seo_block = generate_seo_block(text)

    # -----------------------------------------------------
    # ALT TEXT OUTPUT
    # -----------------------------------------------------
    alt_short = generate_alt_text_short(text)
    alt_medium = generate_alt_text_medium(text)
    alt_long = generate_alt_text_long(text)

    # -----------------------------------------------------
    # MVQUEEN METAFIELDS (custom.mvq.*)
    # -----------------------------------------------------
    metafields.update(mf("custom.mvq", "category", category, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "product_type", product_type, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "trend", trend, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "season", season, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "vibe", vibe, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "material", material, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "silhouette", silhouette, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "detail", detail, "single_line_text_field"))
    metafields.update(mf("custom.mvq", "persona", persona, "single_line_text_field"))

    metafields.update(mf("custom.mvq", "framed_description", framed_description, "multi_line_text_field"))
    metafields.update(mf("custom.mvq", "seo_block", seo_block, "multi_line_text_field"))

    # -----------------------------------------------------
    # ALT TEXT METAFIELDS (alt.*)
    # -----------------------------------------------------
    metafields.update(mf("alt", "short", alt_short, "single_line_text_field"))
    metafields.update(mf("alt", "medium", alt_medium, "multi_line_text_field"))
    metafields.update(mf("alt", "long", alt_long, "multi_line_text_field"))

    # -----------------------------------------------------
    # SHOPIFY SEO METAFIELDS (seo.*)
    # -----------------------------------------------------
    metafields.update(mf("seo", "title", text, "single_line_text_field"))
    metafields.update(mf("seo", "description", framed_description, "multi_line_text_field"))
    metafields.update(mf("seo", "keywords", [category, trend, vibe], "list.single_line_text_field"))

    # -----------------------------------------------------
    # GOOGLE SHOPPING METAFIELDS (google.shopping.*)
    # -----------------------------------------------------
    metafields.update(mf("google.shopping", "product_category", category, "single_line_text_field"))
    metafields.update(mf("google.shopping", "material", material, "single_line_text_field"))
    metafields.update(mf("google.shopping", "pattern", detail, "single_line_text_field"))
    metafields.update(mf("google.shopping", "color", "", "single_line_text_field"))
    metafields.update(mf("google.shopping", "size", "", "single_line_text_field"))
    metafields.update(mf("google.shopping", "gender", "female", "single_line_text_field"))
    metafields.update(mf("google.shopping", "age_group", "adult", "single_line_text_field"))

    # -----------------------------------------------------
    # CUSTOM METAFIELDS (custom.*)
    # -----------------------------------------------------
    metafields.update(mf("custom", "care_instructions", "", "multi_line_text_field"))
    metafields.update(mf("custom", "shipping_note", "", "single_line_text_field"))
    metafields.update(mf("custom", "size_guide", "", "multi_line_text_field"))
    metafields.update(mf("custom", "trust_badges", [], "list.single_line_text_field"))
    metafields.update(mf("custom", "highlights", [], "list.single_line_text_field"))
    metafields.update(mf("custom", "badge", "", "single_line_text_field"))

    return metafields