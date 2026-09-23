"""Compatibility Shopify transport with production-safe mutation boundaries.

The canonical publisher is the only supported production write entry point.
This module retains read helpers for inspection and exposes only the same narrow
editorial product mutation contract as SHOPIFY_PUBLISHER_V1.
"""
from __future__ import annotations

from typing import Any, Dict
import requests

from mvqueen_engine.config import SHOPIFY_BASE_URL, SHOPIFY_ACCESS_TOKEN

_ALLOWED_PRODUCT_FIELDS = frozenset({"id", "title", "body_html", "vendor", "product_type", "tags"})
_PROTECTED_FIELDS = frozenset({
    "handle", "sku", "variants", "options", "inventory", "inventory_quantity",
    "inventory_management", "inventory_policy", "price", "compare_at_price",
})


def _headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }


def get_all_products(limit: int = 250):
    """Fetch products for inspection only."""
    response = requests.get(
        f"{SHOPIFY_BASE_URL}/products.json?limit={limit}",
        headers=_headers(),
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Shopify product read failed: HTTP {response.status_code}")
    return response.json().get("products", [])


def get_product(product_id: str):
    """Fetch one product for inspection only."""
    response = requests.get(
        f"{SHOPIFY_BASE_URL}/products/{product_id}.json",
        headers=_headers(),
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Shopify product read failed: HTTP {response.status_code}")
    return response.json().get("product")


def update_product(product_id: str, updates: Dict[str, Any]):
    """Allow only the publisher's explicitly approved product fields."""
    if not product_id:
        raise ValueError("product_id is required")
    unknown = set(updates) - _ALLOWED_PRODUCT_FIELDS
    protected = unknown & _PROTECTED_FIELDS
    if protected:
        raise ValueError(f"Protected Shopify fields are not publishable: {sorted(protected)}")
    if unknown:
        raise ValueError(f"Unsupported Shopify product fields: {sorted(unknown)}")
    if updates.get("id") not in (None, product_id):
        raise ValueError("Payload product id does not match product_id")
    payload = {"product": {"id": product_id, **{k: v for k, v in updates.items() if k != "id"}}}
    response = requests.put(
        f"{SHOPIFY_BASE_URL}/products/{product_id}.json",
        json=payload,
        headers=_headers(),
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Shopify product update failed: HTTP {response.status_code}")
    return response.json()


def update_metafields(product_id: str, metafields: Dict[str, Any]):
    raise RuntimeError("Direct metafield mutation is disabled; use an approved canonical release.")


def update_variant_price(variant_id: str, price: Any, compare_at_price: Any = None):
    raise RuntimeError("Direct variant price mutation is disabled; use the canonical release path.")


__all__ = [
    "get_all_products",
    "get_product",
    "update_product",
    "update_metafields",
    "update_variant_price",
]
