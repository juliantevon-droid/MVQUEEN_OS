# ============================================================
# BLOCK 33 — SEO ENGINE (FINAL VERSION)
# ============================================================

from __future__ import annotations
import random
from typing import Dict, Any, List, Optional

from engine.engine_core import (
    get_engine,
    ensure_list,
    sanitize_text,
    with_seed,
)


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def generate_seo(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates:
      - primary keyword
      - secondary keywords
      - SEO title
      - meta description
      - alt text
      - canonical tag
      - SEO metafields
    Persona-aware, category-aware, deterministic.
    """

    seo_engine = get_engine("seo") or {}
    persona_engine = get_engine("personas") or {}
    category_engine = get_engine("category") or {}

    persona = product.get("persona")
    category = product.get("category")

    persona_rules = _get_persona_rules(persona_engine, persona)
    category_rules = _get_category_rules(category_engine, category)

    # Deterministic seed
    with_seed(
        product.get("handle"),
        persona,
        category,
        product.get("title"),
    )

    # 1. Primary keyword
    primary = _select_primary_keyword(seo_engine, persona_rules, category_rules, product)

    # 2. Secondary keywords
    secondary = _select_secondary_keywords(seo_engine, persona_rules, category_rules, primary)

    # 3. SEO title
    seo_title = _build_seo_title(seo_engine, product, primary, persona_rules, category_rules)

    # 4. Meta description
    meta_description = _build_meta_description(
        seo_engine, product, primary, secondary, persona_rules, category_rules
    )

    # 5. Alt text
    alt_text = _build_alt_text(seo_engine, product, primary, persona_rules, category_rules)

    # 6. Canonical
    canonical = _build_canonical(seo_engine, product)

    # 7. SEO metafields
    metafields = _build_seo_metafields(
        seo_engine, product, primary, secondary, persona_rules, category_rules
    )

    return {
        "primary_keyword": primary,
        "secondary_keywords": secondary,
        "seo_title": seo_title,
        "meta_description": meta_description,
        "alt_text": alt_text,
        "canonical": canonical,
        "seo_metafields": metafields,
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
# PRIMARY KEYWORD SELECTION
# ------------------------------------------------------------

def _select_primary_keyword(
    seo_engine: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    product: Dict[str, Any],
) -> str:
    # 1. Product override
    if product.get("primary_keyword"):
        return sanitize_text(product["primary_keyword"])

    # 2. Persona bias
    persona_bias = ensure_list(persona_rules.get("seo_bias"))
    if persona_bias:
        return random.choice(persona_bias)

    # 3. Category mapping
    category_keywords = ensure_list(category_rules.get("seo_keywords"))
    if category_keywords:
        return random.choice(category_keywords)

    # 4. Global pools
    pools = seo_engine.get("keyword_pools", {})
    default_pool = ensure_list(pools.get("default"))
    if default_pool:
        return random.choice(default_pool)

    # 5. Hard fallback
    return "luxury"


# ------------------------------------------------------------
# SECONDARY KEYWORD SELECTION
# ------------------------------------------------------------

def _select_secondary_keywords(
    seo_engine: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    primary: str,
) -> List[str]:
    pools = seo_engine.get("keyword_pools", {})
    secondary_pool = ensure_list(pools.get("secondary"))

    persona_secondary = ensure_list(persona_rules.get("secondary_keywords"))
    category_secondary = ensure_list(category_rules.get("secondary_keywords"))

    candidates = (
        persona_secondary
        or category_secondary
        or secondary_pool
    )

    if not candidates:
        return []

    # Remove duplicates + primary
    cleaned = [kw for kw in candidates if kw != primary]
    random.shuffle(cleaned)

    limit = seo_engine.get("secondary_limit", 3)
    return cleaned[:limit]


# ------------------------------------------------------------
# SEO TITLE BUILDER
# ------------------------------------------------------------

def _build_seo_title(
    seo_engine: Dict[str, Any],
    product: Dict[str, Any],
    primary: str,
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> str:
    # 1. Product override
    if product.get("seo_title"):
        return sanitize_text(product["seo_title"])

    patterns = (
        ensure_list(persona_rules.get("seo_title_patterns"))
        or ensure_list(category_rules.get("seo_title_patterns"))
        or ensure_list(seo_engine.get("title_patterns"))
    )

    if not patterns:
        return f"{product.get('title', '')} | {primary}"

    pattern = random.choice(patterns)

    return pattern.format(
        title=product.get("title", ""),
        brand=product.get("brand", ""),
        keyword=primary,
        category=product.get("category", ""),
    )


# ------------------------------------------------------------
# META DESCRIPTION BUILDER
# ------------------------------------------------------------

def _build_meta_description(
    seo_engine: Dict[str, Any],
    product: Dict[str, Any],
    primary: str,
    secondary: List[str],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> str:
    # 1. Product override
    if product.get("meta_description"):
        return sanitize_text(product["meta_description"])

    patterns = (
        ensure_list(persona_rules.get("meta_description_patterns"))
        or ensure_list(category_rules.get("meta_description_patterns"))
        or ensure_list(seo_engine.get("meta_description_patterns"))
    )

    if not patterns:
        # fallback
        desc = f"{product.get('title', '')} — a {primary}-focused essential designed for modern routines."
        return desc[:160]

    pattern = random.choice(patterns)

    desc = pattern.format(
        title=product.get("title", ""),
        brand=product.get("brand", ""),
        keyword=primary,
        keyword2=secondary[0] if secondary else "",
        category=product.get("category", ""),
    )

    # enforce length rules
    max_len = seo_engine.get("meta_description_max", 160)
    return desc[:max_len]


# ------------------------------------------------------------
# ALT TEXT BUILDER
# ------------------------------------------------------------

def _build_alt_text(
    seo_engine: Dict[str, Any],
    product: Dict[str, Any],
    primary: str,
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> str:
    # 1. Product override
    if product.get("alt_text"):
        return sanitize_text(product["alt_text"])

    patterns = (
        ensure_list(persona_rules.get("alt_text_patterns"))
        or ensure_list(category_rules.get("alt_text_patterns"))
        or ensure_list(seo_engine.get("alt_text_patterns"))
    )

    if not patterns:
        return f"{product.get('title', '')} — {primary}"

    pattern = random.choice(patterns)

    return pattern.format(
        title=product.get("title", ""),
        brand=product.get("brand", ""),
        keyword=primary,
        category=product.get("category", ""),
    )


# ------------------------------------------------------------
# CANONICAL BUILDER
# ------------------------------------------------------------

def _build_canonical(seo_engine: Dict[str, Any], product: Dict[str, Any]) -> str:
    base = seo_engine.get("canonical_base", "")
    handle = product.get("handle", "")
    if not base or not handle:
        return ""
    return f"{base.rstrip('/')}/{handle}"


# ------------------------------------------------------------
# SEO METAFIELDS
# ------------------------------------------------------------

def _build_seo_metafields(
    seo_engine: Dict[str, Any],
    product: Dict[str, Any],
    primary: str,
    secondary: List[str],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
) -> Dict[str, Any]:
    metafield_rules = seo_engine.get("metafields", {})

    namespace = metafield_rules.get("namespace", "seo")
    fields = metafield_rules.get("fields", {})

    output = {}

    for key, template in fields.items():
        output[key] = template.format(
            title=product.get("title", ""),
            brand=product.get("brand", ""),
            keyword=primary,
            keywords=", ".join(secondary),
            category=product.get("category", ""),
        )

    return {
        "namespace": namespace,
        "fields": output,
    }