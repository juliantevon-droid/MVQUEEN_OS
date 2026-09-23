"""MVQueen Commercial Intelligence V1.

Pure, deterministic commercial reasoning from verified canonical product data.
No Shopify writes, fabricated evidence, or invented discounts.
"""
from __future__ import annotations

from typing import Any, Dict, List


def _verified_facts(record: Dict[str, Any]) -> Dict[str, Any]:
    facts: Dict[str, Any] = {}
    for fact in record.get("source_truth", {}).get("facts", []):
        if fact.get("verified") is True and fact.get("name"):
            facts[str(fact["name"]).lower()] = fact.get("value")
    return facts


def build_commercial(record: Dict[str, Any]) -> Dict[str, Any]:
    facts = _verified_facts(record)
    intelligence = record.get("intelligence", {})
    category = str(record.get("category", {}).get("product_type", "product")).lower()
    price = record.get("pricing", {}).get("approved_publish_price")

    need = intelligence.get("customer_need") or "Find a product that fits her intended use and personal style."
    desire = intelligence.get("desire") or "Feel confident, polished, and intentional."
    differentiators = list(intelligence.get("differentiators", []))
    objections = list(intelligence.get("objections", []))

    proof: List[str] = []
    for name in ("material", "fabric", "ingredients", "color", "size", "dimensions", "use_context"):
        if name in facts:
            proof.append(f"Verified {name}: {facts[name]}")

    offer_eligibility = ["full_price_hero"]
    if record.get("merchandising", {}).get("bundles"):
        offer_eligibility.append("approved_bundle")
    if record.get("merchandising", {}).get("related_products"):
        offer_eligibility.append("approved_cross_sell")

    landing_requirements = ["value_proposition", "verified_specifications", "pricing", "primary_cta"]
    if category in {"fashion", "dress", "clothing"}:
        landing_requirements.append("fit_or_sizing_information")
    if category in {"skincare", "cosmetics", "beauty"}:
        landing_requirements.append("verified_ingredients_or_product_details")

    return {
        "angle": f"{desire} Designed around {need.lower()}",
        "proof_available": proof,
        "offer_eligibility": offer_eligibility,
        "price_guardrail": "approved_publish_price_required" if price not in (None, "", 0, "0", 0.0) else "blocked_until_price_approved",
        "trust_inputs": ["verified_product_facts", "shipping_and_returns_policy"],
        "objections_responses": objections,
        "funnel_stage": "consideration",
        "aov_strategy": {
            "path": "PRODUCT → COMPLEMENT → BUNDLE → THRESHOLD",
            "related_products": list(record.get("merchandising", {}).get("related_products", [])),
            "bundles": list(record.get("merchandising", {}).get("bundles", [])),
        },
        "landing_page_requirements": landing_requirements,
        "supported_differentiators": differentiators,
    }


def validate_commercial(commercial: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not commercial.get("angle"):
        errors.append("Commercial angle is required")
    if not commercial.get("offer_eligibility"):
        errors.append("Offer eligibility is required")
    if commercial.get("price_guardrail") == "blocked_until_price_approved":
        errors.append("Commercial release is blocked until price approval")
    return errors
