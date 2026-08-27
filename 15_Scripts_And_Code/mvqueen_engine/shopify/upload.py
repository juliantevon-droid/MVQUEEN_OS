"""High-level Shopify upload orchestration.

This module deliberately defaults to dry-run. It consumes already-normalized
product payloads and delegates transport/security to ShopifyClient.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping
from .api import ShopifyClient
from .update import update_product


def upload_products(client: ShopifyClient, products: Iterable[Mapping[str, Any]], *, allow_write: bool = False) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for product in products:
        if "id" not in product:
            results.append({"ok": False, "error": "product id is required"})
            continue
        try:
            original = client.dry_run
            client.dry_run = not allow_write
            result = update_product(client, int(product["id"]), product)
            client.dry_run = original
            results.append({"ok": True, "result": result})
        except Exception as exc:
            client.dry_run = original if 'original' in locals() else client.dry_run
            results.append({"ok": False, "error": str(exc), "id": product.get("id")})
    return results
