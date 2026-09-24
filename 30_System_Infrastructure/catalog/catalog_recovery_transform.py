"""Deterministic, offline Shopify CSV recovery transformer.

The transformer preserves source row order and protected commerce fields. It
normalizes only customer-facing editorial fields and never contacts Shopify.
It is a recovery-normalization stage, not a publication artifact.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from typing import Any

from brand_governance import (
    BRAND_GOVERNANCE_SOURCES,
    SUPPLIER_AND_REFERENCE_BRANDS,
    find_tier1_violations,
)
from mvqueen_engine.config import (
    CANONICAL_BRAND,
    SHOPIFY_PROTECTED_COLUMNS,
)
from mvqueen_engine.catalog_safety import assert_protected_unchanged

UNSAFE_HTML_RE = re.compile(r"<\s*(script|style)\b|\son\w+\s*=|javascript\s*:", re.I)
TAG_SPLIT_RE = re.compile(r"[,|]+")
SPACE_RE = re.compile(r"\s+")

BRAND_RE = re.compile(
    r"\b(?:"
    + "|".join(re.escape(term) for term in sorted(SUPPLIER_AND_REFERENCE_BRANDS, key=len, reverse=True))
    + r")\b",
    re.I,
)

SUPPLIER_BOILERPLATE_RE = re.compile(
    r"\b(?:bulk orders? accepted|wholesale|supplier|dropship(?:ping)?|factory direct)\b",
    re.I,
)


def _text(value: Any) -> str:
    return str(value or "").strip()


def _strip_html(value: str) -> str:
    return SPACE_RE.sub(" ", re.sub(r"<[^>]+>", " ", value or "")).strip()


def _clean_brand_terms(value: str) -> str:
    cleaned = BRAND_RE.sub("", str(value or ""))
    cleaned = SUPPLIER_BOILERPLATE_RE.sub("", cleaned)
    cleaned = re.sub(r"\s+([,.;:])", r"\1", cleaned)
    cleaned = re.sub(r"([|/,:;-])\s*\1+", r"\1", cleaned)
    return SPACE_RE.sub(" ", cleaned).strip(" -|,;:")


def _clean_title(value: str) -> str:
    title = _clean_brand_terms(value)
    title = re.sub(r"\s*\((?:[A-Z0-9_-]{2,20})\)\s*$", "", title)
    return SPACE_RE.sub(" ", title).strip(" -|,:;")


def _clean_body(value: str, title: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return f"<p>{html.escape(title)}</p>" if title else ""
    if UNSAFE_HTML_RE.search(raw):
        raw = _strip_html(raw)
    cleaned = _clean_brand_terms(raw)
    if "<" in cleaned and ">" in cleaned:
        return cleaned
    plain = _strip_html(cleaned)
    return f"<p>{html.escape(plain or title)}</p>" if (plain or title) else ""


def _clean_tags(value: str) -> str:
    tags: list[str] = []
    for raw in TAG_SPLIT_RE.split(str(value or "")):
        tag = _clean_brand_terms(raw).strip()
        if not tag:
            continue
        if tag.casefold() not in {existing.casefold() for existing in tags}:
            tags.append(tag)
    if "mvq:catalog" not in {tag.casefold() for tag in tags}:
        tags.append("mvq:catalog")
    return ", ".join(tags)


def _seo_title(title: str) -> str:
    suffix = f" | {CANONICAL_BRAND}"
    if title.casefold().endswith(suffix.casefold()):
        return title[:60]
    return f"{title[: max(0, 60 - len(suffix))].rstrip()}{suffix}"[:60]


def _seo_description(title: str, body: str) -> str:
    factual = _clean_brand_terms(_strip_html(body))
    combined = SPACE_RE.sub(" ", f"{title}. {factual}").strip(" .")
    return combined[:155]


def _image_alt(title: str, existing: str) -> str:
    existing_clean = _clean_brand_terms(existing)
    if existing_clean:
        return existing_clean[:200]
    return f"{title} product image"[:200] if title else f"{CANONICAL_BRAND} product image"


def _first_nonblank(rows: list[dict[str, str]], field: str) -> str:
    for row in rows:
        value = _text(row.get(field))
        if value:
            return value
    return ""


def _protected_snapshot(row: dict[str, str]) -> dict[str, str]:
    return {k: row.get(k) for k in SHOPIFY_PROTECTED_COLUMNS if k in row}


def transform_rows(rows: list[dict[str, str]], headers: list[str]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    groups: OrderedDict[str, list[int]] = OrderedDict()
    for index, row in enumerate(rows):
        handle = _text(row.get("Handle"))
        key = handle or f"__row_{index}"
        groups.setdefault(key, []).append(index)

    output = [deepcopy(row) for row in rows]
    product_reports: list[dict[str, Any]] = []

    for handle, indexes in groups.items():
        group_rows = [rows[i] for i in indexes]
        lead_index = indexes[0]
        lead_before = rows[lead_index]
        lead_after = output[lead_index]

        source_title = _first_nonblank(group_rows, "Title")
        title = _clean_title(source_title)
        source_body = _first_nonblank(group_rows, "Body (HTML)")
        body = _clean_body(source_body, title)
        tags = _clean_tags(_first_nonblank(group_rows, "Tags"))

        if "Title" in headers:
            lead_after["Title"] = title
        if "Body (HTML)" in headers:
            lead_after["Body (HTML)"] = body
        if "Vendor" in headers:
            lead_after["Vendor"] = CANONICAL_BRAND
        if "Tags" in headers:
            lead_after["Tags"] = tags
        if "SEO Title" in headers:
            lead_after["SEO Title"] = _seo_title(title)
        if "SEO Description" in headers:
            lead_after["SEO Description"] = _seo_description(title, body)

        alt_updates = 0
        for idx in indexes:
            before = rows[idx]
            after = output[idx]
            if _text(before.get("Image Src")) and "Image Alt Text" in headers:
                after["Image Alt Text"] = _image_alt(title, _text(before.get("Image Alt Text")))
                alt_updates += 1

            # Protected fields are immutable in normalization.
            assert_protected_unchanged(_protected_snapshot(before), after)

        customer_blob = " ".join(
            _text(lead_after.get(field))
            for field in ("Title", "Body (HTML)", "SEO Title", "SEO Description", "Tags")
        )
        tier1 = find_tier1_violations(customer_blob)
        supplier_left = [
            term for term in SUPPLIER_AND_REFERENCE_BRANDS
            if term.casefold() in customer_blob.casefold()
        ]

        product_reports.append(
            {
                "handle": "" if handle.startswith("__row_") else handle,
                "row_count": len(indexes),
                "title": title,
                "image_alt_rows_updated": alt_updates,
                "tier1_voice_violations": tier1,
                "supplier_or_reference_brand_leakage": supplier_left,
                "status": "HOLD" if tier1 or supplier_left or not title else "REVIEW",
            }
        )

    holds = [p for p in product_reports if p["status"] == "HOLD"]
    report = {
        "schema_version": "mvqueen.catalog_recovery_transform.v1",
        "mode": "offline-normalization",
        "write_performed": False,
        "shopify_network_io": False,
        "source_rows": len(rows),
        "unique_products": len(groups),
        "hold_products": len(holds),
        "review_products": len(product_reports) - len(holds),
        "brand_governance_sources": list(BRAND_GOVERNANCE_SOURCES),
        "release_importable": False,
        "release_block_reason": (
            "Normalization output preserves historical publication/status fields and "
            "requires QA plus an explicit governed draft-create release step."
        ),
        "products": product_reports,
    }
    return output, report


def transform_csv(source_path: str | Path, output_path: str | Path, report_path: str | Path | None = None) -> dict[str, Any]:
    source = Path(source_path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = list(reader.fieldnames or [])
        if not headers:
            raise ValueError("CSV has no header row")
        if "Handle" not in headers or "Title" not in headers:
            raise ValueError("Shopify CSV must include Handle and Title")
        rows = [dict(row) for row in reader]

    transformed, report = transform_rows(rows, headers)

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(transformed)

    if report_path:
        rp = Path(report_path)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--report")
    args = parser.parse_args()
    report = transform_csv(args.source, args.output, args.report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 2 if report["hold_products"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
