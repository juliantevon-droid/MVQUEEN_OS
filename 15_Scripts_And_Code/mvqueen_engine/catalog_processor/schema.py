"""MVQueen catalog schema and validation foundation.

This module is additive: it preserves the existing dictionary validation model
while providing a richer product record for the new modular engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

REQUIRED_FIELDS = ["title", "description", "category", "product_type"]

SHOPIFY_CORE_FIELDS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Product Category",
    "Type", "Tags", "Published", "Option1 Name", "Option1 Value",
    "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
    "Variant Inventory Qty", "Variant Inventory Policy", "Variant Fulfillment Service",
    "Variant Price", "Variant Compare At Price", "Variant Requires Shipping",
    "Variant Taxable", "Variant Barcode", "Image Src", "Image Position",
    "Image Alt Text", "Gift Card", "SEO Title", "SEO Description",
]

MVQUEEN_METAFIELDS = [
    "metafield.custom.voice", "metafield.custom.intent", "metafield.custom.collection",
    "metafield.custom.prestige_score", "metafield.custom.product_quality_score",
    "metafield.custom.shopify_bundle_safe", "metafield.custom.alt_text",
    "metafield.custom.target_audience", "metafield.custom.key_benefits",
    "metafield.custom.product_type_detailed", "metafield.custom.texture",
    "metafield.custom.finish", "metafield.custom.mood",
    "metafield.custom.short_description", "metafield.custom.long_description",
    "metafield.custom.who_its_for", "metafield.custom.results",
    "metafield.custom.usage", "metafield.custom.material", "metafield.custom.ingredients",
    "metafield.custom.benefits", "metafield.custom.seasonality", "metafield.custom.vibe",
    "metafield.custom.persona", "metafield.custom.trend", "metafield.custom.silhouette",
    "metafield.custom.details", "metafield.custom.occasion", "metafield.custom.fit",
    "metafield.custom.certifications", "metafield.custom.faq", "metafield.custom.seo_keywords",
    "metafield.custom.trust_badges",
]


@dataclass
class ProductRecord:
    """Complete internal representation used between catalog pipeline stages."""

    handle: str = ""
    title: str = ""
    body_html: str = ""
    vendor: str = "MVQueen"
    product_type: str = ""
    tags: List[str] = field(default_factory=list)
    collections: List[str] = field(default_factory=list)

    price: Optional[float] = None
    compare_at_price: Optional[float] = None
    sku: str = ""
    barcode: str = ""
    image_alt_text: str = ""

    category: str = "default"
    product_type_detailed: str = ""
    persona: str = ""
    vibe: str = ""
    trend: str = ""
    season: str = ""
    material: str = ""
    silhouette: str = ""
    details: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    ingredients: List[str] = field(default_factory=list)
    textures: List[str] = field(default_factory=list)
    finishes: List[str] = field(default_factory=list)
    occasion: str = ""
    fit: str = ""

    voice: str = ""
    intent: str = ""
    collection: str = ""
    target_audience: str = ""
    who_its_for: str = ""
    results: str = ""
    mood: str = ""
    key_benefits: str = ""

    generated_title: str = ""
    short_description: str = ""
    long_description: str = ""
    seo_title: str = ""
    seo_description: str = ""
    alt_text: str = ""

    prestige_score: Optional[float] = None
    product_quality_score: Optional[float] = None
    shopify_bundle_safe: bool = False

    metafields: Dict[str, Any] = field(default_factory=dict)
    source: Dict[str, Any] = field(default_factory=dict)
    seed: str = ""


def validate_item(item: Dict[str, Any]) -> List[str]:
    """Validate a dictionary using the legacy required-field contract."""
    errors: List[str] = []
    for field_name in REQUIRED_FIELDS:
        if field_name not in item or not item[field_name]:
            errors.append(f"Missing required field: {field_name}")
    return errors


def validate_batch(items: List[Dict[str, Any]]) -> Dict[int, List[str]]:
    """Validate many dictionary records and return only invalid indexes."""
    results: Dict[int, List[str]] = {}
    for index, item in enumerate(items):
        errors = validate_item(item)
        if errors:
            results[index] = errors
    return results


def ensure_columns(columns: List[str]) -> List[str]:
    """Return a stable union of Shopify and MVQueen columns."""
    seen = set(columns)
    result = list(columns)
    for column in SHOPIFY_CORE_FIELDS + MVQUEEN_METAFIELDS:
        if column not in seen:
            result.append(column)
            seen.add(column)
    return result


__all__ = [
    "ProductRecord", "REQUIRED_FIELDS", "SHOPIFY_CORE_FIELDS",
    "MVQUEEN_METAFIELDS", "validate_item", "validate_batch", "ensure_columns",
]
