"""Retired Shopify API compatibility surface.

Production Shopify writes MUST use the canonical path:
PRODUCT_PIPELINE_V1 -> QA -> RELEASE_GATE_V1 -> PUBLISHING_BOUNDARY_V1
-> SHOPIFY_PUBLISHER_V1.

The former ShopifyAPI exposed create, update, metafield, and collection
mutation methods outside the release gate. It is intentionally disabled so
legacy callers fail closed rather than reporting simulated success.
"""
from __future__ import annotations

from typing import Any, Dict


class LegacyShopifyAPIDisabled(RuntimeError):
    """Raised when a retired Shopify API mutation surface is invoked."""


class ShopifyAPI:
    """Compatibility shim for the retired pre-release-gate API wrapper."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._disabled = True

    @staticmethod
    def _blocked(operation: str) -> None:
        raise LegacyShopifyAPIDisabled(
            f"Legacy ShopifyAPI operation '{operation}' is disabled. "
            "Use the canonical release gate, publishing boundary, and "
            "SHOPIFY_PUBLISHER_V1.py."
        )

    def create_product(self, data: Dict[str, Any]) -> None:
        return self._blocked("create_product")

    def update_product(self, product_id: str, data: Dict[str, Any]) -> None:
        return self._blocked("update_product")

    def update_metafields(self, product_id: str, metafields: Dict[str, Any]) -> None:
        return self._blocked("update_metafields")

    def assign_to_collection(self, product_id: str, collection_id: str) -> None:
        return self._blocked("assign_to_collection")


__all__ = ["ShopifyAPI", "LegacyShopifyAPIDisabled"]
