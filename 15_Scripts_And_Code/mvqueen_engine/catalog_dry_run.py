"""MVQUEEN catalog dry-run processor.

Pipeline:
snapshot -> normalize -> classify -> editorial proposal -> SEO proposal ->
protected-field diff -> safety guard -> QA-style review.

This module NEVER writes to Shopify. A later approved writer must be a
separate, explicit step.
"""
from __future__ import annotations

import html
import re
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Tuple

from .catalog_guard import validate_catalog, validate_protected
from .config import (
    BRAND_NAME,
    MAX_PRODUCTS_PER_IMPORT_FILE,
    SHOPIFY_EDITORIAL_COLUMNS,
    SHOPIFY_PROTECTED_COLUMNS,
)

SUPPLIER_RE = re.compile(
    r"\b(OUHOE|MISS\.?\s*QUEEN|HOEGOA|FANZHEN|EELHOPE|COLOR\s*FIT|"
    r"WEST\s*&\s*MONTH|SUPPLIER|WHOLESALE|GENERIC)\b",
    re.I,
)
UNSAFE_HTML_RE = re.compile(r"<\s*(script|style)\b|\son\w+\s*=|javascript\s*:", re.I)
TAG_SPLIT_RE = re.compile(r"[,|]+")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'&-]*")

def _text(value: Any) -> str:
    return str(value or "").strip()

def _strip_html(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()

def _clean_supplier_text(value: str) -> str:
    value = SUPPLIER_RE.sub("", value)
    return re.sub(r"\s{2,}", " ", value).strip(" -|,:")

def _clean_tags(value: Any) -> List[str]:
    tags = []
    for raw in TAG_SPLIT_RE.split(_text(value)):
        tag = _clean_supplier_text(raw).strip()
        if not tag:
            continue
        if tag.lower() in {x.lower() for x in ("supplier", "wholesale", "generic", "miss queen")}:
            continue
        if tag not in tags:
            tags.append(tag)
    return tags

def _infer_type(title: str, existing: str) -> str:
    if existing and existing.lower() != "other":
        return existing.strip()
    t = title.lower()
    if any(x in t for x in ("necklace", "pendant", "earring", "bracelet", "ring", "jewelry")):
        return "Jewelry"
    if any(x in t for x in ("serum", "cleanser", "moisturizer", "cream", "mask", "toner", "skincare")):
        return "Skincare"
    if any(x in t for x in ("lip", "foundation", "concealer", "blush", "mascara", "eyeshadow", "cosmetic")):
        return "Cosmetics"
    if any(x in t for x in ("shampoo", "conditioner", "hair", "wig", "extension")):
        return "Hair Care"
    return existing.strip() if existing.strip() else "Women’s Fashion"

def _title(source: Dict[str, Any]) -> str:
    raw = _clean_supplier_text(_text(source.get("Title")))
    return re.sub(r"\s{2,}", " ", raw).strip()

def _body(source: Dict[str, Any], title: str) -> str:
    raw = _text(source.get("Body HTML") or source.get("descriptionHtml") or source.get("description"))
    cleaned = _clean_supplier_text(_strip_html(raw))
    if not cleaned:
        return f"<p>{html.escape(title)}</p>"
    # Preserve factual source language where possible, while removing supplier noise.
    return f'<div class="mvqueen-source-content"><p>{html.escape(cleaned)}</p></div>'

def _seo_title(title: str) -> str:
    suffix = " | MVQUEEN"
    if title.lower().endswith("| mvqueen"):
        return title[:60]
    return (title[:60 - len(suffix)].rstrip() + suffix)[:60]

def _seo_description(title: str, body: str) -> str:
    factual = _strip_html(body)
    factual = re.sub(r"\s+", " ", factual)
    text = f"{title}. {factual}".strip()
    text = re.sub(r"\b(wholesale|supplier|generic)\b", "", text, flags=re.I)
    text = re.sub(r"\s{2,}", " ", text).strip(" .")
    return text[:155]

def propose_product(source: Dict[str, Any]) -> Dict[str, Any]:
    """Return a proposed editorial snapshot without mutating the input."""
    original = deepcopy(source)
    title = _title(original)
    body = _body(original, title)
    product_type = _infer_type(title, _text(original.get("Product Type") or original.get("productType")))
    tags = _clean_tags(original.get("Tags") or original.get("tags"))
    if "mvq:catalog" not in {t.lower() for t in tags}:
        tags.append("mvq:catalog")

    proposed = deepcopy(original)
    proposed.update({
        "Title": title,
        "Body HTML": body,
        "Product Type": product_type,
        "Tags": ", ".join(tags),
        "SEO Title": _seo_title(title),
        "SEO Description": _seo_description(title, body),
    })
    return proposed

def field_diff(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    diff = {}
    for field in SHOPIFY_EDITORIAL_COLUMNS:
        b, a = before.get(field), after.get(field)
        if _text(b) != _text(a):
            diff[field] = {"before": b, "after": a}
    return diff

def _review_flags(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    flags = []
    combined = " ".join(_text(after.get(k)) for k in SHOPIFY_EDITORIAL_COLUMNS)
    if SUPPLIER_RE.search(combined):
        flags.append("supplier-contamination")
    if UNSAFE_HTML_RE.search(_text(after.get("Body HTML"))):
        flags.append("unsafe-html")
    if not _text(after.get("Title")):
        flags.append("missing-title")
    if not _text(after.get("Body HTML")):
        flags.append("missing-body")
    if len(_text(after.get("SEO Title"))) > 60:
        flags.append("seo-title-too-long")
    if len(_text(after.get("SEO Description"))) > 160:
        flags.append("seo-description-too-long")
    protected = validate_protected(before, after)
    if protected:
        flags.extend(protected)
    return flags

def dry_run_product(source: Dict[str, Any]) -> Dict[str, Any]:
    before = deepcopy(source)
    after = propose_product(source)
    diff = field_diff(before, after)
    flags = _review_flags(before, after)
    row = {k: after.get(k, "") for k in ("Title", "Body HTML", "Product Type", "Tags", "SEO Title", "SEO Description")}
    guard = validate_catalog([row])
    status = "BLOCKED" if flags or not guard["ok"] else ("REVIEW" if diff else "PASS")
    return {
        "status": status,
        "product_id": source.get("id") or source.get("Product ID"),
        "handle": source.get("handle") or source.get("Handle"),
        "changed_fields": list(diff),
        "diff": diff,
        "flags": sorted(set(flags + guard["issues"])),
        "protected_fields_checked": sorted(SHOPIFY_PROTECTED_COLUMNS),
        "write_performed": False,
        "proposed": after,
    }

def dry_run_catalog(products: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    products = list(products)
    results = [dry_run_product(product) for product in products]
    statuses = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS", "REVIEW", "BLOCKED")}
    return {
        "mode": "dry-run",
        "write_performed": False,
        "product_limit": None,
        "max_products_per_import_file": MAX_PRODUCTS_PER_IMPORT_FILE,
        "count": len(products),
        "statuses": statuses,
        "results": results,
    }
