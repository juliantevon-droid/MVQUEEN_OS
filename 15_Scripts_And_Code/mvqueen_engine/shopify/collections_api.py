"""Controlled Shopify collection operations."""
from __future__ import annotations
from typing import Any, Mapping
from .api import ShopifyClient


def build_collection_payload(data: Mapping[str, Any]) -> dict[str, Any]:
    collection: dict[str, Any] = {}
    for key in ("title", "body_html", "handle", "sort_order", "template_suffix", "published"):
        if data.get(key) is not None and str(data.get(key)).strip() != "":
            collection[key] = data[key]
    return {"custom_collection": collection}


def create_collection(client: ShopifyClient, data: Mapping[str, Any], *, allow_write: bool = False) -> dict[str, Any]:
    original = client.dry_run
    client.dry_run = not allow_write
    try:
        return client.write("POST", "/custom_collections.json", build_collection_payload(data))
    finally:
        client.dry_run = original


def update_collection(client: ShopifyClient, collection_id: int, data: Mapping[str, Any], *, allow_write: bool = False) -> dict[str, Any]:
    original = client.dry_run
    client.dry_run = not allow_write
    try:
        return client.write("PUT", f"/custom_collections/{int(collection_id)}.json", build_collection_payload(data))
    finally:
        client.dry_run = original
