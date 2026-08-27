"""MVQueen custom metafield construction.

This module is deliberately conservative: it never invents product facts. It
maps detected/editorial values into Shopify-ready custom metafield payloads
and preserves empty/unknown values instead of fabricating claims.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

PREFIX = "metafield.custom."

TEXT_KEYS = (
    "voice", "intent", "collection", "persona", "vibe", "trend", "season",
    "material", "silhouette", "details", "benefits", "ingredients",
    "texture", "finish", "mood", "target_audience", "who_its_for", "results",
    "occasion", "fit", "style", "usage", "certifications", "faq",
    "seo_keywords", "trust_badges", "short_description", "long_description",
)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value != value:
        return ""
    return str(value).strip()


def build_metafield_values(data: Mapping[str, Any]) -> dict[str, str]:
    """Return populated MVQueen custom metafields from normalized product data."""
    result: dict[str, str] = {}
    for key in TEXT_KEYS:
        value = _clean(data.get(key, data.get(PREFIX + key, "")))
        if value:
            result[key] = value
    return result


def build_shopify_metafields(data: Mapping[str, Any]) -> list[dict[str, str]]:
    """Build Admin API-compatible metafield objects.

    Text values use Shopify's single-line type only when appropriate; longer
    generated editorial fields use multi_line_text_field.
    """
    values = build_metafield_values(data)
    multiline = {"short_description", "long_description", "benefits", "ingredients", "results", "faq"}
    payload: list[dict[str, str]] = []
    for key, value in values.items():
        payload.append({
            "namespace": "custom",
            "key": key,
            "type": "multi_line_text_field" if key in multiline else "single_line_text_field",
            "value": value,
        })
    return payload


def merge_metafields(existing: Mapping[str, Any], generated: Mapping[str, Any]) -> dict[str, Any]:
    """Merge generated values without deleting unrelated existing values."""
    merged = dict(existing)
    for key, value in generated.items():
        cleaned = _clean(value)
        if cleaned:
            merged[key] = cleaned
    return merged
