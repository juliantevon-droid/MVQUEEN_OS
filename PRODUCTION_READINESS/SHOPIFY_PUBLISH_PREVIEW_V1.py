"""MVQueen Shopify publish preview V1.

Builds a deterministic, human-reviewable description of the exact Shopify
product fields the controlled publisher would attempt to change. This module
never calls Shopify and never authorizes publication.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from SHOPIFY_PUBLISHER_V1 import build_product_payload

PROTECTED_SHOPIFY_FIELDS = (
    "handle", "sku", "variants", "options", "inventory_quantity",
    "inventory_management", "inventory_policy", "price", "compare_at_price",
)

def build_preview(record: Dict[str, Any]) -> Dict[str, Any]:
    """Return the proposed payload plus explicit protected-field guarantees."""
    payload = build_product_payload(deepcopy(record))
    return {
        "operation": "UPDATE_PRODUCT_EDITORIAL",
        "product_id": payload["id"],
        "proposed_updates": {key: value for key, value in payload.items() if key != "id"},
        "protected_fields": list(PROTECTED_SHOPIFY_FIELDS),
        "authorization_required": True,
        "live_write_performed": False,
    }

__all__ = ["PROTECTED_SHOPIFY_FIELDS", "build_preview"]