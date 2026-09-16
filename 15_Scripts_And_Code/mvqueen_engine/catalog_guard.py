"""
MVQUEEN OS — Catalog Guard

Safety layer for catalog-scale product optimization.

Purpose:
- Prevent protected Shopify fields from being changed accidentally.
- Detect duplicate handles/titles and supplier-brand contamination.
- Validate required SEO/content fields before a write plan is approved.
- Produce a deterministic report suitable for CI, dry-runs, or API orchestration.

This module does NOT write to Shopify. It validates proposed changes first.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping
import re


PROTECTED_FIELDS = {
    "Handle",
    "Product ID",
    "Variant ID",
    "SKU",
    "Variant SKU",
    "Inventory quantity",
    "Inventory policy",
    "Inventory tracker",
    "Option1 Name",
    "Option1 Value",
    "Option2 Name",
    "Option2 Value",
    "Option3 Name",
    "Option3 Value",
    "Variant Grams",
    "Variant Inventory Qty",
    "Variant Inventory Tracker",
    "Variant Fulfillment Service",
    "Variant Requires Shipping",
    "Variant Taxable",
    "Variant Barcode",
    "Image Src",
    "Image Position",
    "Variant Image",
    "Gift Card",
}

DEFAULT_CONTAMINATION_TERMS = {
    "OUHOE",
    "MISS.QUEEN",
    "MISS. QUEEN",
    "HOEGOA",
    "FANZHEN",
    "EELHOPE",
    "COLOR FIT",
    "WEST & MONTH",
}

REQUIRED_CONTENT_FIELDS = {
    "Title",
    "Body (HTML)",
    "SEO Title",
    "SEO Description",
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    field: str | None = None
    value: Any = None


@dataclass
class GuardReport:
    findings: list[Finding] = field(default_factory=list)

    def add(self, severity: str, code: str, message: str, *, field: str | None = None, value: Any = None) -> None:
        self.findings.append(Finding(severity, code, message, field, value))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "ERROR"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "WARNING"]

    @property
    def passed(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "findings": [f.__dict__ for f in self.findings],
        }


def validate_change_set(
    before: Mapping[str, Any],
    proposed: Mapping[str, Any],
    *,
    contamination_terms: Iterable[str] = DEFAULT_CONTAMINATION_TERMS,
) -> GuardReport:
    """Validate a single proposed product update without mutating data."""
    report = GuardReport()

    for field in PROTECTED_FIELDS:
        if field in proposed and proposed.get(field) != before.get(field):
            report.add(
                "ERROR",
                "PROTECTED_FIELD_CHANGE",
                f"Protected field '{field}' changed. Catalog Guard blocks this by default.",
                field=field,
            )

    for field in REQUIRED_CONTENT_FIELDS:
        value = proposed.get(field)
        if value is None or not str(value).strip():
            report.add("ERROR", "MISSING_REQUIRED_CONTENT", f"Required content field '{field}' is empty.", field=field)

    title = str(proposed.get("Title", "")).strip()
    if len(title) > 70:
        report.add("WARNING", "TITLE_LENGTH", "Product title exceeds the recommended 70-character ceiling.", field="Title", value=len(title))

    seo_title = str(proposed.get("SEO Title", "")).strip()
    if len(seo_title) > 60:
        report.add("WARNING", "SEO_TITLE_LENGTH", "SEO title exceeds the recommended 60-character target.", field="SEO Title", value=len(seo_title))

    seo_description = str(proposed.get("SEO Description", "")).strip()
    if len(seo_description) > 160:
        report.add("WARNING", "SEO_DESCRIPTION_LENGTH", "SEO description exceeds the recommended 160-character target.", field="SEO Description", value=len(seo_description))

    haystack = " ".join(str(proposed.get(k, "")) for k in ("Title", "Body (HTML)", "SEO Title", "SEO Description", "Tags"))
    upper = haystack.upper()
    for term in contamination_terms:
        if term.upper() in upper:
            report.add("ERROR", "BRAND_CONTAMINATION", f"Supplier/third-party brand term detected: {term}.", value=term)

    if "MVQUEEN" not in upper:
        report.add("WARNING", "BRAND_SIGNAL_MISSING", "No MVQUEEN brand signal was found in the optimized content.")

    return report


def duplicate_values(rows: Iterable[Mapping[str, Any]], field: str) -> dict[str, list[int]]:
    """Return repeated normalized values and their row indexes."""
    seen: dict[str, list[int]] = {}
    for index, row in enumerate(rows):
        value = str(row.get(field, "")).strip().casefold()
        if not value:
            continue
        seen.setdefault(value, []).append(index)
    return {value: indexes for value, indexes in seen.items() if len(indexes) > 1}


def validate_catalog(rows: list[Mapping[str, Any]]) -> GuardReport:
    """Run catalog-level duplicate and product-level safety checks."""
    report = GuardReport()

    for field in ("Handle", "Title"):
        for value, indexes in duplicate_values(rows, field).items():
            report.add(
                "WARNING",
                "DUPLICATE_VALUE",
                f"Duplicate {field} detected across catalog rows.",
                field=field,
                value={"normalized": value, "rows": indexes},
            )

    for index, row in enumerate(rows):
        before = row.get("__before__", row)
        proposed = row.get("__proposed__", row)
        child = validate_change_set(before, proposed)
        for finding in child.findings:
            finding.message = f"Row {index}: {finding.message}"
            report.findings.append(finding)

    return report


if __name__ == "__main__":
    print("MVQUEEN Catalog Guard loaded. Import validate_catalog() or validate_change_set().")
