"""MVQueen Creative Intelligence V1.

Generates deterministic creative briefs from canonical product intelligence.
It does not publish ads or invent product evidence.
"""
from __future__ import annotations

from typing import Any, Dict, List


def _facts(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        str(f.get("name", "")).lower(): f.get("value")
        for f in record.get("source_truth", {}).get("facts", [])
        if f.get("verified") is True and f.get("name")
    }


def build_creative(record: Dict[str, Any]) -> Dict[str, Any]:
    facts = _facts(record)
    intelligence = record.get("intelligence", {})
    copy = record.get("copy", {})
    commercial = record.get("commercial", {})
    title = copy.get("title") or record.get("identity", {}).get("product_id", "MVQueen product")
    desire = intelligence.get("desire") or "feel polished, confident, and intentional"
    angle = commercial.get("angle") or "Show how the product fits the customer's intended use."
    proof = list(commercial.get("proof_available", []))
    fact_hint = next(iter(facts.values()), "verified product detail")

    claim_constraints = [
        "Use verified product facts only",
        "Do not invent testimonials, statistics, certifications, or guarantees",
        "Do not imply unsupported medical, therapeutic, or superiority claims",
    ]

    briefs: List[Dict[str, Any]] = [
        {
            "channel": "Meta",
            "asset_type": "static_or_carousel",
            "brief": f"Lead with {desire}. Feature {title}; visually emphasize {fact_hint}. Angle: {angle}",
            "hook": f"A more intentional way to approach {desire}.",
            "cta": "Shop MVQueen",
            "funnel_stage": "consideration",
            "testing_variable": "hook",
            "claim_constraints": claim_constraints,
        },
        {
            "channel": "TikTok",
            "asset_type": "short_video",
            "brief": f"Open in customer context, reveal {title}, then demonstrate the relevant verified detail: {fact_hint}.",
            "hook": "Show the moment the look comes together.",
            "cta": "Shop MVQueen",
            "funnel_stage": "discovery",
            "testing_variable": "opening_visual",
            "claim_constraints": claim_constraints,
        },
        {
            "channel": "UGC",
            "asset_type": "concept",
            "brief": f"Concept scenario: customer prepares for the intended use and naturally introduces {title}. Focus on experience and verified details, not fabricated results.",
            "hook": "Get ready with me for the moment that calls for a little more polish.",
            "cta": "Explore MVQueen",
            "funnel_stage": "consideration",
            "testing_variable": "context",
            "claim_constraints": claim_constraints + ["Clearly label simulated UGC as a concept"],
        },
        {
            "channel": "Email",
            "asset_type": "product_feature",
            "brief": f"Tell a concise product story around {desire}, then support it with verified evidence: {', '.join(proof[:3]) or 'verified product details'}.",
            "hook": title,
            "cta": "Shop MVQueen",
            "funnel_stage": "conversion",
            "testing_variable": "angle",
            "claim_constraints": claim_constraints,
        },
        {
            "channel": "SMS",
            "asset_type": "short_message",
            "brief": f"Concise product reminder for {title}; use only approved offer information and verified product value.",
            "hook": title,
            "cta": "Shop now",
            "funnel_stage": "conversion",
            "testing_variable": "cta",
            "claim_constraints": claim_constraints,
        },
    ]

    return {"assets": briefs}


def validate_creative(creative: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    assets = creative.get("assets", [])
    if not assets:
        errors.append("At least one creative asset brief is required")
    for index, asset in enumerate(assets):
        for field in ("channel", "asset_type", "brief", "claim_constraints"):
            if not asset.get(field):
                errors.append(f"Creative asset {index} missing {field}")
        if asset.get("testing_variable") not in {"hook", "angle", "opening_visual", "proof_format", "offer_presentation", "cta", "context"}:
            errors.append(f"Creative asset {index} has invalid testing_variable")
    return errors
