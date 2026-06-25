# ============================================================
# MVQueen — Phase 1 CSV Loader/Writer
# ============================================================

import csv
import json
from mvqueen_engine.runtime import run_mvqueen


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

INPUT_CSV = "products.csv"
OUTPUT_CSV = "mvqueen_output.csv"

# Fields MVQueen should NOT overwrite
PRESERVE_FIELDS = {
    "Handle",
    "Variant Price",
    "Vendor",
    "Published"
}

# Image fields to merge
IMAGE_FIELDS = ["Image Src", "Variant Image"]


# ------------------------------------------------------------
# LOAD CSV ROW → PRODUCT DICT
# ------------------------------------------------------------

def row_to_product(row: dict) -> dict:
    """
    Convert a Shopify CSV row into a product dict for MVQueen.
    """

    # Merge images from AF + CB
    images = []
    for field in IMAGE_FIELDS:
        if row.get(field):
            images.append(row[field])

    product = {
        "title": row.get("Title", ""),
        "brand": row.get("Vendor", ""),
        "category": row.get("Product Category", "") or row.get("Type", ""),
        "persona": row.get("Tags", ""),  # You can change this if persona is elsewhere
        "images": images,
        "sku": row.get("Variant SKU", ""),
        "barcode": row.get("Variant Barcode", ""),
        "inventory": row.get("Variant Inventory Tracker", 0),
        "handle": row.get("Handle", ""),
        "price": float(row.get("Variant Price", 0) or 0),
        "compare_at_price": float(row.get("Variant Compare At Price", 0) or 0),
    }

    return product


# ------------------------------------------------------------
# APPLY MVQUEEN OUTPUT → CSV ROW
# ------------------------------------------------------------

def apply_mvqueen_to_row(row: dict, enriched: dict) -> dict:
    """
    Write MVQueen output back into the CSV row,
    preserving Handle, Variant Price, Vendor, Published.
    """

    # Title
    row["Title"] = enriched.get("title", row.get("Title"))

    # Body HTML
    row["Body (HTML)"] = enriched.get("editorial_html", "")

    # Tags
    tags = []
    tags.extend(enriched.get("price_tags", []))
    image_data = enriched.get("image_data", {})
    tags.extend(image_data.get("image_tags", []))
    row["Tags"] = ", ".join(sorted(set(tags)))

    # SEO
    seo = enriched.get("seo", {})
    row["SEO Title"] = seo.get("seo_title", "")
    row["SEO Description"] = seo.get("meta_description", "")

    # Image Alt Text
    row["Image Alt Text"] = image_data.get("alt_text", "")

    # Compare At Price
    row["Variant Compare At Price"] = enriched.get("compare_at_price", "")

    # Metafields (custom)
    metafields = enriched.get("metafields", {})

    # Flatten metafields into CSV columns
    for key, value in metafields.items():
        # Only write metafields that exist in the CSV
        if key in row:
            row[key] = value

    # Preserve fields exactly as they were
    for field in PRESERVE_FIELDS:
        row[field] = row.get(field)

    return row


# ------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------

def run_products_csv(csv_path):
    print("Loading CSV:", csv_path)

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} rows")

    output_rows = []

    for row in rows:
        product = row_to_product(row)
        enriched = run_mvqueen(product)
        new_row = apply_mvqueen_to_row(row, enriched)
        output_rows.append(new_row)

    # Write output CSV
    print("Writing:", OUTPUT_CSV)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(output_rows)

    print("Done! Output saved to:", OUTPUT_CSV)


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

if __name__ == "__main__":
    process_csv()