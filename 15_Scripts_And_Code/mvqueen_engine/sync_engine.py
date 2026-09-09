"""Legacy sync compatibility shim.

The former implementation could create/update products, mutate metafields,
upload images, and auto-publish through an arbitrary adapter. That behavior is
not permitted in the enterprise production architecture.

Use the canonical production readiness pipeline, release gate, publishing
boundary, and Shopify publisher instead.
"""
from __future__ import annotations
from typing import Any, Dict


class LegacySyncEngineDisabled(RuntimeError):
    """Raised when the retired direct Shopify sync path is invoked."""


def sync_to_shopify(product: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    raise LegacySyncEngineDisabled(
        "Legacy sync_to_shopify is disabled. Use the canonical production "
        "release gate and publishing boundary."
    )


def _build_shopify_payload(product: Dict[str, Any], sync_engine: Dict[str, Any]) -> Dict[str, Any]:
    raise LegacySyncEngineDisabled(
        "Legacy Shopify payload construction is disabled outside the canonical publisher."
    )


def _build_tags(product: Dict[str, Any]) -> str:
    raise LegacySyncEngineDisabled(
        "Legacy Shopify tag construction is disabled outside the canonical publisher."
    )
