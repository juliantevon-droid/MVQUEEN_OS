#!/usr/bin/env python3
"""Validate the real historical MVQUEEN recovery catalog end-to-end.

This script is CI-only/read-only with respect to Shopify. The input CSV is
extracted from Git history into a temporary path by the workflow.
"""
from __future__ import annotations

import csv
import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_ROOT = REPO_ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from catalog_recovery_audit import audit_csv
from mvqueen_engine.brand_governance import SUPPLIER_AND_REFERENCE_BRANDS
from mvqueen_engine.catalog_recovery_transform import transform_csv
from mvqueen_engine.config import SHOPIFY_PROTECTED_COLUMNS

EXPECTED_ROWS = 3575
EXPECTED_PRODUCTS = 948


def _read(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def validate(source_path: str | Path) -> dict:
    source = Path(source_path)
    audit = audit_csv(source)

    with tempfile.TemporaryDirectory() as tmp:
        normalized = Path(tmp) / "normalized.csv"
        report_path = Path(tmp) / "transform-report.json"
        transform = transform_csv(source, normalized, report_path)

        source_headers, source_rows = _read(source)
        normalized_headers, normalized_rows = _read(normalized)

        if source_headers != normalized_headers:
            raise AssertionError("Recovery transform changed Shopify column order.")
        if len(source_rows) != EXPECTED_ROWS or len(normalized_rows) != EXPECTED_ROWS:
            raise AssertionError(
                f"Expected {EXPECTED_ROWS} rows; source={len(source_rows)} "
                f"normalized={len(normalized_rows)}"
            )
        if audit["counts"]["unique_products"] != EXPECTED_PRODUCTS:
            raise AssertionError(
                f"Expected {EXPECTED_PRODUCTS} audit products; "
                f"got {audit['counts']['unique_products']}"
            )
        if transform["unique_products"] != EXPECTED_PRODUCTS:
            raise AssertionError(
                f"Expected {EXPECTED_PRODUCTS} transformed products; "
                f"got {transform['unique_products']}"
            )
        if transform["release_importable"]:
            raise AssertionError("Recovery normalization must never be directly importable.")

        for index, (before, after) in enumerate(zip(source_rows, normalized_rows)):
            for field in SHOPIFY_PROTECTED_COLUMNS:
                if field in source_headers and before.get(field) != after.get(field):
                    raise AssertionError(
                        f"Protected field changed at row {index}: {field}"
                    )

        customer_fields = ("Title", "Body (HTML)", "SEO Title", "SEO Description", "Tags")
        leakage = {}
        for index, row in enumerate(normalized_rows):
            blob = " ".join(str(row.get(field) or "") for field in customer_fields).casefold()
            found = [
                term for term in SUPPLIER_AND_REFERENCE_BRANDS
                if term.casefold() in blob
            ]
            if found:
                leakage[index] = found[:5]
                if len(leakage) >= 25:
                    break
        if leakage:
            raise AssertionError(
                "Supplier/reference brand leakage remains after normalization: "
                + json.dumps(leakage, sort_keys=True)
            )

        summary = {
            "source_rows": len(source_rows),
            "unique_products": transform["unique_products"],
            "audit_decision": audit["decision"],
            "audit_hold_reasons": audit["hold_reasons"],
            "normalized_hold_products": transform["hold_products"],
            "normalized_review_products": transform["review_products"],
            "normalized_hold_sample": [
                {
                    "handle": item["handle"],
                    "title": item["title"],
                    "tier1_voice_violations": item["tier1_voice_violations"],
                    "supplier_or_reference_brand_leakage": item["supplier_or_reference_brand_leakage"],
                }
                for item in transform["products"]
                if item["status"] == "HOLD"
            ][:25],
            "audit_missing_category_sample": audit["missing_category_handle_sample"],
            "audit_missing_product_type_sample": audit["missing_product_type_handle_sample"],
            "audit_repeated_sku_sample": audit["repeated_sku_sample"],
            "protected_field_changes": 0,
            "supplier_reference_leakage_after_normalization": 0,
            "release_importable": False,
        }
        return summary


def main(argv: list[str] | None = None) -> int:
    args = list(argv or sys.argv[1:])
    if len(args) != 1:
        raise SystemExit("Usage: validate_historical_recovery.py RECOVERY.csv")
    print(json.dumps(validate(args[0]), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
