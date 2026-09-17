"""Retired Shopify metafield mutation entry point.

Metafields are part of the canonical production record but this legacy module
must not mutate Shopify directly. Publication is handled by the approved
publisher path only.
"""
from __future__ import annotations

from typing import Any, Dict


class LegacyMetafieldSyncDisabled(RuntimeError):
    """Raised when the retired metafield mutation path is invoked."""


def sync_metafields(product_id: str, metafields: Dict[str, Any]) -> None:
    raise LegacyMetafieldSyncDisabled(
        "Legacy metafield sync is disabled on the enterprise production branch. "
        "Use the canonical release path and approved Shopify publisher."
    )


__all__ = ["sync_metafields", "LegacyMetafieldSyncDisabled"]
