"""MVQueen governed content intelligence V1.

Consumes only a canonical, QA-passed product record and produces deterministic
customer-facing content drafts. The module never publishes and never fabricates
product facts. Factual details are drawn only from verified source_truth facts.
"""
from __future__ import annotations

import hashlib
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


def _stable_seed(value: str) -> int:
    raw = _text(value) or "mvqueen"
    return int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8], 16)


def _choose(items: List[str], key: str, salt: str) -> str:
    digest = hashlib.sha256(f"{_stable_seed(key)}:{salt}".encode("utf-8")).digest()
    return items[int.from_bytes(digest[:4], "big") % len(items)]


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
        "catalog.focus_keyword": {
            "type": "single_line_text_field",
            "value": _text(seo.get("primary_keyword")),
            "source": "canonical_seo",
        },
        "catalog.long_tail_keywords": {
            "type": "list.single_line_text_field",
            "value": [x for x in seo.get("long_tail_keywords", []) if _text(x)],
            "source": "canonical_seo",
        },
        "catalog.seo_keywords": {
            "type": "list.single_line_text_field",
            "value": [
                x
                for x in [
                    seo.get("primary_keyword"),
                    *seo.get("secondary_keywords", []),
                    *seo.get("long_tail_keywords", []),
                ]
                if _text(x)
            ],
            "source": "canonical_seo",
        },
        "catalog.highlights": {
            "type": "list.single_line_text_field",
            "value": [
                _text(x)
                for x in [*copy.get("features", []), *copy.get("benefits", [])]
                if _text(x)
            ][:6],
            "source": "canonical_copy",
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
    key = product_type.lower()

    description = _choose(
        [
            (
                f"Explore the MVQueen {product_type.lower()} edit through a considered lens of modern femininity, "
                "polished simplicity, and intentional styling. Every product keeps factual details grounded in "
                "verified source information while the collection holds a clear, cohesive point of view."
            ),
            (
                f"The MVQueen {product_type.lower()} edit brings together pieces chosen for quiet confidence, "
                "refined presentation, and personal expression. Product claims stay tied to verified details; "
                "the editorial layer gives the collection its warm, distinctly MVQueen perspective."
            ),
            (
                f"Discover MVQueen {product_type.lower()} with a curated balance of modern elegance and everyday ease. "
                "The collection is built to feel composed rather than crowded, with verified product information "
                "supporting every customer-facing detail."
            ),
            (
                f"MVQueen approaches {product_type.lower()} as part of a complete feminine edit: intentional, polished, "
                "and easy to make personal. The collection keeps product facts precise while the presentation brings "
                "warmth, restraint, and a consistent editorial direction."
            ),
            (
                f"Shop the MVQueen {product_type.lower()} edit with a focus on considered choices and clear product detail. "
                "The assortment pairs verified source information with refined styling language so the experience feels "
                "curated, useful, and confidently feminine."
            ),
        ],
        key,
        "collection-description",
    )

    meta_description = _choose(
        [
            f"Explore MVQueen {product_type.lower()} with verified product details, polished styling, and a considered feminine point of view.",
            f"Discover the MVQueen {product_type.lower()} edit: clear product details, modern elegance, and intentional styling.",
            f"Shop MVQueen {product_type.lower()} through a curated edit grounded in verified details and refined everyday style.",
        ],
        key,
        "collection-meta",
    )

    return {
        "name": name,
        "slug": _slug(name),
        "description": description,
        "seo_title": _clip(f"{name} | MVQueen", 60),
        "meta_description": _clip(meta_description, 160),
        "primary_keyword": primary_keyword,
        "status": "DRAFT_REVIEW",
    }


def _blog(record: Dict[str, Any], facts: Dict[str, Any]) -> Dict[str, Any]:
    product_type = _text(record.get("category", {}).get("product_type")) or "product"
    title = _text(record.get("copy", {}).get("title"))
    primary_keyword = _text(record.get("seo", {}).get("primary_keyword")) or product_type.lower()
    handle = _text(record.get("identity", {}).get("handle"))
    product_id = _text(record.get("identity", {}).get("product_id"))
    key = product_id or handle or title or product_type

    labeled_details = [
        ("material", _fact(facts, "material", "fabric")),
        ("color", _fact(facts, "color", "shade")),
        ("finish", _fact(facts, "finish")),
        ("main stone", _fact(facts, "main_stone")),
        ("size", _fact(facts, "size", "dimensions", "main_stone_size")),
        ("ingredient", _fact(facts, "ingredient", "key_ingredient", "ingredients")),
    ]
    detail_bits = [f"{label}: {value}" for label, value in labeled_details if value]
    detail_sentence = (
        f"For {title}, verified product details include " + "; ".join(detail_bits[:4]) + "."
        if detail_bits
        else f"For {title}, use the verified product details on the product page as the factual reference."
    )

    blog_title = _choose(
        [
            f"{title}: A Considered Guide to the Details That Matter",
            f"A Closer Look at {title}",
            f"How to Evaluate {title} Before You Choose",
            f"{title}: What the Verified Details Tell You",
            f"Choosing {product_type.title()} with Intention: {title}",
        ],
        key,
        "blog-title",
    )

    target = f"/products/{handle}" if handle else f"product:{product_id}"

    first_heading = _choose(
        [
            f"What to look for in a {product_type.lower()}",
            "Start with the details that matter",
            f"How to read the details on a {product_type.lower()}",
        ],
        key,
        "blog-heading-1",
    )
    second_heading = _choose(
        [
            "Use verified details as the foundation",
            "Separate product facts from editorial framing",
            "Let verified information lead",
        ],
        key,
        "blog-heading-2",
    )
    third_heading = _choose(
        [
            "Make the final choice personal",
            "Bring the details back to your own priorities",
            "Choose for the way it fits your life",
        ],
        key,
        "blog-heading-3",
    )

    first_intro = _choose(
        [
            f"Start with what matters to the way you plan to use a {product_type.lower()}: verified materials, dimensions, color, fit, finish, or ingredient information where those details are available.",
            f"A confident choice begins with clear information. For a {product_type.lower()}, focus first on the verified details that affect how it looks, fits, feels, or belongs in your routine.",
            f"Before the styling language, read the facts. A {product_type.lower()} is easier to evaluate when materials, color, dimensions, fit, finish, or ingredients are clearly identified where available.",
        ],
        key,
        "blog-intro",
    )

    final_guidance = _choose(
        [
            f"Compare the verified details with your own priorities, then use the editorial presentation to decide whether the {product_type.lower()} fits the look, routine, or moment you have in mind.",
            f"Use the factual details to narrow the decision, then let your own style, routine, and intended use determine whether this {product_type.lower()} earns a place in your edit.",
            f"The final decision should come back to your own priorities: how the verified details align with the way you plan to wear, use, or style this {product_type.lower()}.",
        ],
        key,
        "blog-final-guidance",
    )

    sections = [
        {
            "heading": first_heading,
            "paragraphs": [
                first_intro,
                "MVQueen keeps factual specifications separate from editorial framing so product understanding comes before persuasion.",
            ],
        },
        {
            "heading": second_heading,
            "paragraphs": [
                detail_sentence,
                "When a specification is not verified, it should not be treated as a fact. That keeps the product story polished without turning brand language into an unsupported promise.",
            ],
        },
        {
            "heading": third_heading,
            "paragraphs": [
                final_guidance,
                f"Explore {title} for the complete product page, imagery, and currently available specifications.",
            ],
        },
    ]

    dek = _choose(
        [
            f"A practical MVQueen guide to evaluating {primary_keyword} through verified details, personal priorities, and intentional style.",
            f"A closer look at {primary_keyword}, grounded in verified product information and a more considered way to choose.",
            f"Use verified details, personal priorities, and MVQueen editorial guidance to evaluate {primary_keyword} with confidence.",
        ],
        key,
        "blog-dek",
    )

    meta_description = _choose(
        [
            f"Learn how to evaluate {primary_keyword} using verified product details, personal priorities, and MVQueen's considered editorial approach.",
            f"Explore what matters when choosing {primary_keyword}: verified details, personal use, and clear MVQueen editorial guidance.",
            f"A practical MVQueen guide to {primary_keyword}, focused on verified information and intentional product selection.",
        ],
        key,
        "blog-meta",
    )

    return {
        "title": blog_title,
        "slug": _slug(blog_title),
        "dek": dek,
        "sections": sections,
        "internal_links": [{"anchor": title, "target": target, "type": "product"}],
        "primary_keyword": primary_keyword,
        "meta_description": _clip(meta_description, 160),
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
