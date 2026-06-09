# shopify/update.py
"""
MVQueen Shopify Update Pipeline
-------------------------------

Updates an existing Shopify product using the safe ShopifyAPI wrapper.

Supports updating:
- Title
- Description
- Tags
- Metafields
"""

from typing import Dict, Any
from shopify.api import ShopifyAPI


def update_product(product_id: str, package: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates a Shopify product with new MVQueen data.

    Args:
        product_id: Shopify product ID
        package: MVQueen product package

    Returns:
        Dict with Shopify API response.
    """

    api = ShopifyAPI()

    payload = {
        "title": package["raw"].get("title", ""),
        "body_html": package["editorial"].get("description", ""),
        "tags": ", ".join(package.get("tags", [])),
        "metafields": package.get("metafields", {}),
    }

    response = api.update_product(product_id, payload)

    return {
        "update_response": response,
        "payload": payload,
    }


__all__ = ["update_product"]