# ============================================================
# BLOCK 37 — HANDLE ENGINE (FINAL PATCHED VERSION)
# ============================================================

from __future__ import annotations
import re
import random
from typing import Dict, Any, Optional

from mvqueen_engine.engine_core import (
    get_engine,
    sanitize_text,
    ensure_list,
    with_seed,
)


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def generate_handle(product: Dict[str, Any]) -> str:
    """
    Generates a Shopify-safe handle using:
      - product title
      - persona modifiers
      - category modifiers
      - SEO keyword
      - deterministic slug rules
    """

    handle_engine = get_engine("handle") or {}
    persona_engine = get_engine("personas") or {}
    category_engine = get_engine("category") or {}

    persona = product.get("persona")
    category = product.get("category")
    primary_keyword = product.get("primary_keyword", "")

    persona_rules = _get_persona_rules(persona_engine, persona)
    category_rules = _get_category_rules(category_engine, category)

    # Deterministic seed
    with_seed(
        product.get("title"),
        persona,
        category,
        primary_keyword,
    )

    # 1. Base slug from title
    base = _slugify(product.get("title", ""))

    # 2. Persona modifier
    persona_mod = _select_modifier(persona_rules.get("handle_modifiers"))

    # 3. Category modifier
    category_mod = _select_modifier(category_rules.get("handle_modifiers"))

    # 4. SEO keyword modifier
    seo_mod = _select_modifier(handle_engine.get("seo_modifiers"))

    # --------------------------------------------------------
    # 5. Assemble + SANITIZE (this fixes your crash)
    # --------------------------------------------------------
    raw_parts = [base, persona_mod, category_mod, seo_mod]

    clean_parts = []
    for p in raw_parts:
        if isinstance(p, str):
            clean_parts.append(p)
        else:
            # Remove dicts, lists, numbers, None, etc.
            clean_parts.append("")

    # Remove empty strings
    clean_parts = [p for p in clean_parts if p]

    handle = "-".join(clean_parts)

    # 6. Clean + enforce Shopify rules
    handle = _clean_handle(handle)

    return handle


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
# SLUGIFY
# ------------------------------------------------------------

def _slugify(text: str) -> str:
    text = sanitize_text(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


# ------------------------------------------------------------
# MODIFIER SELECTION
# ------------------------------------------------------------

def _select_modifier(pool: Any) -> str:
    pool = ensure_list(pool)
    if not pool:
        return ""
    return random.choice(pool)


# ------------------------------------------------------------
# HANDLE CLEANING
# ------------------------------------------------------------

def _clean_handle(handle: str) -> str:
    # Lowercase
    handle = handle.lower()

    # Remove invalid chars
    handle = re.sub(r"[^a-z0-9\-]", "", handle)

    # Collapse dashes
    handle = re.sub(r"-+", "-", handle)

    # Trim
    handle = handle.strip("-")

    return handle