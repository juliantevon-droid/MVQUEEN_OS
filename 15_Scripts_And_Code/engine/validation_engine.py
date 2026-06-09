from __future__ import annotations

# ============================================================
# BLOCK 36 — VALIDATION ENGINE (FINAL PATCHED VERSION)
# ============================================================

import re
from typing import Dict, Any, List

from engine.engine_core import (
    get_engine,
    ensure_list,
)


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def validate_product(product: Dict[str, Any]) -> Dict[str, Any]:
    validation_engine = get_engine("validation") or {}

    # --------------------------------------------------------
    # SANITIZE PRODUCT KEYS (fixes "unhashable type: dict")
    # --------------------------------------------------------
    clean_product = {}
    for k, v in product.items():
        if isinstance(k, str):
            clean_product[k] = v
    product = clean_product

    errors: List[Dict[str, Any]] = []

    # 1. Required fields
    errors.extend(_validate_required_fields(product, validation_engine))

    # 2. Type checks
    errors.extend(_validate_types(product, validation_engine))

    # 3. Price checks
    errors.extend(_validate_price(product, validation_engine))

    # 4. SEO checks
    errors.extend(_validate_seo(product, validation_engine))

    # 5. Handle checks
    errors.extend(_validate_handle(product, validation_engine))

    # 6. Image checks
    errors.extend(_validate_images(product, validation_engine))

    # 7. Metafield checks
    errors.extend(_validate_metafields(product, validation_engine))

    # 8. Persona + category checks
    errors.extend(_validate_persona_category(product, validation_engine))

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


# ------------------------------------------------------------
# REQUIRED FIELDS
# ------------------------------------------------------------

def _validate_required_fields(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors = []
    required = ensure_list(validation_engine.get("required_fields"))

    for field in required:
        if not isinstance(field, str):
            continue

        if field not in product or product[field] in (None, "", []):
            errors.append(_err("missing_required", f"Missing required field: {field}", field))

    return errors


# ------------------------------------------------------------
# TYPE CHECKS
# ------------------------------------------------------------

def _validate_types(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    type_rules = validation_engine.get("type_rules", {})
    errors = []

    for field, expected_type in type_rules.items():
        if field not in product:
            continue

        value = product[field]

        if expected_type == "string" and not isinstance(value, str):
            errors.append(_err("invalid_type", f"{field} must be a string", field))

        if expected_type == "number" and not isinstance(value, (int, float)):
            errors.append(_err("invalid_type", f"{field} must be a number", field))

        if expected_type == "list" and not isinstance(value, list):
            errors.append(_err("invalid_type", f"{field} must be a list", field))

        if expected_type == "dict" and not isinstance(value, dict):
            errors.append(_err("invalid_type", f"{field} must be a dict", field))

    return errors


# ------------------------------------------------------------
# PRICE VALIDATION
# ------------------------------------------------------------

def _validate_price(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors = []

    price = product.get("price")
    compare_at = product.get("compare_at_price")

    if price is not None and price < 0:
        errors.append(_err("invalid_price", "Price cannot be negative", "price"))

    if compare_at is not None and compare_at < price:
        errors.append(_err("invalid_compare_at", "Compare-at price must be >= price", "compare_at_price"))

    return errors


# ------------------------------------------------------------
# SEO VALIDATION
# ------------------------------------------------------------

def _validate_seo(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors = []

    seo = product.get("seo", {})
    primary = seo.get("primary_keyword", "")
    meta = seo.get("meta_description", "")

    if not primary:
        errors.append(_err("missing_primary_keyword", "Primary keyword missing", "seo.primary_keyword"))

    if len(meta) > validation_engine.get("max_meta_description_length", 160):
        errors.append(_err("meta_description_too_long", "Meta description exceeds max length", "seo.meta_description"))

    return errors


# ------------------------------------------------------------
# HANDLE VALIDATION
# ------------------------------------------------------------

def _validate_handle(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors = []

    handle = product.get("handle", "")
    if not handle:
        errors.append(_err("missing_handle", "Handle is missing", "handle"))
        return errors

    if " " in handle:
        errors.append(_err("invalid_handle", "Handle cannot contain spaces", "handle"))

    if handle != handle.lower():
        errors.append(_err("invalid_handle_case", "Handle must be lowercase", "handle"))

    return errors


# ------------------------------------------------------------
# IMAGE VALIDATION
# ------------------------------------------------------------

def _validate_images(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors = []

    images = product.get("images", [])
    if not isinstance(images, list):
        errors.append(_err("invalid_images", "Images must be a list", "images"))
        return errors

    min_images = validation_engine.get("min_images", 1)
    if len(images) < min_images:
        errors.append(_err("too_few_images", f"At least {min_images} images required", "images"))

    return errors


# ------------------------------------------------------------
# METAFIELD VALIDATION
# ------------------------------------------------------------

def _validate_metafields(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors = []

    metafields = product.get("metafields", {})
    if not isinstance(metafields, dict):
        errors.append(_err("invalid_metafields", "Metafields must be a dict", "metafields"))
        return errors

    allowed_namespaces = ensure_list(validation_engine.get("allowed_metafield_namespaces"))
    if allowed_namespaces:
        for ns in metafields.keys():
            if ns not in allowed_namespaces:
                errors.append(_err("invalid_namespace", f"Namespace '{ns}' not allowed", f"metafields.{ns}"))

    return errors


# ------------------------------------------------------------
# PERSONA + CATEGORY VALIDATION
# ------------------------------------------------------------

def _validate_persona_category(product: Dict[str, Any], validation_engine: Dict[str, Any]) -> List[Dict[str, Any]]:
    errors = []

    persona = product.get("persona")
    category = product.get("category")

    allowed_personas = ensure_list(validation_engine.get("allowed_personas"))
    allowed_categories = ensure_list(validation_engine.get("allowed_categories"))

    if allowed_personas and persona not in allowed_personas:
        errors.append(_err("invalid_persona", f"Persona '{persona}' not allowed", "persona"))

    if allowed_categories and category not in allowed_categories:
        errors.append(_err("invalid_category", f"Category '{category}' not allowed", "category"))

    return errors


# ------------------------------------------------------------
# ERROR HELPER
# ------------------------------------------------------------

def _err(code: str, message: str, field: str) -> Dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "field": field,
    }