"""MVQUEEN governed content intelligence V1.

Consumes only a canonical, QA-passed product record and produces deterministic
customer-facing content drafts. The module never publishes and never fabricates
product facts. Factual details are drawn only from verified source_truth facts.
"""
from __future__ import annotations

import json
import re
from copy import deepcopy
from typing import Any, Dict, List

HIGH_RISK_CLAIMS = re.compile(
    r"\b(cures?|treats?|prevents?|guaranteed?|clinically proven|medical[- ]grade|"
    r"hypoallergenic|non[- ]toxic|chemical[- ]free|#1|100%|instant|permanent|"
    r"best seller)\b",
    re.I,
)

FACT_LABELS = {
    "material": "Material",
    "fabric": "Fabric",
    "color": "Color",
    "shade": "Shade",
    "finish": "Finish",
    "texture": "Texture",
    "size": "Size",
    "dimensions": "Dimensions",
    "fit": "Fit",
    "occasion": "Occasion",
    "use_context": "Use context",
    "usage": "Usage",
    "ingredient": "Ingredient",
    "key_ingredient": "Key ingredient",
    "ingredients": "Ingredients",
    "care": "Care",
    "care_instructions": "Care instructions",
    "how_to_use": "How to use",
    "main_stone": "Main stone",
    "main_stone_size": "Main stone size",
    "total_weight": "Total weight",
    "creation": "Creation",
    "design_code": "Design code",
    "item_code": "Item code",
}

METAFIELD_FACT_KEYS = {
    "material": ("attributes", "material"),
    "fabric": ("attributes", "fabric"),
    "color": ("attributes", "color"),
    "shade": ("attributes", "shade"),
    "finish": ("attributes", "finish"),
    "texture": ("attributes", "texture"),
    "size": ("attributes", "size"),
    "dimensions": ("attributes", "dimensions"),
    "fit": ("attributes", "fit"),
    "occasion": ("attributes", "occasion"),
    "ingredient": ("attributes", "ingredient"),
    "key_ingredient": ("attributes", "key_ingredient"),
    "ingredients": ("attributes", "ingredients"),
    "care": ("content", "care_instructions"),
    "care_instructions": ("content", "care_instructions"),
    "how_to_use": ("content", "how_to_use"),
}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _clip(value: str, limit: int) -> str:
    clean = re.sub(r"\s+", " ", value).strip()
    if len(clean) <= limit:
        return clean
    if limit <= 1:
        return clean[:limit]
    return clean[: limit - 1].rstrip(" ,—-") + "…"


def _verified_facts(record: Dict[str, Any]) -> Dict[str, Any]:
    facts: Dict[str, Any] = {}
    for fact in record.get("source_truth", {}).get("facts", []):
        name = _text(fact.get("name")).lower()
        if name and fact.get("verified") is True:
            facts[name] = deepcopy(fact.get("value"))
    return facts


def _fact(facts: Dict[str, Any], *names: str) -> str:
    for name in names:
        value = _text(facts.get(name.lower()))
        if value:
            return value
    return ""


def _require_production_record(record: Dict[str, Any]) -> None:
    if record.get("status") != "PRODUCTION_READY":
        raise ValueError("Content generation requires a PRODUCTION_READY canonical record")
    qa = record.get("qa", {})
    if qa.get("passed") is not True or qa.get("errors"):
        raise ValueError("Content generation requires a canonical record with passed QA")
    if not _text(record.get("identity", {}).get("product_id")):
        raise ValueError("Content generation requires identity.product_id")
    if not _text(record.get("copy", {}).get("title")):
        raise ValueError("Content generation requires copy.title")


