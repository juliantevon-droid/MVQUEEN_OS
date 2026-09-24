"""MVQUEEN controlled publisher contract.

Python owns canonical record validation, QA, release fingerprints, approval
verification, preview generation, and transport-neutral payload construction.

Python does NOT discover or create a live Shopify transport. The only live
Shopify writer in MVQUEEN_OS is the authenticated React Router Shopify app.
A transport may be injected here only for deterministic tests or an explicitly
controlled caller.
"""
from __future__ import annotations

from typing import Any, Dict


class ShopifyPublisherError(RuntimeError):
    """Raised when a controlled publish hand-off is invalid."""


def build_product_payload(record: Dict[str, Any]) -> Dict[str, Any]:
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
    """Hand an authorized record to an explicitly injected client.

    There is deliberately no repository-default network client. A caller that
    omits client is blocked. Production network writes are owned by
    app/lib/product-processor.ts.
    """
    if client is None:
        raise ShopifyPublisherError(
            "No Python Shopify transport is configured. "
            "Production writes belong to the authenticated React Router app."
        )

    payload = build_product_payload(record)
    product_id = payload["id"]
    ok = client.update_product(product_id, payload)
    if ok is not True:
        raise ShopifyPublisherError(f"Shopify product update failed for {product_id}")

    return {
        "product_id": product_id,
        "operation": "UPDATE_PRODUCT_EDITORIAL",
        "status": "SUCCESS",
    }


__all__ = ["ShopifyPublisherError", "build_product_payload", "publish_to_shopify"]
