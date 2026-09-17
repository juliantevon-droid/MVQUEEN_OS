"""Retired Shopify upload entry point.

Legacy package-shaped uploads are intentionally disabled. A product may only
reach Shopify through the canonical production record, QA gate, explicit
publish approval, publishing boundary, and dedicated Shopify publisher.
"""
from __future__ import annotations

from typing import Any, Dict


class LegacyShopifyUploadDisabled(RuntimeError):
    """Raised when the retired package upload path is invoked."""


def upload_product(package: Dict[str, Any]) -> None:
    """Fail closed so package-shaped data cannot bypass production controls."""
    raise LegacyShopifyUploadDisabled(
        "Legacy upload.py is disabled on the enterprise production branch. "
        "Use the canonical release path and SHOPIFY_PUBLISHER_V1.py."
    )


__all__ = ["upload_product", "LegacyShopifyUploadDisabled"]
