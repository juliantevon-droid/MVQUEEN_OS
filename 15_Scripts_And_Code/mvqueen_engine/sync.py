"""Legacy Shopify sync compatibility shim.

Production Shopify writes MUST use the canonical path:
PRODUCT_PIPELINE_V1 -> QA -> RELEASE_GATE_V1 -> PUBLISHING_BOUNDARY_V1
-> SHOPIFY_PUBLISHER_V1.

The former sync implementation could create products, mutate variants/prices,
write metafields, create collections, and assign products to collections. It is
intentionally disabled here so legacy callers fail closed instead of bypassing
production controls.
"""
from __future__ import annotations


class LegacyShopifySyncDisabled(RuntimeError):
    """Raised when a legacy Shopify sync path is invoked."""


class ShopifySync:
    """Compatibility surface for the retired direct Shopify sync engine."""

    def __init__(self, *args, **kwargs):
        self.shop_url = kwargs.get("shop_url")
        self.api_version = kwargs.get("api_version", "2024-01")
        self.vendor = kwargs.get("vendor", "MVQueen")

    @staticmethod
    def _blocked(operation: str):
        raise LegacyShopifySyncDisabled(
            f"Legacy Shopify operation '{operation}' is disabled. "
            "Use the canonical production release gate and publisher."
        )

    def _request(self, *args, **kwargs):
        return self._blocked("raw_request")

    def create_product(self, *args, **kwargs):
        return self._blocked("create_product")

    def update_metafields(self, *args, **kwargs):
        return self._blocked("update_metafields")

    def add_to_collections(self, *args, **kwargs):
        return self._blocked("add_to_collections")

    def _ensure_collection(self, *args, **kwargs):
        return self._blocked("ensure_collection")

    def sync_product(self, *args, **kwargs):
        return self._blocked("sync_product")
