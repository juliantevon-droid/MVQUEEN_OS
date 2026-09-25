"""MVQueen catalog-level internal-linking intelligence V1.

Builds deterministic internal-link targets only from canonical product handles and
explicitly supplied Shopify collection handles. It never guesses a collection URL,
never crosses brand worlds, and performs no network or Shopify writes.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List, Mapping


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _link(anchor: str, target: str, link_type: str, reason: str) -> Dict[str, str]:
    return {
        "anchor": anchor,
        "target": target,
        "type": link_type,
        "reason": reason,
    }


def resolve_internal_links(
    records: Iterable[Dict[str, Any]],
    *,
    collection_handles: Mapping[str, str] | None = None,
    product_collection_targets: Mapping[str, Iterable[Mapping[str, str]]] | None = None,
    product_limit: int = 3,
    collection_limit: int = 6,
) -> List[Dict[str, Any]]:
    """Return enriched record copies with verified internal-link targets."""
    items = [deepcopy(record) for record in records]
    by_id = {
        _text(record.get("identity", {}).get("product_id")): record
        for record in items
        if _text(record.get("identity", {}).get("product_id"))
    }
    collection_handles = dict(collection_handles or {})
    product_collection_targets = dict(product_collection_targets or {})

    for record in items:
        if record.get("status") != "PRODUCTION_READY":
            raise ValueError("Internal linking requires PRODUCTION_READY records")
        if record.get("qa", {}).get("passed") is not True:
            raise ValueError("Internal linking requires QA-passed records")

        product_id = _text(record.get("identity", {}).get("product_id"))
        brand_world = _text(record.get("intelligence", {}).get("brand_world"))
        links: List[Dict[str, str]] = []
        seen_targets: set[str] = set()

        relationship_ids = [
            *record.get("merchandising", {}).get("related_products", []),
            *record.get("intelligence", {}).get("cross_sell_candidates", []),
        ]
        for candidate_id in relationship_ids:
            candidate = by_id.get(_text(candidate_id))
            if not candidate:
                continue
            if _text(candidate.get("intelligence", {}).get("brand_world")) != brand_world:
                continue
            handle = _text(candidate.get("identity", {}).get("handle"))
            title = _text(candidate.get("copy", {}).get("title"))
            if not handle or not title:
                continue
            target = f"/products/{handle}"
            if target in seen_targets:
                continue
            links.append(_link(title, target, "product", "catalog_relationship"))
            seen_targets.add(target)
            if len([item for item in links if item["type"] == "product"]) >= product_limit:
                break

        for collection_name in record.get("merchandising", {}).get("collections", []):
            name = _text(collection_name)
            handle = _text(collection_handles.get(name))
            if not name or not handle:
                continue
            target = f"/collections/{handle}"
            if target in seen_targets:
                continue
            links.append(_link(name, target, "collection", "explicit_collection_handle"))
            seen_targets.add(target)
            if len([item for item in links if item["type"] == "collection"]) >= collection_limit:
                break

        for membership in product_collection_targets.get(product_id, []):
            if len([item for item in links if item["type"] == "collection"]) >= collection_limit:
                break
            name = _text(membership.get("title"))
            handle = _text(membership.get("handle"))
            if not name or not handle:
                continue
            target = f"/collections/{handle}"
            if target in seen_targets:
                continue
            links.append(_link(name, target, "collection", "verified_shopify_membership"))
            seen_targets.add(target)

        record.setdefault("seo", {})["internal_links"] = links
        record["seo"]["internal_link_audit"] = {
            "resolver": "INTERNAL_LINKING_INTELLIGENCE_V1",
            "source_product_id": product_id,
            "brand_world": brand_world,
            "product_links": sum(1 for item in links if item["type"] == "product"),
            "collection_links": sum(1 for item in links if item["type"] == "collection"),
            "collection_urls_require_explicit_handle": True,
        }

        suite = record.get("content_suite")
        if isinstance(suite, dict):
            blog = suite.get("blog")
            if isinstance(blog, dict):
                existing = [
                    item
                    for item in blog.get("internal_links", [])
                    if isinstance(item, dict)
                    and _text(item.get("target"))
                    and _text(item.get("anchor"))
                ]
                combined = existing + [
                    {"anchor": item["anchor"], "target": item["target"], "type": item["type"]}
                    for item in links
                ]
                deduped = []
                seen = set()
                for item in combined:
                    target = _text(item.get("target"))
                    if target and target not in seen:
                        deduped.append(item)
                        seen.add(target)
                blog["internal_links"] = deduped

    return items


__all__ = ["resolve_internal_links"]
