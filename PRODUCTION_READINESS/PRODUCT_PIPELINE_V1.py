"""MVQUEEN canonical product production pipeline V1.

Pure standard-library implementation. Source facts are preserved, generated copy
may interpret them, but cannot invent unsupported factual attributes. Brand voice
is a production requirement rather than an optional prompt preference.
"""
from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Dict, List, Tuple

STAGES = [
    "RAW", "NORMALIZED", "INTELLIGENCE_READY", "COPY_READY", "SEO_READY",
    "MERCH_READY", "COMMERCIAL_READY", "CREATIVE_READY", "QA_PASSED",
    "PRODUCTION_READY",
]
PROTECTED_FIELDS = {
    "id", "product_id", "handle", "sku", "variant_id", "variant_sku",
    "inventory", "inventory_quantity", "inventory_item_id", "option1",
    "option2", "option3",
}
CLAIM_TERMS = re.compile(
    r"\b(cures?|treats?|prevents?|guaranteed?|clinically proven|medical[- ]grade|"
    r"hypoallergenic|non[- ]toxic|chemical[- ]free|organic|certified|best|#1|"
    r"100%|instant|permanent|never|always)\b", re.I
)
ROBOTIC_PHRASES = re.compile(
    r"\b(versatile and stylish|perfect for any occasion|elevate your everyday look|"
    r"elevate your wardrobe|must[- ]have|game[- ]changer|level up|designed to elevate|"
    r"whether you'?re dressing up or down|this versatile)\b", re.I
)
MVQUEEN_SIGNALS = (
    "confidence", "confident", "feminine", "elevated", "modern", "polished",
    "intentional", "effortless", "luxury", "mvqueen",
)


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _fact_map(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        _text(f.get("name")): f.get("value")
        for f in record.get("source_truth", {}).get("facts", [])
        if f.get("verified") is True and _text(f.get("name"))
    }


def _verified(record: Dict[str, Any], name: str) -> Any:
    return _fact_map(record).get(name)