def _detail_rows(facts: Dict[str, Any]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    seen: set[str] = set()
    for key, label in FACT_LABELS.items():
        if key in seen:
            continue
        value = _text(facts.get(key))
        if not value:
            continue
        rows.append({"label": label, "value": value, "source": "verified_product_fact"})
        seen.add(key)
    return rows


def _faq(record: Dict[str, Any], facts: Dict[str, Any]) -> List[Dict[str, str]]:
    title = _text(record.get("copy", {}).get("title"))
    product_type = _text(record.get("category", {}).get("product_type")) or "product"
    faq: List[Dict[str, str]] = [
        {
            "question": f"What is {title}?",
            "answer": f"{title} is an MVQueen {product_type.lower()} presented with verified product details and MVQueen editorial copy.",
        }
    ]

    material = _fact(facts, "material", "fabric")
    if material:
        faq.append({
            "question": "What material or fabric is listed?",
            "answer": f"The verified product information lists {material}.",
        })

    color = _fact(facts, "color", "shade")
    if color:
        faq.append({
            "question": "What color or shade is listed?",
            "answer": f"The verified product information lists {color}.",
        })

    size = _fact(facts, "size", "dimensions", "main_stone_size")
    if size:
        faq.append({
            "question": "What size information is available?",
            "answer": f"The verified product information lists {size}.",
        })

    ingredients = _fact(facts, "ingredients", "ingredient", "key_ingredient")
    if ingredients:
        faq.append({
            "question": "What ingredient information is available?",
            "answer": f"The verified product information lists {ingredients}.",
        })

    how_to_use = _fact(facts, "how_to_use", "usage", "use_context")
    if how_to_use:
        faq.append({
            "question": "How is this product intended to be used?",
            "answer": f"The verified product information describes its use as: {how_to_use}.",
        })

    care = _fact(facts, "care_instructions", "care")
    if care:
        faq.append({
            "question": "What care information is available?",
            "answer": f"The verified product information states: {care}.",
        })

    faq.append({
        "question": "Where should I check final product specifications?",
        "answer": "Review the product details shown on the product page before purchasing. MVQueen does not add unsupported specifications or performance claims.",
    })
    return faq


def _metafields(record: Dict[str, Any], facts: Dict[str, Any], faq: List[Dict[str, str]]) -> Dict[str, Dict[str, Any]]:
    copy = record.get("copy", {})
    seo = record.get("seo", {})
    fields: Dict[str, Dict[str, Any]] = {
        "catalog.short_description": {
            "type": "single_line_text_field",
            "value": _text(copy.get("short_description")),
            "source": "canonical_copy",
        },
        "catalog.seo_keywords": {
            "type": "list.single_line_text_field",
            "value": [x for x in [seo.get("primary_keyword"), *seo.get("secondary_keywords", [])] if _text(x)],
            "source": "canonical_seo",
        },
        "catalog.review_status": {
            "type": "single_line_text_field",
            "value": "ready",
            "source": "canonical_qa",
        },
        "content.faq": {
            "type": "json",
            "value": faq,
            "source": "canonical_content",
        },
    }

    for fact_key, (namespace, metafield_key) in METAFIELD_FACT_KEYS.items():
        value = facts.get(fact_key)
        if value is None or not _text(value):
            continue
        fields[f"{namespace}.{metafield_key}"] = {
            "type": "single_line_text_field",
            "value": deepcopy(value),
            "source": f"verified_fact:{fact_key}",
        }
    return fields


def _product_page(record: Dict[str, Any], facts: Dict[str, Any], faq: List[Dict[str, str]]) -> Dict[str, Any]:
    copy = record.get("copy", {})
    seo = record.get("seo", {})
    return {
        "title": _text(copy.get("title")),
        "short_description": _text(copy.get("short_description")),
        "description": _text(copy.get("description")),
        "benefits": list(copy.get("benefits", [])),
        "features": list(copy.get("features", [])),
        "details": _detail_rows(facts),
        "faq": faq,
        "cta": _text(copy.get("cta")) or "Discover the MVQueen edit.",
        "seo_title": _text(seo.get("seo_title")),
        "meta_description": _text(seo.get("meta_description")),
        "image_alt_text": list(seo.get("alt_texts", [])),
    }


def _collection(record: Dict[str, Any]) -> Dict[str, Any]:
    product_type = _text(record.get("category", {}).get("product_type")) or "Essentials"
    primary_keyword = _text(record.get("seo", {}).get("primary_keyword")) or product_type.lower()
    name = f"MVQueen {product_type} Edit"
    description = (
        f"Explore the MVQueen {product_type.lower()} edit, curated around modern femininity, "
        "polished styling, and a clear point of view. Product-specific details remain grounded "
        "in verified source information, while the collection brings those pieces together in "
        "a consistent MVQueen experience designed for confident, intentional shopping."
    )
    return {
        "name": name,
        "slug": _slug(name),
        "description": description,
        "seo_title": _clip(f"{name} | MVQueen", 60),
        "meta_description": _clip(
            f"Explore MVQueen {product_type.lower()} with polished editorial presentation, verified product details, and confidence-driven style.",
            160,
        ),
        "primary_keyword": primary_keyword,
        "status": "DRAFT_REVIEW",
    }


def _blog(record: Dict[str, Any], facts: Dict[str, Any]) -> Dict[str, Any]:
    product_type = _text(record.get("category", {}).get("product_type")) or "product"
    title = _text(record.get("copy", {}).get("title"))
    primary_keyword = _text(record.get("seo", {}).get("primary_keyword")) or product_type.lower()
    handle = _text(record.get("identity", {}).get("handle"))
    material = _fact(facts, "material", "fabric")
    color = _fact(facts, "color", "shade")
    detail_bits = [x for x in [material, color] if x]
    detail_sentence = (
        f"For {title}, verified product details include {', '.join(detail_bits)}."
        if detail_bits
        else f"For {title}, use the verified product details on the product page as the factual reference."
    )
    blog_title = f"A Considered Guide to Choosing {product_type.title()}"
    target = f"/products/{handle}" if handle else f"product:{_text(record.get('identity', {}).get('product_id'))}"
    sections = [
        {
            "heading": f"What to look for in a {product_type.lower()}",
            "paragraphs": [
                f"Start with the details that matter to the way you plan to use a {product_type.lower()}: verified materials, dimensions, color, fit, or ingredient information where those details are available.",
                "MVQueen separates factual specifications from editorial language so you can understand both what the product is and how it fits the brand experience.",
            ],
        },
        {
            "heading": "Use verified details as the foundation",
            "paragraphs": [
                detail_sentence,
                "When a specification is not verified, it should not be treated as a fact. That keeps the product story polished without turning marketing language into an unsupported promise.",
            ],
        },
        {
            "heading": "Make the final choice personal",
            "paragraphs": [
                f"Compare the verified details with your own priorities, then use the editorial presentation to decide whether the {product_type.lower()} fits the look, routine, or moment you have in mind.",
                f"Explore {title} for the complete product page, imagery, and available specifications.",
            ],
        },
    ]
    return {
        "title": blog_title,
        "slug": _slug(blog_title),
        "dek": f"A practical MVQueen guide to evaluating {primary_keyword} through verified details, personal use, and intentional style.",
        "sections": sections,
        "internal_links": [{"anchor": title, "target": target, "type": "product"}],
        "primary_keyword": primary_keyword,
        "meta_description": _clip(
            f"Learn how to evaluate {primary_keyword} using verified product details, personal priorities, and MVQueen's polished editorial approach.",
            160,
        ),
        "status": "DRAFT_REVIEW",
        "auto_publish": False,
    }


def _site_faq(record: Dict[str, Any], faq: List[Dict[str, str]]) -> Dict[str, Any]:
    title = _text(record.get("copy", {}).get("title"))
    return {
        "topic": title,
        "entries": faq,
        "status": "DRAFT_REVIEW",
        "auto_publish": False,
    }


def _content_text(content: Dict[str, Any]) -> str:
    return json.dumps(content, sort_keys=True, ensure_ascii=False, default=str)


def validate_content_suite(content: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ("product_page", "metafields", "collection", "blog", "site_faq")
    for key in required:
        if not content.get(key):
            errors.append(f"Missing content section: {key}")

    text = _content_text(content)
    claims = HIGH_RISK_CLAIMS.findall(text)
    if claims:
        errors.append(
            "High-risk or unsupported claim language detected in generated content: "
            + ", ".join(sorted(set(claims), key=str.lower))
        )

    if content.get("blog", {}).get("auto_publish") is not False:
        errors.append("Blog content must remain review-only")
    if content.get("site_faq", {}).get("auto_publish") is not False:
        errors.append("FAQ content must remain review-only")

    forbidden_metafields = {
        "attributes.origin",
        "attributes.shelf_life",
        "trust.certifications",
        "catalog.badge",
        "custom.origin",
        "custom.shelf_life",
        "custom.certifications",
        "custom.badge",
    }
    present = forbidden_metafields.intersection(content.get("metafields", {}))
    if present:
        errors.append("Unsafe legacy metafields are not allowed: " + ", ".join(sorted(present)))
    return errors


def generate_content_suite(record: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a reviewable content suite from one canonical product record."""
    _require_production_record(record)
    facts = _verified_facts(record)
    faq = _faq(record, facts)

    content: Dict[str, Any] = {
        "content_version": "mvq-content-v1",
        "product_id": _text(record.get("identity", {}).get("product_id")),
        "product_page": _product_page(record, facts, faq),
        "metafields": _metafields(record, facts, faq),
        "collection": _collection(record),
        "blog": _blog(record, facts),
        "site_faq": _site_faq(record, faq),
        "governance": {
            "fact_policy": "verified_source_truth_only",
            "protected_fields_mutated": False,
            "auto_publish": False,
        },
    }
    errors = validate_content_suite(content)
    content["qa"] = {
        "errors": errors,
        "passed": not errors,
        "status": "CONTENT_READY_FOR_REVIEW" if not errors else "CONTENT_BLOCKED",
    }
    return content


if __name__ == "__main__":
    import sys

    payload = json.load(sys.stdin)
    print(json.dumps(generate_content_suite(payload), indent=2, ensure_ascii=False))
