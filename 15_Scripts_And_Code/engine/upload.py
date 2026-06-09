# shopify/upload.py
"""
MVQueen Shopify Upload Pipeline
-------------------------------

Takes a fully processed MVQueen product package and uploads it
to Shopify using the safe ShopifyAPI wrapper.

This includes:
- Title
- Description
- Tags
- Collections
- Metafields
"""

from typing import Dict, Any
from shopify.api import ShopifyAPI


def upload_product(package: Dict[str, Any]) -> Dict[str, Any]:
    """
    Uploads a processed product package to Shopify.

    Args:
        package: The full MVQueen product package:
            {
                "raw": {...},
                "profile": {...},
                "editorial": {...},
                "metafields": {...},
                "tags": [...],
                "collections": [...]
            }

    Returns:
        Dict with Shopify API response.
    """

    api = ShopifyAPI()

    # Build Shopify product payload
    payload = {
        "title": package["raw"].get("title", ""),
        "body_html": package["editorial"].get("description", ""),
        "tags": ", ".join(package.get("tags", [])),
        "metafields": package.get("metafields", {}),
    }

    # Create product
    response = api.create_product(payload)

    return {
        "upload_response": response,
        "payload": payload,
    }


__all__ = ["upload_product"]