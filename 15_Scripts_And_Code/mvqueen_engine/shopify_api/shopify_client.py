"""Controlled Shopify transport for MVQueen production publishing.

Read operations remain available to support inspection. Mutation operations are
strictly scoped: product updates may change only the editorial fields allowed
by SHOPIFY_PUBLISHER_V1. Variant, inventory, price, metafield, and arbitrary
product mutations are rejected here rather than delegated to a generic REST
client.
"""
from __future__ import annotations

from typing import Any, Dict
import requests

from ..config import SHOPIFY_BASE_URL, SHOPIFY_ACCESS_TOKEN

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


def get_all_products():
    """Fetch products for inspection; no mutation occurs."""
    response = requests.get(f"{SHOPIFY_BASE_URL}/products.json", headers=_headers(), timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"Shopify product read failed: HTTP {response.status_code}")
    return response.json().get("products", [])


def get_product(product_id: str):
    """Fetch one product for inspection; no mutation occurs."""
    response = requests.get(
        f"{SHOPIFY_BASE_URL}/products/{product_id}.json",
        headers=_headers(),
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Shopify product read failed: HTTP {response.status_code}")
    return response.json().get("product")


def update_product(product_id: str, data: Dict[str, Any]):
    """Apply the publisher's narrow editorial/merchandising field allowlist."""
    if not product_id:
        raise ValueError("product_id is required")
    unknown = set(data) - _ALLOWED_PRODUCT_FIELDS
    protected = unknown & _PROTECTED_FIELDS
    if protected:
        raise ValueError(f"Protected Shopify fields are not publishable: {sorted(protected)}")
    if unknown:
        raise ValueError(f"Unsupported Shopify product fields: {sorted(unknown)}")
    if data.get("id") not in (None, product_id):
        raise ValueError("Payload product id does not match product_id")

    product = {"id": product_id, **{k: v for k, v in data.items() if k != "id"}}
    response = requests.put(
        f"{SHOPIFY_BASE_URL}/products/{product_id}.json",
        json={"product": product},
        headers=_headers(),
        timeout=30,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Shopify product update failed: HTTP {response.status_code}")
    return response.json()


def update_metafields(product_id: str, metafields: Dict[str, Any]):
    """Disabled: legacy metafield writes must not bypass the canonical publisher."""
    raise RuntimeError(
        "Direct metafield mutation is disabled. Use an approved canonical release."
    )


def update_variant_price(variant_id: str, price: Any, compare_at: Any = None):
    """Disabled: price and variant identity are protected production fields."""
    raise RuntimeError(
        "Direct variant price mutation is disabled. Pricing requires the canonical release path."
    )


__all__ = [
    "get_all_products",
    "get_product",
    "update_product",
    "update_metafields",
    "update_variant_price",
]
