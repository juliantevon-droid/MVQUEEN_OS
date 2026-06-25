
# ============================================================
# MVQUEEN OMNILUXE SUPREME v9.3
# SHOPIFY ADMIN API UPLOADER (SAFE MODE)
# ============================================================

import pandas as pd
import requests
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# CONFIG - LOAD FROM ENVIRONMENT
# ============================================================

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

SHOP_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "mvqueen.myshopify.com")
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-10")
ADMIN_API_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN", "REPLACE_WITH_ENV_VAR")

DRY_RUN = True   # <- SET TO False ONLY WHEN READY
SLEEP_SECONDS = 0.5

EXPORT_DIR = Path.cwd() / "MVQ_Exports"

# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "X-Shopify-Access-Token": ADMIN_API_TOKEN,
    "Content-Type": "application/json"
}

# ============================================================
# LOAD ALL OPTIMIZED CSV PARTS
# ============================================================

csv_files = sorted(EXPORT_DIR.glob("MVQueenOptimized_Part*.csv"))
df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# ============================================================
# FETCH PRODUCT ID MAP (HANDLE -> ID)
# ============================================================

def fetch_all_products():
    products = {}
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/products.json?limit=250"
    while url:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()["products"]
        for p in data:
            products[p["handle"]] = p["id"]
        url = r.links.get("next", {}).get("url")
    return products

# NOTE: This API call is commented out for safety in DRY_RUN mode.
# Uncomment and ensure ADMIN_API_TOKEN is set before live runs.
# product_id_map = fetch_all_products()
product_id_map = {} # Placeholder for DRY_RUN

# ============================================================
# UPDATE PRODUCTS
# ============================================================

for idx, row in df.iterrows():
    handle = row["Handle"]

    # if handle not in product_id_map:
    #     print(f"WARNING Skipping missing product: {handle}")
    #     continue

    # product_id = product_id_map[handle]
    product_id = f"dummy_id_{idx}" # Placeholder for DRY_RUN

    product_payload = {
        "product": {
            "id": product_id,
            "title": row["Title"],
            "body_html": row["Body (HTML)"],
            "tags": row["Tags"],
            "metafields_global_title_tag": row["SEO Title"],
            "metafields_global_description_tag": row["SEO Description"]
        }
    }

    # ---------- METAFIELDS ----------
    metafields = []
    for col in row.index:
        if col.startswith("metafield.custom.") and str(row[col]).strip():
            key = col.replace("metafield.custom.", "")
            metafields.append({
                "namespace": "custom",
                "key": key,
                "type": "single_line_text_field",
                "value": str(row[col])
            })

    if metafields:
        product_payload["product"]["metafields"] = metafields

    if DRY_RUN:
        print(f"INFO DRY RUN -> Would update {handle}")
        continue

    try:
        r = requests.put(
            f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/products/{product_id}.json",
            headers=HEADERS,
            json=product_payload
        )
        r.raise_for_status()
        print(f"SUCCESS Updated {handle}")
    except Exception as e:
        print(f"ERROR Failed {handle}: {e}")

    time.sleep(SLEEP_SECONDS)

print("API upload complete")
