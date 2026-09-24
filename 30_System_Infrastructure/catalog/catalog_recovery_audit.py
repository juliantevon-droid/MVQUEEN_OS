#!/usr/bin/env python3
"""Read-only audit for historical Shopify catalog recovery files.

This utility never transforms, imports, publishes, or mutates Shopify data.
It summarizes a Shopify CSV and returns a deterministic HOLD/READY_FOR_REVIEW
decision so historical recovery blobs cannot bypass the governed catalog path.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

def _load_worker_forbidden() -> tuple[str, ...]:
    """Reuse the canonical denylist without duplicating legacy brand literals."""
    import importlib.util

    worker_path = Path(__file__).with_name("mvqueen_catalog_worker.py")
    spec = importlib.util.spec_from_file_location("mvqueen_catalog_worker_policy", worker_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load canonical catalog worker policy")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(module.FORBIDDEN)


FORBIDDEN_CUSTOMER_BRANDS = _load_worker_forbidden()

REQUIRED_HEADERS = (
    "Handle",
    "Title",
    "Body (HTML)",
    "Vendor",
    "Status",
)

CUSTOMER_FACING_FIELDS = (
    "Title",
    "Body (HTML)",
    "SEO Title",
    "SEO Description",
    "Tags",
)

MVQ_CATEGORY_FIELDS = ("MVQ Category", "Category")
MVQ_PRODUCT_TYPE_FIELDS = ("MVQ Product Type", "Product Type", "Type")


def _value(row: Dict[str, str], *names: str) -> str:
    for name in names:
        value = (row.get(name) or "").strip()
        if value:
            return value
    return ""


def _product_rows(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    first_by_handle: Dict[str, Dict[str, str]] = {}
    for row in rows:
        handle = (row.get("Handle") or "").strip()
        if handle and handle not in first_by_handle:
            first_by_handle[handle] = row
    return list(first_by_handle.values())


def audit_csv(path: str | Path) -> Dict[str, Any]:
    source = Path(path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing_headers = [name for name in REQUIRED_HEADERS if name not in headers]
        if missing_headers:
            raise ValueError(f"Missing required Shopify headers: {missing_headers}")
        rows = [dict(row) for row in reader if any((v or "").strip() for v in row.values())]

    products = _product_rows(rows)
    vendors = Counter((_value(row, "Vendor") or "(blank)") for row in products)
    statuses = Counter((_value(row, "Status") or "(blank)") for row in products)
    categories = Counter(
        (_value(row, *MVQ_CATEGORY_FIELDS) or "(blank)") for row in products
    )

    leakage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for row in products:
        for field in CUSTOMER_FACING_FIELDS:
            blob = (row.get(field) or "").upper()
            for brand in FORBIDDEN_CUSTOMER_BRANDS:
                if brand in blob:
                    leakage[brand][field] += 1

    image_rows = [row for row in rows if _value(row, "Image Src")]
    missing_alt_rows = [row for row in image_rows if not _value(row, "Image Alt Text")]

    sku_rows = [row for row in rows if _value(row, "Variant SKU")]
    sku_counts = Counter(_value(row, "Variant SKU") for row in sku_rows)
    repeated_skus = {sku: count for sku, count in sku_counts.items() if count > 1}

    missing_categories = [
        _value(row, "Handle") for row in products if not _value(row, *MVQ_CATEGORY_FIELDS)
    ]
    missing_product_types = [
        _value(row, "Handle") for row in products if not _value(row, *MVQ_PRODUCT_TYPE_FIELDS)
    ]

    holds: List[str] = []
    if leakage:
        holds.append("supplier_or_legacy_brand_in_customer_copy")
    if missing_alt_rows:
        holds.append("missing_image_alt_text")
    if missing_categories:
        holds.append("missing_mvqueen_category")
    if missing_product_types:
        holds.append("missing_product_type")
    if repeated_skus:
        holds.append("repeated_sku_relationships_require_review")

    return {
        "schema_version": "mvqueen.catalog_recovery_audit.v1",
        "source_name": source.name,
        "decision": "HOLD" if holds else "READY_FOR_REVIEW",
        "hold_reasons": holds,
        "counts": {
            "csv_rows": len(rows),
            "unique_products": len(products),
            "image_rows": len(image_rows),
            "image_rows_missing_alt": len(missing_alt_rows),
            "sku_rows": len(sku_rows),
            "unique_skus": len(sku_counts),
            "repeated_sku_values": len(repeated_skus),
            "products_missing_category": len(missing_categories),
            "products_missing_product_type": len(missing_product_types),
        },
        "vendor_counts": dict(sorted(vendors.items())),
        "status_counts": dict(sorted(statuses.items())),
        "category_counts": dict(sorted(categories.items())),
        "customer_copy_brand_leakage": {
            brand: dict(sorted(fields.items()))
            for brand, fields in sorted(leakage.items())
        },
        "repeated_sku_sample": dict(list(sorted(repeated_skus.items()))[:25]),
        "missing_category_handle_sample": missing_categories[:25],
        "missing_product_type_handle_sample": missing_product_types[:25],
        "safety": {
            "shopify_network_io": False,
            "writes_source_csv": False,
            "changes_protected_fields": False,
            "publishes_products": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Historical Shopify CSV to audit")
    parser.add_argument("--output", help="Optional JSON report path")
    parser.add_argument(
        "--fail-on-hold",
        action="store_true",
        help="Exit 2 when the recovery decision is HOLD",
    )
    args = parser.parse_args()

    report = audit_csv(args.source)
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 2 if args.fail_on_hold and report["decision"] == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
