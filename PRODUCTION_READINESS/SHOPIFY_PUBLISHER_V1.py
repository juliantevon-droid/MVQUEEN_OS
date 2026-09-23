"""MVQUEEN controlled Shopify publisher V1.

This is the only Shopify-facing publisher allowed to consume a canonical
production record. Authorization is enforced by PUBLISHING_BOUNDARY_V1;
this module is transport/mapping only and never generates product content.

The publisher intentionally updates only approved editorial/merchandising
fields. It does not mutate inventory, SKU, variant identity, or variant prices.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict


class ShopifyPublisherError(RuntimeError):
    """Raised when the Shopify transport rejects a publish operation."""


def _default_client() -> Any:
    """Load the repository Shopify transport without coupling package paths."""
    repo_root = Path(__file__).resolve().parents[1]
    engine_root = repo_root / "15_Scripts_And_Code"
    if str(engine_root) not in sys.path:
        sys.path.insert(0, str(engine_root))
    try:
        from mvqueen_engine.shopify_api import shopify_client
    except ImportError as exc:
        raise ShopifyPublisherError("Shopify transport is unavailable") from exc
    return shopify_client


def build_product_payload(record: Dict[str, Any]) -> Dict[str, Any]:
    """Map canonical fields to the narrowly scoped Shopify product payload."""
    identity = record.get("identity", {})
    category = record.get("category", {})
    copy = record.get("copy", {})
    merch = record.get("merchandising", {})

    product_id = identity.get("product_id")
    if not product_id:
        raise ShopifyPublisherError("identity.product_id is required")

    tags = merch.get("tags", [])
    if not isinstance(tags, list):
        tags = [str(tags)]

    return {
        "id": product_id,
        "title": copy.get("title", ""),
        "body_html": copy.get("description", ""),
        "vendor": "MVQueen",
        "product_type": category.get("product_type", ""),
        "tags": ", ".join(str(tag) for tag in tags if str(tag).strip()),
    }


def publish_to_shopify(record: Dict[str, Any], client: Any = None) -> Dict[str, Any]:
    """Publish one already-authorized canonical record through the transport.

    ``client`` is injectable for tests. No variant, inventory, SKU, handle, or
    price update is performed here. A false transport result is treated as a
    failed publication rather than a successful hand-off.
    """
    transport = client or _default_client()
    payload = build_product_payload(record)
    product_id = payload["id"]
    ok = transport.update_product(product_id, payload)
    if ok is not True:
        raise ShopifyPublisherError(f"Shopify product update failed for {product_id}")

    return {
        "product_id": product_id,
        "operation": "UPDATE_PRODUCT_EDITORIAL",
        "status": "SUCCESS",
    }


__all__ = ["ShopifyPublisherError", "build_product_payload", "publish_to_shopify"]
