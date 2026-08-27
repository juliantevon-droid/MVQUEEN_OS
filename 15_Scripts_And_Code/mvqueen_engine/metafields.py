"""MVQueen enterprise metafield compatibility layer.

Preserves the existing generate_all_metafields contract while exposing the
new catalog_processor metafield builder. The legacy detector/editorial stack
remains the source of richer generated fields; the normalized mapper handles
safe Shopify payload construction.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping

try:
    from brand_brain.detection.detect_category import detect_category
    from brand_brain.detection.detect_product_type import detect_product_type
    from brand_brain.detection.detect_trend import detect_trend
    from brand_brain.detection.detect_season import detect_season
    from brand_brain.detection.detect_vibe import detect_vibe
    from brand_brain.detection.detect_material import detect_material
    from brand_brain.detection.detect_silhouette import detect_silhouette
    from brand_brain.detection.detect_details import detect_details
    from brand_brain.detection.detect_persona import detect_persona
except ImportError:  # package-relative fallback for installed use
    detect_category = detect_product_type = detect_trend = detect_season = None
    detect_vibe = detect_material = detect_silhouette = detect_details = detect_persona = None


def mf(namespace: str, key: str, value: Any, type_: str) -> dict[str, Any]:
    """Create one Shopify-native metafield entry."""
    return {f"{namespace}.{key}": {"value": value, "type": type_}}


def _call(detector, text: str) -> str:
    if detector is None:
        return ""
    try:
        value = detector(text)
        return "" if value is None else str(value)
    except (TypeError, ValueError, KeyError, AttributeError):
        return ""


def generate_all_metafields(text: str) -> Dict[str, Any]:
    """Generate the legacy MVQueen metafield map without fabricating facts."""
    category = _call(detect_category, text)
    product_type = _call(detect_product_type, text)
    trend = _call(detect_trend, text)
    season = _call(detect_season, text)
    vibe = _call(detect_vibe, text)
    material = _call(detect_material, text)
    silhouette = _call(detect_silhouette, text)
    detail = _call(detect_details, text)
    persona = _call(detect_persona, text)

    return {
        **mf("custom.mvq", "category", category, "single_line_text_field"),
        **mf("custom.mvq", "product_type", product_type, "single_line_text_field"),
        **mf("custom.mvq", "trend", trend, "single_line_text_field"),
        **mf("custom.mvq", "season", season, "single_line_text_field"),
        **mf("custom.mvq", "vibe", vibe, "single_line_text_field"),
        **mf("custom.mvq", "material", material, "single_line_text_field"),
        **mf("custom.mvq", "silhouette", silhouette, "single_line_text_field"),
        **mf("custom.mvq", "detail", detail, "single_line_text_field"),
        **mf("custom.mvq", "persona", persona, "single_line_text_field"),
    }


def build_custom_metafields(data: Mapping[str, Any]) -> list[dict[str, str]]:
    """Build Shopify Admin API objects from normalized MVQueen data."""
    try:
        from .catalog_processor.metafields import build_shopify_metafields
    except ImportError:
        from catalog_processor.metafields import build_shopify_metafields
    return build_shopify_metafields(data)


def merge_preserving(existing: Mapping[str, Any], generated: Mapping[str, Any]) -> dict[str, Any]:
    """Merge non-empty generated values without deleting unrelated data."""
    result = dict(existing)
    for key, value in generated.items():
        if value is not None and str(value).strip():
            result[key] = value
    return result
