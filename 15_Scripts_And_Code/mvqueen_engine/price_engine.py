# ============================================================
# BLOCK 35 — PRICE ENGINE (FINAL VERSION)
# ============================================================

from __future__ import annotations
from typing import Dict, Any, Optional

from mvqueen_engine.engine_core import (
    get_engine,
    ensure_list,
    sanitize_text,
    with_seed,
)


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def generate_price(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates:
      - base price
      - persona-adjusted price
      - category-adjusted price
      - bundle-adjusted price
      - luxury/prestige tier adjustments
      - compare_at_price
      - price tags
      - price collections
    """

    price_engine = get_engine("price") or {}
    persona_engine = get_engine("personas") or {}
    category_engine = get_engine("category") or {}
    bundle_engine = get_engine("bundle_settings") or {}

    persona = product.get("persona")
    category = product.get("category")
    is_bundle = product.get("is_bundle", False)

    persona_rules = _get_persona_rules(persona_engine, persona)
    category_rules = _get_category_rules(category_engine, category)

    # Deterministic seed
    with_seed(
        product.get("handle"),
        persona,
        category,
        product.get("title"),
    )

    # 1. Base price
    base_price = _get_base_price(product, price_engine)

    # 2. Persona adjustments
    persona_price = _apply_persona_adjustments(base_price, persona_rules)

    # 3. Category adjustments
    category_price = _apply_category_adjustments(persona_price, category_rules)

    # 4. Bundle adjustments
    final_price = _apply_bundle_adjustments(category_price, bundle_engine, is_bundle)

    # 5. Luxury / prestige tiers
    final_price = _apply_tier_adjustments(final_price, persona_rules, category_rules)

    # 6. Rounding
    final_price = _round_price(final_price, price_engine)

    # 7. Compare-at price
    compare_at = _build_compare_at(final_price, price_engine, persona_rules, category_rules)

    # 8. Price tags
    price_tags = _build_price_tags(final_price, price_engine, persona_rules, category_rules)

    # 9. Price collections
    price_collections = _build_price_collections(final_price, price_engine, persona_rules, category_rules)

    return {
        "price": final_price,
        "compare_at_price": compare_at,
        "price_tags": price_tags,
        "price_collections": price_collections,
    }


# ------------------------------------------------------------
# CONFIG HELPERS
# ------------------------------------------------------------

def _get_persona_rules(persona_engine: Dict[str, Any], persona: Optional[str]) -> Dict[str, Any]:
    personas = persona_engine.get("personas", {})
    return personas.get(persona, personas.get("default", {}))


def _get_category_rules(category_engine: Dict[str, Any], category: Optional[str]) -> Dict[str, Any]:
    if not category:
        return {}
    categories = category_engine.get("categories", {})
    return categories.get(category, categories.get("default", {}))


# ------------------------------------------------------------
# BASE PRICE
# ------------------------------------------------------------

def _get_base_price(product: Dict[str, Any], price_engine: Dict[str, Any]) -> float:
    # 1. Product override
    if product.get("price"):
        return float(product["price"])

    # 2. Category base price
    category = product.get("category")
    category_bases = price_engine.get("category_base_prices", {})
    if category in category_bases:
        return float(category_bases[category])

    # 3. Global base price
    return float(price_engine.get("default_base_price", 19.99))


# ------------------------------------------------------------
# PERSONA ADJUSTMENTS
# ------------------------------------------------------------

def _apply_persona_adjustments(price: float, persona_rules: Dict[str, Any]) -> float:
    multiplier = persona_rules.get("price_multiplier")
    if multiplier:
        return price * float(multiplier)
    return price


# ------------------------------------------------------------
# CATEGORY ADJUSTMENTS
# ------------------------------------------------------------

def _apply_category_adjustments(price: float, category_rules: Dict[str, Any]) -> float:
    multiplier = category_rules.get("price_multiplier")
    if multiplier:
        return price * float(multiplier)
    return price


# ------------------------------------------------------------
# BUNDLE ADJUSTMENTS
# ------------------------------------------------------------

def _apply_bundle_adjustments(price: float, bundle_engine: Dict[str, Any], is_bundle: bool) -> float:
    if not is_bundle:
        return price

    discount = bundle_engine.get("discount_rate", 0.15)
    return price * (1 - float(discount))


# ------------------------------------------------------------
# LUXURY / PRESTIGE TIER ADJUSTMENTS
# ------------------------------------------------------------

def _apply_tier_adjustments(
    price: float,
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> float:
    tier = persona_rules.get("tier") or category_rules.get("price_tier")

    if tier == "luxury":
        return price * 1.25
    if tier == "prestige":
        return price * 1.40
    if tier == "ultra_luxury":
        return price * 1.75

    return price


# ------------------------------------------------------------
# ROUNDING
# ------------------------------------------------------------

def _round_price(price: float, price_engine: Dict[str, Any]) -> float:
    rounding = price_engine.get("round_to", 0.99)

    # Example: 34.99, 49.99, etc.
    return float(int(price)) + float(rounding)


# ------------------------------------------------------------
# COMPARE-AT PRICE
# ------------------------------------------------------------

def _build_compare_at(
    price: float,
    price_engine: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> float:
    # Persona override
    persona_compare = persona_rules.get("compare_at_multiplier")
    if persona_compare:
        return price * float(persona_compare)

    # Category override
    category_compare = category_rules.get("compare_at_multiplier")
    if category_compare:
        return price * float(category_compare)

    # Global
    global_compare = price_engine.get("compare_at_multiplier", 1.25)
    return price * float(global_compare)


# ------------------------------------------------------------
# PRICE TAGS
# ------------------------------------------------------------

def _build_price_tags(
    price: float,
    price_engine: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> list:
    tags = []

    # Persona-based tags
    persona_tags = ensure_list(persona_rules.get("price_tags"))
    tags.extend(persona_tags)

    # Category-based tags
    category_tags = ensure_list(category_rules.get("price_tags"))
    tags.extend(category_tags)

    # Price-tier tags
    tiers = price_engine.get("price_tiers", {})
    for tier_name, tier_range in tiers.items():
        low, high = tier_range
        if low <= price <= high:
            tags.append(f"tier:{tier_name}")

    return list(set(tags))


# ------------------------------------------------------------
# PRICE COLLECTIONS
# ------------------------------------------------------------

def _build_price_collections(
    price: float,
    price_engine: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> list:
    collections = []

    # Persona-based collections
    persona_cols = ensure_list(persona_rules.get("price_collections"))
    collections.extend(persona_cols)

    # Category-based collections
    category_cols = ensure_list(category_rules.get("price_collections"))
    collections.extend(category_cols)

    # Price-tier collections
    tiers = price_engine.get("price_tiers", {})
    for tier_name, tier_range in tiers.items():
        low, high = tier_range
        if low <= price <= high:
            collections.append(f"Price Tier — {tier_name.title()}")

    return list(set(collections))