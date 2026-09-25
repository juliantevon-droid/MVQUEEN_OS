"""MVQueen canonical product production pipeline V1.

Pure standard-library implementation. Source facts are preserved, generated copy
may interpret them, but cannot invent unsupported factual attributes. Brand voice
is a production requirement rather than an optional prompt preference.
"""
from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Dict, List, Tuple

try:
    from .MVQUEEN_EDITORIAL_INTELLIGENCE_V1 import generate, validate_editorial
    from .COMMERCIAL_INTELLIGENCE_V1 import build_commercial, validate_commercial
    from .CREATIVE_INTELLIGENCE_V1 import build_creative, validate_creative
    from .BRAND_WORLD_V1 import classify_brand_world
except ImportError:
    from MVQUEEN_EDITORIAL_INTELLIGENCE_V1 import generate, validate_editorial
    from COMMERCIAL_INTELLIGENCE_V1 import build_commercial, validate_commercial
    from CREATIVE_INTELLIGENCE_V1 import build_creative, validate_creative
    from BRAND_WORLD_V1 import classify_brand_world

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
    r"100%|instant|permanent)\b", re.I
)
ROBOTIC_PHRASES = re.compile(
    r"\b(versatile and stylish|perfect for any occasion|elevate your everyday look|"
    r"elevate your wardrobe|must[- ]have|game[- ]changer|level up|designed to elevate|"
    r"whether you'?re dressing up or down|this versatile)\b", re.I
)
MVQUEEN_SIGNALS = (
    "confidence", "confident", "feminine", "elevated", "modern", "polished",
    "intentional", "effortless", "luxury", "mvqueen", "refined",
)
MISS_PRINCESS_SIGNALS = (
    "soft", "playful", "romantic", "bright", "color", "feminine",
    "expressive", "polished", "princess", "glamour",
)


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _fact_map(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        _text(f.get("name")): f.get("value")
        for f in record.get("source_truth", {}).get("facts", [])
        if f.get("verified") is True and _text(f.get("name"))
    }


def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
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
    brand = classify_brand_world(record)

    if brand["brand_world"] == "miss-princess":
        desire = "Feel expressive, feminine, polished, and free to play with color."
        positioning = "Miss.Princess soft glamour with playful color, romantic detail, and polished femininity."
    elif brand["brand_world"] == "mvqueen":
        desire = "Feel polished, confident, and intentionally styled."
        positioning = "MVQueen confidence-driven style with a refined, modern finish."
    else:
        desire = "Find the right brand-world fit from verified product details."
        positioning = "Brand-world assignment requires review before customer-facing publication."

    record["intelligence"] = {
        "customer_need": f"Find a {category} that fits her intended use and personal style.",
        "desire": desire,
        "use_context": use or "Everyday styling and personal use.",
        "positioning": positioning,
        "supported_benefits": [x for x in [f"{material} construction" if material else "", f"{color} finish" if color else ""] if x],
        "differentiators": [],
        "objections": [],
        "collection_candidates": [category],
        "cross_sell_candidates": [],
        **brand,
    }
    record["status"] = "INTELLIGENCE_READY"


def build_copy(record: Dict[str, Any]) -> None:
    editorial = generate(record)
    editorial.pop("_editorial_category", None)
    record["copy"] = editorial
    record["status"] = "COPY_READY"


