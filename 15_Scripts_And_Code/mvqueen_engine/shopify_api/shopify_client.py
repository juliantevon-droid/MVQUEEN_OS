import requests
import time
from ..config import SHOPIFY_BASE_URL, SHOPIFY_ACCESS_TOKEN

def get_all_products():
    """Fetch all products from Shopify Admin API."""
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
    response = requests.get(f"{SHOPIFY_BASE_URL}/products.json", headers=headers)
    if response.status_code == 200:
        return response.json().get("products", [])
    else:
        print(f"Error fetching products: {response.status_code}")
        return []

def update_product(product_id, data):
    """Update a product in Shopify."""
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
    url = f"{SHOPIFY_BASE_URL}/products/{product_id}.json"
    response = requests.put(url, json={"product": data}, headers=headers)
    return response.status_code == 200

def update_metafields(product_id, metafields):
    """Update metafields for a product."""
    # Simplified implementation
    pass

def update_variant_price(variant_id, price, compare_at):
    """Update the price of a product variant."""
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
    url = f"{SHOPIFY_BASE_URL}/variants/{variant_id}.json"
    data = {"variant": {"id": variant_id, "price": price, "compare_at_price": compare_at}}
    response = requests.put(url, json=data, headers=headers)
    return response.status_code == 200
