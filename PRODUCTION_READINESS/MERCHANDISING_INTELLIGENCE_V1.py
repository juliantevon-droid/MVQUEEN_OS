"""MVQueen catalog-level merchandising intelligence V1.

Resolves related-product and cross-sell candidates across a set of canonical
PRODUCTION_READY records. The resolver is deterministic, brand-world aware,
fact-safe, and transport-neutral. It never mutates Shopify and never invents
bundle eligibility, discounts, compatibility, or product facts.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Iterable, List, Tuple


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _norm(value: Any) -> str:
    return " ".join(_text(value).lower().split())


def _verified_fact(record: Dict[str, Any], *names: str) -> str:
    wanted = {_norm(name) for name in names}
    for fact in record.get("source_truth", {}).get("facts", []):
        if fact.get("verified") is True and _norm(fact.get("name")) in wanted:
            value = _text(fact.get("value"))
            if value:
                return value
    return ""


def _require_ready(record: Dict[str, Any]) -> None:
    if record.get("status") != "PRODUCTION_READY":
        raise ValueError("Catalog merchandising requires PRODUCTION_READY records")
    qa = record.get("qa", {})
    if qa.get("passed") is not True or qa.get("errors"):
        raise ValueError("Catalog merchandising requires QA-passed records")
    if not _text(record.get("identity", {}).get("product_id")):
        raise ValueError("Catalog merchandising requires identity.product_id")
    if _text(record.get("intelligence", {}).get("brand_world")) not in {"mvqueen", "miss-princess"}:
        raise ValueError("Catalog merchandising requires an approved brand_world")


def _relationship_score(source: Dict[str, Any], candidate: Dict[str, Any]) -> Tuple[int, List[str]]:
    reasons: List[str] = []
    score = 0

    source_category = source.get("category", {})
    candidate_category = candidate.get("category", {})

    source_type = _norm(source_category.get("product_type"))
    candidate_type = _norm(candidate_category.get("product_type"))
    source_category_name = _norm(source_category.get("category"))
    candidate_category_name = _norm(candidate_category.get("category"))
    source_subcategory = _norm(source_category.get("subcategory"))
    candidate_subcategory = _norm(candidate_category.get("subcategory"))

    if source_type and source_type == candidate_type:
        score += 6
        reasons.append("same_product_type")
    if source_subcategory and source_subcategory == candidate_subcategory:
        score += 5
        reasons.append("same_subcategory")
    if source_category_name and source_category_name == candidate_category_name:
        score += 4
        reasons.append("same_category")

    source_material = _norm(_verified_fact(source, "material", "fabric", "composition"))
    candidate_material = _norm(_verified_fact(candidate, "material", "fabric", "composition"))
    if source_material and source_material == candidate_material:
        score += 2
        reasons.append("same_verified_material")

    source_color = _norm(_verified_fact(source, "color", "shade"))
    candidate_color = _norm(_verified_fact(candidate, "color", "shade"))
    if source_color and source_color == candidate_color:
        score += 1
        reasons.append("same_verified_color")

    return score, reasons


def resolve_catalog(records: Iterable[Dict[str, Any]], *, related_limit: int = 4, cross_sell_limit: int = 4) -> List[Dict[str, Any]]:
    """Return enriched record copies with deterministic catalog relationships."""
    items = [deepcopy(record) for record in records]
    for record in items:
        _require_ready(record)

    by_id = {
        _text(record.get("identity", {}).get("product_id")): record
        for record in items
    }

    for record in items:
        product_id = _text(record.get("identity", {}).get("product_id"))
        brand_world = _text(record.get("intelligence", {}).get("brand_world"))
        source_category = _norm(record.get("category", {}).get("category"))
        source_type = _norm(record.get("category", {}).get("product_type"))

        ranked: List[Tuple[int, str, List[str]]] = []
        cross_sell: List[Tuple[int, str, List[str]]] = []

        for candidate_id, candidate in by_id.items():
            if candidate_id == product_id:
                continue
            if _text(candidate.get("intelligence", {}).get("brand_world")) != brand_world:
                continue

            score, reasons = _relationship_score(record, candidate)
            if score > 0:
                ranked.append((score, candidate_id, reasons))

            candidate_category = _norm(candidate.get("category", {}).get("category"))
            candidate_type = _norm(candidate.get("category", {}).get("product_type"))
            if (
                source_category
                and source_category == candidate_category
                and source_type
                and candidate_type
                and source_type != candidate_type
            ):
                cross_score = score + 3
                cross_sell.append((cross_score, candidate_id, reasons + ["complementary_product_type"]))

        ranked.sort(key=lambda item: (-item[0], item[1]))
        cross_sell.sort(key=lambda item: (-item[0], item[1]))

        related_ids = [candidate_id for _, candidate_id, _ in ranked[:related_limit]]
        cross_sell_ids = [candidate_id for _, candidate_id, _ in cross_sell[:cross_sell_limit]]

        record.setdefault("merchandising", {})["related_products"] = related_ids
        record["merchandising"]["bundles"] = []
        record.setdefault("intelligence", {})["cross_sell_candidates"] = cross_sell_ids

        record["merchandising"]["relationship_audit"] = {
            "resolver": "MERCHANDISING_INTELLIGENCE_V1",
            "brand_world": brand_world,
            "related": [
                {"product_id": candidate_id, "score": score, "reasons": reasons}
                for score, candidate_id, reasons in ranked[:related_limit]
            ],
            "cross_sell": [
                {"product_id": candidate_id, "score": score, "reasons": reasons}
                for score, candidate_id, reasons in cross_sell[:cross_sell_limit]
            ],
            "bundle_policy": "no_approved_bundle_rule_no_bundle",
        }

    return items


__all__ = ["resolve_catalog"]