def build_seo(record: Dict[str, Any]) -> None:
    """Build factual short-tail and long-tail SEO from verified product data."""
    title = _text(record.get("copy", {}).get("title"))
    category = record.get("category", {})
    product_type = _text(category.get("product_type")) or "women's style"
    category_name = _text(category.get("category"))
    subcategory = _text(category.get("subcategory"))
    facts = _fact_map(record)

    def first_fact(*names: str) -> str:
        for name in names:
            value = _text(facts.get(name))
            if value:
                return value
        return ""

    def unique(values: List[str]) -> List[str]:
        output: List[str] = []
        seen = set()
        for value in values:
            cleaned = re.sub(r"\s+", " ", _text(value)).strip(" ,-|")
            key = cleaned.casefold()
            if cleaned and key not in seen:
                seen.add(key)
                output.append(cleaned)
        return output

    material = first_fact("material", "fabric", "composition")
    color = first_fact("color", "shade")
    stone = first_fact("main_stone", "stone", "gemstone")
    size = first_fact("stone_size", "size", "dimensions")
    occasion = first_fact("occasion", "use_context")

    primary = product_type.lower()

    secondary_candidates = [
        subcategory.lower() if subcategory else "",
        category_name.lower() if category_name else "",
        f"{material} {product_type}".lower() if material else "",
        f"{color} {product_type}".lower() if color else "",
        f"{stone} {product_type}".lower() if stone else "",
    ]
    secondary = [
        value for value in unique(secondary_candidates)
        if value.casefold() != primary.casefold()
    ][:4]

    long_tail_candidates = [
        f"{color} {material} {product_type}" if color and material else "",
        f"{stone} {material} {product_type}" if stone and material else "",
        f"{size} {stone} {product_type}" if size and stone else "",
        f"{material} {product_type} for {occasion}" if material and occasion else "",
        title if len(title.split()) >= 4 else "",
        f"{title} {product_type}" if title and len(title.split()) < 4 else "",
    ]
    long_tail = [
        value.lower() for value in unique(long_tail_candidates)
        if value and value.casefold() != primary.casefold()
    ][:5]

    brand_name = _text(record.get("intelligence", {}).get("brand_name"))
    seo_suffix = f" | {brand_name}" if brand_name in {"MVQueen", "Miss.Princess"} else ""
    seo_base = title or product_type
    if len(seo_base) + len(seo_suffix) > 60:
        seo_base = seo_base[: 60 - len(seo_suffix)].rstrip(" ,—-|")
    seo_title = f"{seo_base}{seo_suffix}"

    factual_bits = unique([stone, material, color, size])
    if factual_bits:
        facts_phrase = ", ".join(factual_bits[:3])
        meta = f"Shop {title or product_type} from MVQueen, featuring {facts_phrase}. Explore verified product details, imagery, shipping and returns."
    else:
        meta = f"Shop {title or product_type} from MVQueen. Explore verified product details, imagery, shipping and returns before you choose."

    if len(meta) > 160:
        meta = meta[:157].rstrip(" ,—-") + "..."

    record["seo"] = {
        "seo_title": seo_title,
        "meta_description": meta,
        "handle_recommendation": re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") if title else "",
        "primary_keyword": primary,
        "secondary_keywords": secondary,
        "long_tail_keywords": long_tail,
        "alt_texts": [],
    }

    for index, image in enumerate(record.get("images", {}).get("items", []), start=1):
        alt_bits = unique([title or product_type, color, material, stone])
        alt = " — ".join(alt_bits[:3])
        if index > 1:
            alt = f"{alt} — view {index}"
        image["alt"] = alt[:120]
        record["seo"]["alt_texts"].append(image["alt"])

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


def build_commercial_stage(record: Dict[str, Any]) -> None:
    record["commercial"] = build_commercial(record)
    record["status"] = "COMMERCIAL_READY"


def build_creative_stage(record: Dict[str, Any]) -> None:
    record["creative"] = build_creative(record)
    record["measurement"] = {
        "events": ["ViewContent", "AddToCart", "BeginCheckout", "Purchase"],
        "primary_kpi": "Purchase",
        "secondary_kpis": ["ATC rate", "conversion rate", "AOV", "CAC", "ROAS"],
        "product_identifier": _text(record.get("identity", {}).get("product_id")),
        "tracking_key": f"product:{_text(record.get('identity', {}).get('product_id'))}",
    }
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
    measurement = record.get("measurement", {})
    if not _text(measurement.get("product_identifier")):
        errors.append("Missing measurement.product_identifier")
    if not _text(measurement.get("tracking_key")):
        errors.append("Missing measurement.tracking_key")
    if measurement.get("events") != ["ViewContent", "AddToCart", "BeginCheckout", "Purchase"]:
        errors.append("measurement.events must contain the canonical funnel events in order")
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
    brand_world = _text(record.get("intelligence", {}).get("brand_world"))
    if brand_world == "needs-review":
        errors.append("Brand-world routing requires review")
    elif brand_world == "miss-princess":
        signal_count = sum(
            1 for signal in MISS_PRINCESS_SIGNALS
            if re.search(r"\b" + re.escape(signal) + r"\b", generated_text, re.I)
        )
        if signal_count < 2:
            errors.append("Miss.Princess brand-voice signal threshold not met")
    else:
        signal_count = sum(
            1 for signal in MVQUEEN_SIGNALS
            if re.search(r"\b" + re.escape(signal) + r"\b", generated_text, re.I)
        )
        if signal_count < 2:
            errors.append("MVQueen brand-voice signal threshold not met")
    editorial_errors, editorial_warnings = validate_editorial(record)
    errors.extend(editorial_errors)
    warnings.extend(editorial_warnings)
    errors.extend(validate_commercial(record.get("commercial", {})))
    errors.extend(validate_creative(record.get("creative", {})))
    if len(meta) < 150:
        warnings.append("Meta description is below the preferred 150–160 character range")
    return errors, warnings


def run(raw: Dict[str, Any]) -> Dict[str, Any]:
    record = normalize(raw)
    build_intelligence(record)
    build_copy(record)
    build_seo(record)
    build_merchandising(record)
    build_commercial_stage(record)
    build_creative_stage(record)
    errors, warnings = validate(record)
    record["qa"] = {"errors": errors, "warnings": warnings, "passed": not errors}
    record["status"] = "QA_PASSED" if not errors else "CREATIVE_READY"
    if not errors:
        record["status"] = "PRODUCTION_READY"
    return record


if __name__ == "__main__":
    import json, sys
    payload = json.load(sys.stdin)
    print(json.dumps(run(payload), indent=2, ensure_ascii=False))
