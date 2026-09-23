"""Legacy Shopify updater disabled on the enterprise production branch.

Use the canonical production pipeline, release gate, publishing boundary, and
`PRODUCTION_READINESS/SHOPIFY_PUBLISHER_V1.py` instead.
"""
from __future__ import annotations


class ProductUpdater:
    """Compatibility shim that fails closed instead of bypassing release controls."""

    def __init__(self, *args, **kwargs):
        self._disabled = True

    def update_product(self, *args, **kwargs):
        raise RuntimeError(
            "Direct Shopify updates from product_updater.py are disabled on the "
            "enterprise production branch. Use the canonical release path."
        )

    def upsert_by_handle(self, *args, **kwargs):
        raise RuntimeError(
            "Handle-based Shopify upserts are disabled on the enterprise production branch. "
            "Use an approved canonical release through the publishing boundary."
        )


__all__ = ["ProductUpdater"]
