# shopify/collections_api.py
"""
MVQueen Shopify Collection Sync
-------------------------------

Assigns products to Shopify collections using the safe ShopifyAPI wrapper.

Collections come from:
- catalog_processor/collection.py
"""

from typing import List
from shopify.api import ShopifyAPI


def sync_collections(product_id: str, collections: List[str]) -> List[dict]:
    """
    Assigns a product to multiple Shopify collections.

    Args:
        product_id: Shopify product ID
        collections: List of collection handles or IDs

    Returns:
        List of Shopify API responses.
    """

    api = ShopifyAPI()
    responses = []

    for collection in collections:
        resp = api.assign_to_collection(product_id, collection)
        responses.append(resp)

    return responses


__all__ = ["sync_collections"]