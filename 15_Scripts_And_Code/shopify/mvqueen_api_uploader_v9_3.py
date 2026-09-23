"""Legacy Shopify uploader quarantine.

This module is retained for historical compatibility only. The former v9.3
implementation performed direct Shopify mutations and could bypass the
canonical production, QA, approval, and publishing gates.

Use the canonical path instead:
RAW -> ... -> PRODUCTION_READY -> APPROVED_FOR_PUBLISH ->
PUBLISHING_BOUNDARY_V1 -> SHOPIFY_PUBLISHER_V1

No live Shopify operation is performed here.
"""
from __future__ import annotations


class LegacyShopifyUploaderDisabled(RuntimeError):
    """Raised whenever the retired direct uploader is invoked."""


def main() -> None:
    raise LegacyShopifyUploaderDisabled(
        "Legacy v9.3 direct Shopify uploader is disabled. "
        "Use PRODUCTION_READINESS/PUBLISHING_BOUNDARY_V1.py and "
        "SHOPIFY_PUBLISHER_V1.py after explicit approval."
    )


if __name__ == "__main__":
    main()
