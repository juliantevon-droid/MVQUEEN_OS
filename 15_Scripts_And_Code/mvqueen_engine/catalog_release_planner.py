"""Read-only release planner for the recovered MVQueen Shopify catalog.

The planner resolves proven duplicate product listings without rewriting handles,
SKUs, prices, inventory, variants, or media relationships. It produces a
manifest only; it never contacts Shopify and never creates an import file.
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mvqueen_engine.brand_governance import SUPPLIER_AND_REFERENCE_BRANDS, contains_term

TOKEN_RE = re.compile(r"[a-z0-9]+", re.I)
NUMERIC_SUFFIX_RE = re.compile(r"-\d+$")
STOPWORDS = {
    "the", "and", "for", "with", "your", "this", "that", "from", "has",
    "are", "not", "easy", "long", "lasting", "makeup", "product",
}


@dataclass
class ProductRecord:
    handle: str
    first_index: int
    rows: list[dict[str, str]]
    skus: set[str]
    title: str
    category: str
    product_type: str
    image_src_count: int
    variant_image_count: int


def _value(row: dict[str, str], field: str) -> str:
    return str(row.get(field) or "").strip()


def _first(rows: list[dict[str, str]], field: str) -> str:
    for row in rows:
        value = _value(row, field)
        if value:
            return value
    return ""


def _tokens(text: str) -> set[str]:
    return {
        token.casefold()
        for token in TOKEN_RE.findall(str(text or ""))
        if len(token) > 2 and token.casefold() not in STOPWORDS
    }


def _similarity(a: str, b: str) -> float:
    left, right = _tokens(a), _tokens(b)
    if not left and not right:
        return 1.0
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def _has_supplier_identity(handle: str) -> bool:
    readable = handle.replace("-", " ")
    return any(contains_term(readable, term) for term in SUPPLIER_AND_REFERENCE_BRANDS)


def _base_handle(handle: str) -> str:
    return NUMERIC_SUFFIX_RE.sub("", handle)


def _records(rows: list[dict[str, str]]) -> dict[str, ProductRecord]:
    indexes: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(rows):
        handle = _value(row, "Handle")
        if handle:
            indexes[handle].append(index)

    output: dict[str, ProductRecord] = {}
    for handle, members in indexes.items():
        group = [rows[index] for index in members]
        output[handle] = ProductRecord(
            handle=handle,
            first_index=members[0],
            rows=group,
            skus={_value(row, "Variant SKU") for row in group if _value(row, "Variant SKU")},
            title=_first(group, "Title"),
            category=_first(group, "MVQ Category") or _first(group, "Category"),
            product_type=_first(group, "MVQ Product Type") or _first(group, "Product Type") or _first(group, "Type"),
            image_src_count=sum(bool(_value(row, "Image Src")) for row in group),
            variant_image_count=sum(bool(_value(row, "Variant Image")) for row in group),
        )
    return output


def _collision_components(records: dict[str, ProductRecord]) -> list[list[str]]:
    sku_handles: dict[str, set[str]] = defaultdict(set)
    for handle, record in records.items():
        for sku in record.skus:
            sku_handles[sku].add(handle)

    adjacency: dict[str, set[str]] = defaultdict(set)
    for handles in sku_handles.values():
        if len(handles) < 2:
            continue
        for handle in handles:
            adjacency[handle].update(handles - {handle})

    components: list[list[str]] = []
    visited: set[str] = set()
    for start in sorted(adjacency):
        if start in visited:
            continue
        stack = [start]
        component: list[str] = []
        visited.add(start)
        while stack:
            current = stack.pop()
            component.append(current)
            for nxt in sorted(adjacency[current]):
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append(nxt)
        components.append(sorted(component))
    return components


def _candidate_score(record: ProductRecord) -> tuple:
    # Rich operational structure first; branding/handle cosmetics are only
    # tie-breakers because protected commerce data is more valuable.
    return (
        len(record.skus),
        record.image_src_count,
        record.variant_image_count,
        len(record.rows),
        0 if _has_supplier_identity(record.handle) else 1,
        0 if NUMERIC_SUFFIX_RE.search(record.handle) else 1,
        -record.first_index,
    )


def _component_plan(handles: list[str], records: dict[str, ProductRecord]) -> dict[str, Any]:
    members = [records[handle] for handle in handles]
    union_skus = set().union(*(record.skus for record in members))
    eligible = [record for record in members if record.skus == union_skus]

    if not eligible:
        return {
            "status": "HOLD",
            "reason": "no_single_member_preserves_all_component_skus",
            "handles": handles,
            "sku_union_count": len(union_skus),
        }

    canonical = max(eligible, key=_candidate_score)
    exclusions: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for member in members:
        if member.handle == canonical.handle:
            continue
        if not member.skus.issubset(canonical.skus):
            issues.append({
                "handle": member.handle,
                "reason": "sku_not_subset_of_canonical",
            })
            continue

        same_taxonomy = (
            member.category == canonical.category
            and member.product_type == canonical.product_type
        )
        title_similarity = _similarity(member.title, canonical.title)
        same_base = _base_handle(member.handle) == _base_handle(canonical.handle)

        # Strong duplicate evidence: same numbered family OR same taxonomy plus
        # meaningful title overlap. This rejects arbitrary SKU collisions.
        if not same_base and not (same_taxonomy and title_similarity >= 0.30):
            issues.append({
                "handle": member.handle,
                "reason": "insufficient_duplicate_identity_evidence",
                "title_similarity": round(title_similarity, 4),
                "same_taxonomy": same_taxonomy,
            })
            continue

        exclusions.append({
            "handle": member.handle,
            "sku_count": len(member.skus),
            "row_count": len(member.rows),
            "image_src_count": member.image_src_count,
            "variant_image_count": member.variant_image_count,
            "title_similarity": round(title_similarity, 4),
            "same_numbered_family": same_base,
        })

    if issues:
        return {
            "status": "HOLD",
            "reason": "ambiguous_collision_component",
            "handles": handles,
            "canonical_candidate": canonical.handle,
            "issues": issues,
            "sku_union_count": len(union_skus),
        }

    return {
        "status": "RESOLVED_DUPLICATE",
        "canonical_handle": canonical.handle,
        "canonical_sku_count": len(canonical.skus),
        "canonical_row_count": len(canonical.rows),
        "canonical_image_src_count": canonical.image_src_count,
        "canonical_variant_image_count": canonical.variant_image_count,
        "excluded": exclusions,
        "sku_union_count": len(union_skus),
    }


def build_release_plan(rows: list[dict[str, str]]) -> dict[str, Any]:
    records = _records(rows)
    components = _collision_components(records)
    component_plans = [_component_plan(component, records) for component in components]

    unresolved = [item for item in component_plans if item["status"] == "HOLD"]
    excluded_handles = {
        item["handle"]
        for plan in component_plans
        if plan["status"] == "RESOLVED_DUPLICATE"
        for item in plan["excluded"]
    }
    canonical_handles = set(records) - excluded_handles

    candidate_records = [records[handle] for handle in canonical_handles]
    media_handles = {
        record.handle for record in candidate_records
        if record.image_src_count or record.variant_image_count
    }
    handles_without_media = sorted(canonical_handles - media_handles)

    return {
        "schema_version": "mvqueen.catalog_release_plan.v1",
        "mode": "read-only-release-planning",
        "shopify_network_io": False,
        "write_performed": False,
        "source_products": len(records),
        "collision_components": len(components),
        "resolved_duplicate_components": sum(
            plan["status"] == "RESOLVED_DUPLICATE" for plan in component_plans
        ),
        "unresolved_collision_components": len(unresolved),
        "excluded_duplicate_handles": len(excluded_handles),
        "release_candidate_products": len(canonical_handles),
        "handles_with_recovered_media": len(media_handles),
        "handles_without_recovered_media": len(handles_without_media),
        "release_importable": False,
        "release_blockers": [
            blocker for blocker, active in (
                ("unresolved_sku_collisions", bool(unresolved)),
                ("incomplete_recovered_media", bool(handles_without_media)),
                ("explicit_draft_create_approval_required", True),
            )
            if active
        ],
        "components": component_plans,
        "unresolved_components": unresolved,
        "excluded_handle_sample": sorted(excluded_handles)[:50],
        "media_missing_handle_sample": handles_without_media[:50],
    }


def plan_csv(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return build_release_plan([dict(row) for row in reader])


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--output")
    args = parser.parse_args()
    plan = plan_csv(args.source)
    rendered = json.dumps(plan, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 2 if plan["unresolved_collision_components"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
