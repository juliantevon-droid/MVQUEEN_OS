"""Retired Shopify collection mutation entry point.

Collection assignment is derived by the canonical merchandising stage and may
only be applied through the approved production publisher architecture.
"""
from __future__ import annotations

from typing import List


class LegacyCollectionSyncDisabled(RuntimeError):
    """Raised when the retired collection mutation path is invoked."""


def sync_collections(product_id: str, collections: List[str]) -> None:
    raise LegacyCollectionSyncDisabled(
        "Legacy collection sync is disabled on the enterprise production branch. "
        "Use the canonical release path and approved Shopify publisher."
    )


__all__ = ["sync_collections", "LegacyCollectionSyncDisabled"]
