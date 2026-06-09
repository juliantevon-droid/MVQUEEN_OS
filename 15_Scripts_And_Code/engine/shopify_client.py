# mvqueen_engine/shopify_api/shopify_client.py
"""
PHASE 3 — SHOPIFY API ENGINE

Handles:
- GET all products
- GET single product
- UPDATE product
- UPDATE metafields
- Safe variant handling
- Rate limit handling
- Retry logic
- Logging hooks

This is the backbone of Phase 4 (Catalog Processor) and Phase 5 (Control Panel).
"""

import time
import json
import requests

from mvqueen_engine.config import (
    SHOPIFY_BASE_URL,
    SHOPIFY_ACCESS_TOKEN,
    DEBUG,
)


# ---------------------------------------------
# INTERNAL REQUEST WRAPPER
# ---------------------------------------------

def _shopify_request(method: str, endpoint: str, payload=None, retries=3):
    """
    Safe Shopify request wrapper with:
    - retries
    - rate limit handling
    - JSON safety
    - debug logging
    """

    url = f"{SHOPIFY_BASE_URL}/{endpoint}"

    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    }

    for attempt in range(1, retries + 1):
        try:
            if DEBUG:
                print(f"[SHOPIFY] {method} {url}")

            if method == "GET":
                response = requests.get(url, headers=headers)
            else:
                response = requests.request(method, url, headers=headers, data=json.dumps(payload or {}))

            # Rate limit handling
            if response.status_code == 429:
                if DEBUG:
                    print("[SHOPIFY] Rate limit hit. Retrying in 2 seconds...")
                time.sleep(2)
                continue

            # Success
            if response.status_code in (200, 201):
                return response.json()

            # Other errors
            if DEBUG:
                print(f"[SHOPIFY] Error {response.status_code}: {response.text}")

        except Exception as e:
            if DEBUG:
                print(f"[SHOPIFY] Exception: {e}")

        # Retry delay
        time.sleep(1)

    return None


# ---------------------------------------------
# GET ALL PRODUCTS
# ---------------------------------------------

def get_all_products(limit=250):
    """
    Fetch all products from Shopify.
    Handles pagination automatically.
    """

    products = []
    page_info = None

    while True:
        endpoint = f"products.json?limit={limit}"
        if page_info:
            endpoint += f"&page_info={page_info}"

        data = _shopify_request("GET", endpoint)
        if not data or "products" not in data:
            break

        products.extend(data["products"])

        # Pagination
        link_header = data.get("link")
        if not link_header:
            break

        # Shopify REST pagination uses page_info
        if "page_info=" not in link_header:
            break

        page_info = link_header.split("page_info=")[-1].split(">")[0]

    return products


# ---------------------------------------------
# GET SINGLE PRODUCT
# ---------------------------------------------

def get_product(product_id: str):
    endpoint = f"products/{product_id}.json"
    data = _shopify_request("GET", endpoint)
    return data.get("product") if data else None


# ---------------------------------------------
# UPDATE PRODUCT
# ---------------------------------------------

def update_product(product_id: str, updates: dict):
    """
    Updates product fields:
    - title
    - body_html
    - tags
    - vendor
    - product_type
    - etc.
    """

    payload = {"product": {"id": product_id, **updates}}
    endpoint = f"products/{product_id}.json"
    return _shopify_request("PUT", endpoint, payload)


# ---------------------------------------------
# UPDATE METAFIELDS
# ---------------------------------------------

def update_metafields(product_id: str, metafields: dict):
    """
    Writes metafields to Shopify.
    Always overwrites (Mode A).
    """

    results = {}

    for key, value in metafields.items():
        namespace, name = key.split(".", 1)

        payload = {
            "metafield": {
                "namespace": namespace,
                "key": name,
                "value": value,
                "type": "single_line_text_field",
            }
        }

        endpoint = f"products/{product_id}/metafields.json"
        result = _shopify_request("POST", endpoint, payload)
        results[key] = result

    return results


# ---------------------------------------------
# UPDATE VARIANT PRICES
# ---------------------------------------------

def update_variant_price(variant_id: str, price: float, compare_at_price: float = None):
    payload = {
        "variant": {
            "id": variant_id,
            "price": str(price),
        }
    }

    if compare_at_price:
        payload["variant"]["compare_at_price"] = str(compare_at_price)

    endpoint = f"variants/{variant_id}.json"
    return _shopify_request("PUT", endpoint, payload)