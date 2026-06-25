# ============================================================
# BLOCK 36 — IMAGE ENGINE (FINAL VERSION)
# ============================================================

from __future__ import annotations
from typing import Dict, Any, List, Optional
import random

from mvqueen_engine.engine_core import (
    get_engine,
    ensure_list,
    sanitize_text,
    with_seed,
)


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def generate_image_data(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates:
      - alt text (SEO + persona + category aware)
      - detected colors
      - detected materials
      - detected finishes
      - detected textures
      - image tags
    """

    image_engine = get_engine("image") or {}
    persona_engine = get_engine("personas") or {}
    category_engine = get_engine("category") or {}
    seo_engine = get_engine("seo") or {}

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

    # 1. Detect attributes
    colors = _detect_colors(product, image_engine)
    materials = _detect_materials(product, image_engine)
    finishes = _detect_finishes(product, image_engine)
    textures = _detect_textures(product, image_engine)

    # 2. Alt text
    alt_text = _build_alt_text(
        product,
        image_engine,
        persona_rules,
        category_rules,
        colors,
        materials,
        finishes,
        textures,
    )

    # 3. Image tags
    tags = _build_image_tags(
        product,
        persona_rules,
        category_rules,
        colors,
        materials,
        finishes,
        textures,
    )

    return {
        "colors": colors,
        "materials": materials,
        "finishes": finishes,
        "textures": textures,
        "alt_text": alt_text,
        "image_tags": tags,
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
# DETECTION HELPERS
# ------------------------------------------------------------

def _detect_colors(product: Dict[str, Any], image_engine: Dict[str, Any]) -> List[str]:
    # Product override
    if product.get("colors"):
        return ensure_list(product["colors"])

    # Config-based detection
    color_map = image_engine.get("color_map", {})
    title = sanitize_text(product.get("title", "")).lower()

    detected = [color for color in color_map if color in title]
    return detected or ensure_list(image_engine.get("default_colors"))


def _detect_materials(product: Dict[str, Any], image_engine: Dict[str, Any]) -> List[str]:
    if product.get("materials"):
        return ensure_list(product["materials"])

    material_map = image_engine.get("material_map", {})
    title = sanitize_text(product.get("title", "")).lower()

    detected = [mat for mat in material_map if mat in title]
    return detected or ensure_list(image_engine.get("default_materials"))


def _detect_finishes(product: Dict[str, Any], image_engine: Dict[str, Any]) -> List[str]:
    if product.get("finishes"):
        return ensure_list(product["finishes"])

    finish_map = image_engine.get("finish_map", {})
    title = sanitize_text(product.get("title", "")).lower()

    detected = [f for f in finish_map if f in title]
    return detected or ensure_list(image_engine.get("default_finishes"))


def _detect_textures(product: Dict[str, Any], image_engine: Dict[str, Any]) -> List[str]:
    if product.get("textures"):
        return ensure_list(product["textures"])

    texture_map = image_engine.get("texture_map", {})
    title = sanitize_text(product.get("title", "")).lower()

    detected = [t for t in texture_map if t in title]
    return detected or ensure_list(image_engine.get("default_textures"))


# ------------------------------------------------------------
# ALT TEXT BUILDER
# ------------------------------------------------------------

def _build_alt_text(
    product: Dict[str, Any],
    image_engine: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    colors: List[str],
    materials: List[str],
    finishes: List[str],
    textures: List[str],
) -> str:

    # Product override
    if product.get("alt_text"):
        return sanitize_text(product["alt_text"])

    # Persona-specific patterns
    persona_patterns = ensure_list(persona_rules.get("alt_text_patterns"))
    if persona_patterns:
        pattern = random.choice(persona_patterns)
        return _render_alt(pattern, product, colors, materials, finishes, textures)

    # Category-specific patterns
    category_patterns = ensure_list(category_rules.get("alt_text_patterns"))
    if category_patterns:
        pattern = random.choice(category_patterns)
        return _render_alt(pattern, product, colors, materials, finishes, textures)

    # Global patterns
    global_patterns = ensure_list(image_engine.get("alt_text_patterns"))
    if global_patterns:
        pattern = random.choice(global_patterns)
        return _render_alt(pattern, product, colors, materials, finishes, textures)

    # Hard fallback
    return f"{product.get('title', '')} product image"


def _render_alt(
    pattern: str,
    product: Dict[str, Any],
    colors: List[str],
    materials: List[str],
    finishes: List[str],
    textures: List[str],
) -> str:
    return pattern.format(
        title=product.get("title", ""),
        brand=product.get("brand", ""),
        color=", ".join(colors),
        material=", ".join(materials),
        finish=", ".join(finishes),
        texture=", ".join(textures),
        category=product.get("category", ""),
    )


# ------------------------------------------------------------
# IMAGE TAGS
# ------------------------------------------------------------

def _build_image_tags(
    product: Dict[str, Any],
    persona_rules: Dict[str, Any],
    category_rules: Dict[str, Any],
    colors: List[str],
    materials: List[str],
    finishes: List[str],
    textures: List[str],
) -> List[str]:

    tags = []

    # Persona-based tags
    tags.extend(ensure_list(persona_rules.get("image_tags")))

    # Category-based tags
    tags.extend(ensure_list(category_rules.get("image_tags")))

    # Attribute tags
    for c in colors:
        tags.append(f"color:{c}")
    for m in materials:
        tags.append(f"material:{m}")
    for f in finishes:
        tags.append(f"finish:{f}")
    for t in textures:
        tags.append(f"texture:{t}")

    return list(set(tags))