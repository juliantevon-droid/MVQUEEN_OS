"""Legacy Shopify update entry point disabled on the enterprise branch.

Production writes must pass through the canonical product pipeline, release gate,
publishing boundary, and dedicated Shopify publisher.
"""
from __future__ import annotations

from typing import Any, Dict


def update_product(product_id: str, package: Dict[str, Any]) -> Dict[str, Any]:
    """Fail closed to prevent legacy package-shaped writes from bypassing QA."""
    raise RuntimeError(
        "Legacy Shopify update.py is disabled on the enterprise production branch. "
        "Use the canonical release path and SHOPIFY_PUBLISHER_V1.py."
    )


__all__ = ["update_product"]
