# ============================================================
# BLOCK 39 — SYNC ENGINE (FINAL VERSION)
# ============================================================

from __future__ import annotations
from typing import Dict, Any, Optional

from engine.engine_core import (
    get_engine,
    sanitize_text,
)


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def sync_to_shopify(product: Dict[str, Any], adapter) -> Dict[str, Any]:
    """
    Syncs a fully processed MVQueen product to Shopify using the provided adapter.

    adapter must implement:
        - create_product(payload)
        - update_product(product_id, payload)
        - upsert_metafields(product_id, metafields)
        - upload_images(product_id, images)
        - publish_product(product_id)

    Returns:
        {
            "success": bool,
            "product_id": str | None,
            "errors": list
        }
    """

    sync_engine = get_engine("sync") or {}
    errors = []

    # 1. Build Shopify payload
    payload = _build_shopify_payload(product, sync_engine)

    # 2. Create or update
    product_id = product.get("shopify_id")

    try:
        if product_id:
            result = adapter.update_product(product_id, payload)
        else:
            result = adapter.create_product(payload)
            product_id = result.get("id")

    except Exception as e:
        return {
            "success": False,
            "product_id": None,
            "errors": [f"Product sync failed: {str(e)}"],
        }

    # 3. Sync metafields
    try:
        metafields = product.get("metafields", {})
        adapter.upsert_metafields(product_id, metafields)
    except Exception as e:
        errors.append(f"Metafield sync failed: {str(e)}")

    # 4. Sync images
    try:
        images = product.get("images", [])
        if images:
            adapter.upload_images(product_id, images)
    except Exception as e:
        errors.append(f"Image sync failed: {str(e)}")

    # 5. Publish product
    try:
        if sync_engine.get("auto_publish", True):
            adapter.publish_product(product_id)
    except Exception as e:
        errors.append(f"Publish failed: {str(e)}")

    return {
        "success": len(errors) == 0,
        "product_id": product_id,
        "errors": errors,
    }


# ------------------------------------------------------------
# PAYLOAD BUILDER
# ------------------------------------------------------------

def _build_shopify_payload(product: Dict[str, Any], sync_engine: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts MVQueen product into Shopify's product payload structure.
    """

    title = sanitize_text(product.get("title", ""))
    handle = sanitize_text(product.get("handle", ""))
    body_html = product.get("editorial_html", "")

    seo = product.get("seo", {})
    price = product.get("price")
    compare_at = product.get("compare_at_price")

    payload = {
        "title": title,
        "handle": handle,
        "body_html": body_html,
        "status": "active" if sync_engine.get("auto_publish", True) else "draft",
        "variants": [
            {
                "price": price,
                "compare_at_price": compare_at,
                "sku": product.get("sku", ""),
                "barcode": product.get("barcode", ""),
                "inventory_quantity": product.get("inventory", 0),
            }
        ],
        "tags": _build_tags(product),
        "product_type": product.get("category", ""),
        "vendor": product.get("brand", ""),
        "metafields_global_title_tag": seo.get("seo_title", ""),
        "metafields_global_description_tag": seo.get("meta_description", ""),
    }

    return payload


# ------------------------------------------------------------
# TAG BUILDER
# ------------------------------------------------------------

def _build_tags(product: Dict[str, Any]) -> str:
    tags = []

    # Persona tags
    if product.get("persona"):
        tags.append(f"persona:{product['persona']}")

    # Category tags
    if product.get("category"):
        tags.append(f"category:{product['category']}")

    # Price tags
    tags.extend(product.get("price_tags", []))

    # Image tags
    image_data = product.get("image_data", {})
    tags.extend(image_data.get("image_tags", []))

    # Deduplicate + join
    tags = list(set(tags))
    return ", ".join(tags)