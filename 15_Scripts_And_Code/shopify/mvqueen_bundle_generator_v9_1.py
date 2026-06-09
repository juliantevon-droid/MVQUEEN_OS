
# ============================================================
# MVQUEEN OMNILUXE SUPREME v9.1
# BUNDLE GENERATION ENGINE
# ============================================================

import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib
import math

# ============================================================
# CONFIG
# ============================================================

BRAND_NAME = "MVQueen"
DISCOUNT_RATE = 0.15
EXPORT_DIR = Path.cwd() / "MVQ_Exports"
DATE_STAMP = datetime.now().strftime("%Y-%m-%d")

# ============================================================
# LOAD OPTIMIZED CATALOG (PART 1 IS ENOUGH)
# ============================================================

optimized_file = list(EXPORT_DIR.glob(f"{BRAND_NAME}Optimized_Part1_*.csv"))[0]
df = pd.read_csv(optimized_file)

# ============================================================
# FILTER BUNDLE-SAFE PRODUCTS
# ============================================================

bundle_safe_df = df[df["metafield.custom.shopify_bundle_safe"] == "true"]

# ============================================================
# GROUP BY COLLECTION + INTENT
# ============================================================

groups = bundle_safe_df.groupby(
    ["metafield.custom.collection", "metafield.custom.intent"]
)

bundle_rows = []

def generate_handle(a, b):
    base = f"bundle-{a}-{b}"
    return hashlib.md5(base.encode()).hexdigest()[:12]

# ============================================================
# CREATE BUNDLES
# ============================================================

for (_, _), group in groups:
    group = group.reset_index(drop=True)
    for i in range(0, len(group) - 1, 2):
        p1 = group.iloc[i]
        p2 = group.iloc[i + 1]

        price_sum = float(p1["Variant Price"]) + float(p2["Variant Price"])
        bundle_price = round(price_sum * (1 - DISCOUNT_RATE), 2)
        compare_at = round(price_sum, 2)

        bundle_title = f"{p1['Title']} + {p2['Title']} Bundle | {BRAND_NAME}"
        bundle_handle = generate_handle(p1["Handle"], p2["Handle"])

        body_html_template = """
                <p>Exclusive {BRAND_NAME} bundle featuring:</p>
                <ul>
                    <li>{p1_title}</li>
                    <li>{p2_title}</li>
                </ul>
                <p>Luxury value with exclusive bundle savings.</p>
            """
        formatted_body_html = body_html_template.format(
            BRAND_NAME=BRAND_NAME,
            p1_title=p1['Title'],
            p2_title=p2['Title']
        )

        bundle_rows.append({
            "Handle": bundle_handle,
            "Title": bundle_title,
            "Body (HTML)": formatted_body_html,
            "Vendor": BRAND_NAME,
            "Tags": f"bundle,{p1['Tags']},{p2['Tags']}",
            "Variant Price": bundle_price,
            "Variant Compare At Price": compare_at,
            "SEO Title": bundle_title[:60],
            "SEO Description": f"Luxury bundle by {BRAND_NAME}. Premium products paired for elevated results."[:155],
            "Image Alt Text": bundle_title,
            "metafield.custom.voice": "luxury-modern-elegant",
            "metafield.custom.intent": p1["metafield.custom.intent"],
            "metafield.custom.collection": p1["metafield.custom.collection"],
            "metafield.custom.prestige_score": max(
                p1["metafield.custom.prestige_score"],
                p2["metafield.custom.prestige_score"]
            ),
            "metafield.custom.product_quality_score": round(
                (p1["metafield.custom.product_quality_score"] +
                 p2["metafield.custom.product_quality_score"]) / 2, 1
            ),
            "metafield.custom.shopify_bundle_safe": "true"
        })

# ============================================================
# EXPORT BUNDLES
# ============================================================

bundle_df = pd.DataFrame(bundle_rows)

bundle_path = EXPORT_DIR / f"{BRAND_NAME}Bundles{DATE_STAMP}.csv"
bundle_df.to_csv(bundle_path, index=False)

print(f"✅ {len(bundle_df)} bundles generated safely")
