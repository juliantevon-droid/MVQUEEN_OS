# mvqueen_engine/config.py
"""
PHASE 0 — CONFIG

Global configuration for MVQueen Engine:
- Shopify API settings
- General engine settings
- Safety toggles
"""

import os

# -----------------------------
# SHOPIFY CONFIG
# -----------------------------

SHOPIFY_STORE_DOMAIN = "mvqueen.myshopify.com"
SHOPIFY_API_VERSION = "2024-01"
SHOPIFY_ACCESS_TOKEN = "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"

SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"

# -----------------------------
# ENGINE SETTINGS
# -----------------------------

BRAND_NAME = "MVQueen"

# Max rows per CSV chunk when exporting
CSV_CHUNK_SIZE = 15000

# Whether to log debug info to console
DEBUG = True

# -----------------------------
# SAFETY / PROTECTION
# -----------------------------

# Columns we NEVER touch in CSV workflows
SHOPIFY_PROTECTED_COLUMNS = [
    "Handle","Product ID","Variant ID",
    "Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value",
    "Variant SKU","Variant Grams","Variant Inventory Tracker","Variant Inventory Qty",
    "Variant Inventory Policy","Variant Fulfillment Service","Variant Requires Shipping",
    "Variant Taxable","Image Position","Gift Card","Variant Weight Unit"
]