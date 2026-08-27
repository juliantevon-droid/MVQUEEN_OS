"""Controlled product update operations."""
from __future__ import annotations
from typing import Any, Mapping
from .api import ShopifyClient


def build_product_payload(product_id: int, data: Mapping[str, Any]) -> dict[str, Any]:
    product: dict[str, Any] = {"id": product_id}
    mapping = {
        "title": "title", "body_html": "body_html", "vendor": "vendor",
        "product_type": "product_type", "tags": "tags",
        "seo_title": "metafields_global_title_tag",
        "seo_description": "metafields_global_description_tag",
    }
    for source, target in mapping.items():
        if data.get(source) is not None and str(data.get(source)).strip():
            product[target] = data[source]
    return {"product": product}


def update_product(client: ShopifyClient, product_id: int, data: Mapping[str, Any]) -> dict[str, Any]:
    return client.write("PUT", f"/products/{product_id}.json", build_product_payload(product_id, data))