def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize presentation without changing protected source values."""
    out = deepcopy(raw)
    out.setdefault("schema_version", "1.0")
    out.setdefault("source_truth", {}).setdefault("facts", [])
    out.setdefault("protected_fields", {}).setdefault("fields", sorted(PROTECTED_FIELDS))
    out.setdefault("images", {}).setdefault("items", [])
    out["status"] = "NORMALIZED"
    return out


def build_intelligence(record: Dict[str, Any]) -> None:
    facts = _fact_map(record)
    category = _text(record.get("category", {}).get("product_type")) or "product"
    material = _text(facts.get("material"))
    color = _text(facts.get("color"))
    use = _text(facts.get("use_context"))
    record["intelligence"] = {
        "customer_need": f"Find a {category} that fits her intended use and personal style.",
        "desire": "Feel polished, confident, and intentionally styled.",
        "use_context": use or "Everyday styling and personal use.",
        "positioning": "MVQueen confidence-driven style with an elevated, modern finish.",
        "supported_benefits": [x for x in [f"{material} construction" if material else "", f"{color} finish" if color else ""] if x],
        "differentiators": [],
        "objections": [],
        "collection_candidates": [category],
        "cross_sell_candidates": [],
    }
    record["status"] = "INTELLIGENCE_READY"


def build_copy(record: Dict[str, Any]) -> None:
    facts = _fact_map(record)
    product_type = _text(record.get("category", {}).get("product_type")) or "Essential"
    material = _text(facts.get("material"))
    color = _text(facts.get("color"))
    use = _text(facts.get("use_context")) or "everyday use"
    title_parts = [x for x in ["MVQueen", color, product_type] if x]
    title = " — ".join(title_parts)
    opening = f"Meet the {product_type.lower()} made for {use}."
    if material:
        opening = f"Meet the {material.lower()} {product_type.lower()} made for {use}."
    short = f"{opening} A polished, confidence-driven piece with the modern ease MVQueen is known for."
    details = [f"Product type: {product_type}."]
    if material:
        details.append(f"Material: {material}.")
    if color:
        details.append(f"Color: {color}.")
    record["copy"] = {
        "title": title,
        "short_description": short,
        "description": " ".join(details) + " Designed for intentional styling, with a refined finish that keeps the focus on her.",
        "benefits": record.get("intelligence", {}).get("supported_benefits", []),
        "features": details,
        "cta": "Shop MVQueen",
    }
    record["status"] = "COPY_READY"


def build_seo(record: Dict[str, Any]) -> None:
    title = _text(record.get("copy", {}).get("title"))
    product_type = _text(record.get("category", {}).get("product_type")) or "women's style"
    keyword = product_type.lower()
    seo_title = f"MVQueen | {title}" if title else f"MVQueen | {product_type}"
    meta = f"Shop {title or product_type} from MVQueen—confidence-driven style with a polished, modern finish."
    if len(meta) > 160:
        meta = meta[:157].rstrip(" ,—-") + "..."
    record["seo"] = {
        "seo_title": seo_title,
        "meta_description": meta,
        "handle_recommendation": re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") if title else "",
        "primary_keyword": keyword,
        "secondary_keywords": [],
        "alt_texts": [],
    }
    for image in record.get("images", {}).get("items", []):
        alt = title or product_type
        image["alt"] = alt
        record["seo"]["alt_texts"].append(alt)
    record["status"] = "SEO_READY"


def build_merchandising(record: Dict[str, Any]) -> None:
    category = _text(record.get("category", {}).get("product_type")) or "Essentials"
    record["merchandising"] = {
        "collections": [category],
        "tags": ["MVQueen", category],
        "related_products": [],
        "bundles": [],
    }
    record["status"] = "MERCH_READY"


def build_commercial(record: Dict[str, Any]) -> None:
    supported = record.get("intelligence", {}).get("supported_benefits", [])
    record["commercial"] = {
        "angle": "Confidence through intentional, elevated styling.",
        "proof_available": supported,
        "offer_eligibility": [],
        "price_guardrail": "Publish only an explicitly approved price.",
        "trust_inputs": [],
        "objections_responses": [],
        "funnel_stage": "product",
    }
    record["status"] = "COMMERCIAL_READY"


def build_creative(record: Dict[str, Any]) -> None:
    title = _text(record.get("copy", {}).get("title")) or "product"
    record["creative"] = {"assets": [
        {"channel": "meta", "asset_type": "paid_static", "brief": f"Create an identity-led visual for {title}.", "claim_constraints": []},
        {"channel": "tiktok", "asset_type": "short_video", "brief": f"Show {title} in a concise styling/use context.", "claim_constraints": []},
        {"channel": "email", "asset_type": "product_feature", "brief": f"Introduce {title} with verified product details only.", "claim_constraints": []},
    ]}
    record["status"] = "CREATIVE_READY"


def validate(record: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    for key in ("identity", "source_truth", "category", "pricing", "images", "intelligence", "copy", "seo", "merchandising", "commercial", "creative"):
        if key not in record:
            errors.append(f"Missing required section: {key}")
    if not _text(record.get("identity", {}).get("product_id")):
        errors.append("Missing identity.product_id")
    if not _text(record.get("identity", {}).get("source_name")):
        errors.append("Missing identity.source_name")
    if not _text(record.get("pricing", {}).get("approved_publish_price")):
        errors.append("No approved_publish_price; recommendation cannot publish automatically")
    for field in ("title", "short_description", "description"):
        if not _text(record.get("copy", {}).get(field)):
            errors.append(f"Missing copy.{field}")
    if not _text(record.get("seo", {}).get("seo_title")):
        errors.append("Missing seo.seo_title")
    if not _text(record.get("seo", {}).get("primary_keyword")):
        errors.append("Missing seo.primary_keyword")
    meta = _text(record.get("seo", {}).get("meta_description"))
    if not meta or len(meta) > 160:
        errors.append("seo.meta_description must be 1–160 characters")
    for image in record.get("images", {}).get("items", []):
        if not _text(image.get("alt")):
            errors.append("Every published image requires ALT text")
    generated_text = " ".join([
        _text(record.get("copy", {}).get("title")),
        _text(record.get("copy", {}).get("short_description")),
        _text(record.get("copy", {}).get("description")),
        _text(record.get("commercial", {}).get("angle")),
    ])
    suspicious = CLAIM_TERMS.findall(generated_text)
    if suspicious:
        errors.append("Unsupported/high-risk claim language detected: " + ", ".join(sorted(set(suspicious), key=str.lower)))
    robotic = ROBOTIC_PHRASES.findall(generated_text)
    if robotic:
        errors.append("Generic/robotic marketing language detected: " + ", ".join(sorted(set(robotic), key=str.lower)))
    signal_count = sum(1 for signal in MVQUEEN_SIGNALS if re.search(r"\b" + re.escape(signal) + r"\b", generated_text, re.I))
    if signal_count < 2:
        errors.append("MVQueen brand-voice signal threshold not met")
    if len(meta) < 150:
        warnings.append("Meta description is below the preferred 150–160 character range")
    return errors, warnings


def run(raw: Dict[str, Any]) -> Dict[str, Any]:
    record = normalize(raw)
    build_intelligence(record)
    build_copy(record)
    build_seo(record)
    build_merchandising(record)
    build_commercial(record)
    build_creative(record)
    errors, warnings = validate(record)
    record["qa"] = {"errors": errors, "warnings": warnings, "passed": not errors}
    record["measurement"] = {
        "events": ["ViewContent", "AddToCart", "BeginCheckout", "Purchase"],
        "primary_kpi": "Purchase",
        "secondary_kpis": ["ATC rate", "conversion rate", "AOV", "CAC", "ROAS"],
    }
    record["status"] = "QA_PASSED" if not errors else "CREATIVE_READY"
    if not errors:
        record["status"] = "PRODUCTION_READY"
    return record


if __name__ == "__main__":
    import json, sys
    payload = json.load(sys.stdin)
    print(json.dumps(run(payload), indent=2, ensure_ascii=False))
