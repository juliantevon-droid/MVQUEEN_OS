from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from catalog_service import read_all_products
from shopify_graphql_client import get_client

ROOT = Path(__file__).resolve().parents[2]
BACKUP_DIR = ROOT / "backups" / "shopify_catalog"


def main() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    client = get_client(dry_run=True)
    products = read_all_products(client)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = BACKUP_DIR / f"products_{timestamp}.json"
    csv_path = BACKUP_DIR / f"products_{timestamp}.csv"

    payload = {
        "generated_at_utc": timestamp,
        "store_domain": client.store_domain,
        "api_version": client.api_version,
        "count": len(products),
        "read_only": True,
        "products": products,
    }
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    fieldnames = [
        "id", "title", "handle", "status", "vendor", "product_type",
        "tags", "description_html", "created_at", "updated_at",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            row = dict(product)
            row["tags"] = "|".join(row.get("tags") or [])
            writer.writerow(row)

    print(f"Catalog snapshot created: {json_path}")
    print(f"CSV snapshot created: {csv_path}")
    print(f"Products captured: {len(products)}")


if __name__ == "__main__":
    main()
