
# ============================================================
# MVQUEEN OMNILUXE SUPREME v9.2
# COLLECTIONS OPTIMIZER
# ============================================================

import pandas as pd
from pathlib import Path
from datetime import datetime
import re
import hashlib

# ============================================================
# CONFIG
# ============================================================

BRAND_NAME = "MVQueen"
EXPORT_DIR = Path.cwd() / "MVQ_Exports"
DATE_STAMP = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# LOAD OPTIMIZED PRODUCTS (PART 1 IS ENOUGH)
# ============================================================

product_file = list(EXPORT_DIR.glob(f"{BRAND_NAME}Optimized_Part1_*.csv"))[0]
df = pd.read_csv(product_file)

# ============================================================
# COLLECTION UTILITIES
# ============================================================

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def collection_row(handle, title, rule_column, rule_condition):
    seo_title = title[:60]
    seo_desc = f"Discover {title} by {BRAND_NAME}. Curated luxury products designed for elevated performance."[:155]

    return {
        "Handle": handle,
        "Title": title,
        "Body (HTML)": f"<p>{seo_desc}</p>",
        "Sort Order": "best-selling",
        "Template Suffix": "",
        "Published": "TRUE",
        "Rule: Column": rule_column,
        "Rule: Relation": "equals",
        "Rule: Condition": rule_condition,
        "SEO Title": seo_title,
        "SEO Description": seo_desc,
        "metafield.custom.voice": "luxury-modern-elegant",
        "metafield.custom.search_priority": 3
    }

# ============================================================
# BUILD COLLECTIONS
# ============================================================

collections = []

# ---------- CORE COLLECTIONS ----------

for value in df["metafield.custom.collection"].dropna().unique():
    title = f"{value.title()} Collection"
    collections.append(
        collection_row(
            slugify(title),
            title,
            "Product metafield: custom.collection",
            value
        )
    )

# ---------- INTENT COLLECTIONS ----------

for intent in df["metafield.custom.intent"].dropna().unique():
    title = f"{intent.title()} Picks"
    collections.append(
        collection_row(
            slugify(title),
            title,
            "Product metafield: custom.intent",
            intent
        )
    )

# ---------- SEASONAL COLLECTIONS ----------
# Check if 'metafield.custom.seasonality' column exists before processing
if "metafield.custom.seasonality" in df.columns:
    for season in df["metafield.custom.seasonality"].dropna().unique():
        title = f"{season.title()} Edit"
        collections.append(
            collection_row(
                slugify(title),
                title,
                "Product metafield: custom.seasonality",
                season
            )
        )
else:
    print("Skipping seasonal collections as 'metafield.custom.seasonality' column is missing.")

# ---------- PRESTIGE COLLECTIONS ----------

prestige_threshold = 9
title = "Signature Luxury"
collections.append(
    collection_row(
        slugify(title),
        title,
        "Product metafield: custom.prestige_score",
        prestige_threshold
    )
)

# ============================================================
# EXPORT COLLECTIONS
# ============================================================

collections_df = pd.DataFrame(collections)

collection_path = EXPORT_DIR / f"{BRAND_NAME}Collections{DATE_STAMP}.csv"
collections_df.to_csv(collection_path, index=False)

print(f"✅ {len(collections_df)} collections generated safely")
