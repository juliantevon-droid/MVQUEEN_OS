"""MVQueen catalog dry-run processor.

Consolidates useful proposal logic from pre-production branches behind the
canonical main-branch Catalog Guard. This module is intentionally write-free.
"""
from __future__ import annotations

import html
import re
from copy import deepcopy
from typing import Any, Dict, Iterable

from .catalog_guard import validate_catalog, validate_change_set
from .config import MAX_PRODUCTS_PER_IMPORT_FILE, SHOPIFY_EDITORIAL_COLUMNS

SUPPLIER_RE = re.compile(
    r"\\b(OUHOE|MISS\\.?\\s*QUEEN|HOEGOA|FANZHEN|EELHOPE|COLOR\\s*FIT|"
    r"WEST\\s*&\\s*MONTH|SUPPLIER|WHOLESALE|GENERIC)\\b",
    re.I,
)
UNSAFE_HTML_RE = re.compile(r"<\\s*(script|style)\\b|\\son\\w+\\s*=|javascript\\s*:", re.I)
TAG_SPLIT_RE = re.compile(r"[,|]+")


def _text(value: Any) -> str:
    return str(value or "").strip()


def _strip_html(value: str) -> str:
    return re.sub(r"\\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


def _clean_supplier_text(value: str) -> str:
    return re.sub(r"\\s{2,}", " ", SUPPLIER_RE.sub("", value)).strip(" -|,:")


def _clean_tags(value: Any) -> list[str]:
    raw_values = value if isinstance(value, (list, tuple, set)) else TAG_SPLIT_RE.split(_text(value))
    tags: list[str] = []
    for raw in raw_values:
        tag = _clean_supplier_text(_text(raw))
        if not tag:
            continue
        if tag.casefold() not in {existing.casefold() for existing in tags}:
            tags.append(tag)
    return tags


def _infer_type(title: str, existing: str) -> str:
    if existing and existing.casefold() != "other":
        return existing.strip()
    lowered = title.casefold()
    if any(x in lowered for x in ("necklace", "pendant", "earring", "bracelet", "ring", "jewelry")):
        return "Jewelry"
    if any(x in lowered for x in ("serum", "cleanser", "moisturizer", "cream", "mask", "toner", "skincare")):
        return "Skincare"
    if any(x in lowered for x in ("lip", "foundation", "concealer", "blush", "mascara", "eyeshadow", "cosmetic")):
        return "Cosmetics"
    if any(x in lowered for x in ("shampoo", "conditioner", "hair", "wig", "extension")):
        return "Hair Care"
    return existing.strip() if existing.strip() else "Women’s Fashion"


def _body(source: Dict[str, Any], title: str) -> str:
    raw = _text(
        source.get("Body (HTML)")
        or source.get("Body HTML")
        or source.get("descriptionHtml")
        or source.get("description")
    )
    if not raw:
        return f"<p>{html.escape(title)}</p>"
    if not SUPPLIER_RE.search(raw) and not UNSAFE_HTML_RE.search(raw):
        return raw
    cleaned = _clean_supplier_text(_strip_html(raw))
    return f"<p>{html.escape(cleaned or title)}</p>"


def _seo_title(title: str) -> str:
    suffix = " | MVQueen"
    if title.casefold().endswith(suffix.casefold()):
        return title[:60]
    return f"{title[: 60 - len(suffix)].rstrip()}{suffix}"[:60]


def _seo_description(title: str, body: str) -> str:
    factual = _strip_html(body)
    text = _clean_supplier_text(f"{title}. {factual}")
    return re.sub(r"\\s{2,}", " ", text).strip(" .")[:155]


def propose_product(source: Dict[str, Any]) -> Dict[str, Any]:
    """Create an editorial proposal while retaining all source fields."""
    original = deepcopy(source)
    title = _clean_supplier_text(_text(original.get("Title")))
    body = _body(original, title)
    product_type = _infer_type(
        title,
        _text(original.get("Product Type") or original.get("productType")),
    )
    tags = _clean_tags(original.get("Tags") or original.get("tags"))
    if not any(tag.casefold() == "mvq:catalog" for tag in tags):
        tags.append("mvq:catalog")

    proposed = deepcopy(original)
    proposed.update(
        {
            "Title": title,
            "Body (HTML)": body,
            "Product Type": product_type,
            "Tags": ", ".join(tags),
            "SEO Title": _seo_title(title),
            "SEO Description": _seo_description(title, body),
        }
    )
    return proposed


def field_diff(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        field: {"before": before.get(field), "after": after.get(field)}
        for field in SHOPIFY_EDITORIAL_COLUMNS
        if _text(before.get(field)) != _text(after.get(field))
    }


def dry_run_product(source: Dict[str, Any]) -> Dict[str, Any]:
    before = deepcopy(source)
    proposed = propose_product(source)
    diff = field_diff(before, proposed)
    guard = validate_change_set(before, proposed)
    findings = [finding.__dict__.copy() for finding in guard.findings]
    status = "BLOCKED" if guard.errors else ("REVIEW" if diff or guard.warnings else "PASS")

    return {
        "status": status,
        "product_id": source.get("id") or source.get("Product GID") or source.get("Product ID"),
        "handle": source.get("Handle") or source.get("handle"),
        "changed_fields": list(diff),
        "diff": diff,
        "findings": findings,
        "write_performed": False,
        "before": before,
        "proposed": proposed,
    }


def dry_run_catalog(products: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    source_products = list(products)
    results = [dry_run_product(product) for product in source_products]
    catalog_rows = [
        {"__before__": result["before"], "__proposed__": result["proposed"]}
        for result in results
    ]
    catalog_guard = validate_catalog(catalog_rows)
    statuses = {
        name: sum(1 for result in results if result["status"] == name)
        for name in ("PASS", "REVIEW", "BLOCKED")
    }
    return {
        "mode": "dry-run",
        "write_performed": False,
        "product_limit": None,
        "max_products_per_import_file": MAX_PRODUCTS_PER_IMPORT_FILE,
        "count": len(source_products),
        "statuses": statuses,
        "catalog_guard": catalog_guard.as_dict(),
        "results": results,
    }
