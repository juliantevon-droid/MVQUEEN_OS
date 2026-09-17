"""MVQueen catalog safety primitives.

This module is intentionally dependency-light and fail-closed. It validates that
editorial/SEO work cannot silently alter Shopify operational identity or source
image structure. It does not publish to Shopify.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

from mvqueen_engine.config import (
    CANONICAL_BRAND,
    MAX_PRODUCTS_PER_IMPORT_FILE,
    ONLY_EDIT_IMAGE_FIELD,
    SHOPIFY_EDITORIAL_COLUMNS,
    SHOPIFY_PROTECTED_COLUMNS,
    PRESERVE_SOURCE_COLUMN_ORDER,
)


def validate_columns(columns: Sequence[str]) -> Tuple[List[str], List[str]]:
    """Return (errors, warnings) for an incoming Shopify CSV schema."""
    errors: List[str] = []
    warnings: List[str] = []
    if not columns:
        return ["CSV has no header row"], warnings

    if "Title" not in columns:
        errors.append("Required Shopify column missing: Title")
    if "Handle" not in columns:
        errors.append("Required Shopify column missing: Handle")

    unknown_operational = [
        c for c in columns
        if c.lower().startswith("variant ") and c not in SHOPIFY_PROTECTED_COLUMNS
    ]
    if unknown_operational:
        warnings.append(
            "Review unknown Variant columns before enabling writes: "
            + ", ".join(unknown_operational)
        )

    return errors, warnings


def protected_snapshot(row: dict) -> dict:
    """Capture every protected field present in a source row."""
    return {k: row.get(k) for k in SHOPIFY_PROTECTED_COLUMNS if k in row}


def assert_protected_unchanged(before: dict, after: dict) -> None:
    """Raise if any protected value changed."""
    for key, expected in before.items():
        if after.get(key) != expected:
            raise ValueError(f"Protected Shopify field changed: {key}")


def validate_brand(text: str) -> None:
    """Reject explicit use of known inspiration brands as the product brand."""
    lowered = (text or "").lower()
    forbidden_brand_mentions = (
        "sephora", "victoria's secret", "victorias secret",
        "fenty beauty", "dior", "miss. queen", "miss queen",
    )
    for brand in forbidden_brand_mentions:
        if brand in lowered and CANONICAL_BRAND.lower() not in lowered:
            raise ValueError(f"Non-canonical brand reference detected: {brand}")


def validate_import_size(product_count: int) -> None:
    if product_count > MAX_PRODUCTS_PER_IMPORT_FILE:
        raise ValueError(
            f"Import batch contains {product_count} products; maximum is "
            f"{MAX_PRODUCTS_PER_IMPORT_FILE}."
        )


def validate_alt_policy(changed_columns: Iterable[str]) -> None:
    """Ensure image edits are limited to Image Alt Text."""
    forbidden = set(changed_columns) - {ONLY_EDIT_IMAGE_FIELD}
    forbidden -= set(SHOPIFY_EDITORIAL_COLUMNS)
    if forbidden:
        raise ValueError(
            "Image workflow attempted to change protected/non-editorial fields: "
            + ", ".join(sorted(forbidden))
        )


def inspect_csv_header(path: str | Path) -> Tuple[List[str], List[str]]:
    """Read only the header for an early, non-destructive schema check."""
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    return validate_columns(header)


__all__ = [
    "validate_columns",
    "protected_snapshot",
    "assert_protected_unchanged",
    "validate_brand",
    "validate_import_size",
    "validate_alt_policy",
    "inspect_csv_header",
]
