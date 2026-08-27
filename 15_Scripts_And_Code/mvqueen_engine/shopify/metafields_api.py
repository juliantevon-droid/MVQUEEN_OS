"""Shopify Admin API metafield synchronization."""
from __future__ import annotations
from typing import Any, Iterable, Mapping
from .api import ShopifyClient


def upsert_product_metafields(client: ShopifyClient, product_id: int, metafields: Iterable[Mapping[str, Any]], *, allow_write: bool = False) -> list[dict[str, Any]]:
    """Create/update product metafields through the GraphQL-safe REST endpoint.

    Writes remain disabled unless both the client is non-dry-run and the caller
    explicitly opts in.
    """
    results = []
    original = client.dry_run
    client.dry_run = not allow_write
    try:
        for item in metafields:
            namespace = str(item.get("namespace", "custom")).strip()
            key = str(item.get("key", "")).strip()
            value = item.get("value")
            type_ = str(item.get("type", "single_line_text_field")).strip()
            if not key or value is None or str(value).strip() == "":
                results.append({"ok": False, "error": "namespace, key and non-empty value required"})
                continue
            payload = {"metafield": {"namespace": namespace, "key": key, "type": type_, "value": str(value)}}
            result = client.write("POST", f"/products/{int(product_id)}/metafields.json", payload)
            results.append({"ok": True, "key": f"{namespace}.{key}", "result": result})
    finally:
        client.dry_run = original
    return results
