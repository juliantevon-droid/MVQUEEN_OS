"""MVQueen Editorial Intelligence Engine V1.

Deterministic, category-aware customer-facing copy generation.
The engine only uses verified source facts as factual inputs. It does not
invent ingredients, materials, fit, performance, results, certifications,
or other product attributes.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Tuple

PLACEHOLDER_RE = re.compile(r"\{[^}]+\}|\b(?:describe|close with|insert|add)\s+(?:the\s+)?(?:benefits?|features?|details?|cta|keyword|persona)\b", re.I)
FORBIDDEN_COPY_RE = re.compile(
    r"\b(cures?|treats?|prevents?|guaranteed?|clinically proven|medical[- ]grade|"
    r"hypoallergenic|non[- ]toxic|chemical[- ]free|organic|certified|#1|100%|"
    r"instant|permanent|never|always)\b", re.I
)
GENERIC_RE = re.compile(
    r"\b(perfect for any occasion|versatile and stylish|must[- ]have|game[- ]changer|"
    r"elevate your everyday|elevate your wardrobe|level up|designed to elevate|"
    r"whether you'?re dressing up or down)\b", re.I
)

CATEGORY_ALIASES = {
    "fashion": {"dress", "top", "blouse", "shirt", "skirt", "pants", "jeans", "trousers", "jumpsuit", "romper", "bodysuit", "set", "coat", "jacket", "outerwear", "clothing", "apparel"},
    "skincare": {"skincare", "serum", "moisturizer", "cleanser", "toner", "mask", "cream", "lotion", "essence", "oil", "balm", "eye cream", "face wash"},
    "cosmetics": {"cosmetics", "makeup", "lipstick", "lip gloss", "lip liner", "foundation", "concealer", "blush", "bronzer", "highlighter", "eyeshadow", "mascara", "eyeliner", "palette"},
    "jewelry": {"jewelry", "necklace", "earrings", "bracelet", "ring", "anklet", "chain", "pendant", "accessory", "accessories"},
}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def verified_facts(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        _text(f.get("name")).lower(): f.get("value")
        for f in record.get("source_truth", {}).get("facts", [])
        if f.get("verified") is True and _text(f.get("name"))
    }


def _fact(facts: Dict[str, Any], *names: str) -> str:
    for name in names:
        value = _text(facts.get(name.lower()))
        if value:
            return value
    return ""


def classify_category(product_type: str) -> str:
    value = product_type.lower().strip()
    for category, aliases in CATEGORY_ALIASES.items():
        if value in aliases or any(alias in value for alias in aliases if len(alias) > 3):
            return category
    return "general"


def _seed(record: Dict[str, Any]) -> int:
    identity = record.get("identity", {})
    raw = _text(identity.get("product_id")) or _text(identity.get("sku")) or _text(record.get("category", {}).get("product_type"))
    return int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8], 16)


def _choose(items: List[str], record: Dict[str, Any], salt: str) -> str:
    digest = hashlib.sha256(f"{_seed(record)}:{salt}".encode()).digest()
    return items[int.from_bytes(digest[:4], "big") % len(items)]


def _safe_value(value: str, fallback: str = "") -> str:
    value = _text(value)
    if not value:
        return fallback
    return re.sub(r"\s+", " ", value).strip(" .,")


def _product_specific_detail(facts: Dict[str, Any], category: str) -> str:
    material = _safe_value(_fact(facts, "material", "fabric"))
    color = _safe_value(_fact(facts, "color", "shade"))
    finish = _safe_value(_fact(facts, "finish"))
    texture = _safe_value(_fact(facts, "texture"))
    size = _safe_value(_fact(facts, "size", "dimensions"))
    ingredient = _safe_value(_fact(facts, "ingredient", "key_ingredient"))
    if category == "skincare" and ingredient:
        return f"with {ingredient} listed among its verified ingredients"
    if category == "cosmetics" and finish:
        return f"with a {finish.lower()} finish"
    if texture:
        return f"with a {texture.lower()} texture"
    if material:
        return f"in {material.lower()}"
    if color:
        return f"in {color.lower()}"
    if size:
        return f"in the verified {size.lower()} specification"
    return ""


def generate(record: Dict[str, Any]) -> Dict[str, Any]:
    facts = verified_facts(record)
    product_type = _safe_value(_text(record.get("category", {}).get("product_type")), "piece")
    category = classify_category(product_type)
    detail = _product_specific_detail(facts, category)
    use = _safe_value(_fact(facts, "use_context", "usage", "occasion"), "her everyday routine")
    color = _safe_value(_fact(facts, "color", "shade"))
    material = _safe_value(_fact(facts, "material", "fabric"))
    finish = _safe_value(_fact(facts, "finish"))
    ingredient = _safe_value(_fact(facts, "ingredient", "key_ingredient"))

    if category == "fashion":
        titles = [
            f"{color + ' ' if color else ''}{product_type}",
            f"The {color.lower() + ' ' if color else ''}{product_type.lower()}",
            f"{product_type} — {color}" if color else f"{product_type} — MVQueen",
        ]
        openings = [
            f"A {product_type.lower()} for {use.lower()}, with the kind of polished presence that never needs to try too hard.",
            f"For {use.lower()}, this {product_type.lower()} brings a clean, confident direction to the way she dresses.",
            f"The right {product_type.lower()} can change the feeling of a look; this one starts with {detail or 'a considered silhouette'} and leaves room for her style to lead.",
        ]
        closer = "It is an easy foundation for modern, feminine styling with an intentional finish."
    elif category == "skincare":
        titles = [
            f"{product_type} for Her Routine",
            f"The {product_type}",
            f"{product_type} — MVQueen",
        ]
        openings = [
            f"Make room for a more considered {use.lower()} with this {product_type.lower()}{(' ' + detail) if detail else ''}.",
            f"A polished routine begins with products that make sense for the moment. This {product_type.lower()} brings {detail or 'a clearly defined step'} into focus.",
            f"For the part of her routine when she wants to slow down and be intentional, this {product_type.lower()} keeps the experience beautifully simple.",
        ]
        closer = "Keep the language of the routine clear, confident, and grounded in the product details that are actually verified."
    elif category == "cosmetics":
        titles = [
            f"{product_type} for the MVQueen Look",
            f"The {product_type}",
            f"{product_type} — MVQueen",
        ]
        openings = [
            f"Build the look around what she wants to express. This {product_type.lower()}{(' ' + detail) if detail else ''} brings a polished finishing touch to {use.lower()}.",
            f"For {use.lower()}, this {product_type.lower()} keeps the focus on a confident, modern finish{(' in ' + color.lower()) if color else ''}.",
            f"A beauty look feels most personal when every detail has a reason. Start with this {product_type.lower()}{(' and its ' + finish.lower() + ' finish') if finish else ''} and make it her own.",
        ]
        closer = "The result is a refined beauty moment that feels expressive rather than overworked."
    elif category == "jewelry":
        titles = [
            f"{color + ' ' if color else ''}{product_type}",
            f"The {product_type}",
            f"{product_type} — MVQueen",
        ]
        openings = [
            f"A small detail can set the tone. This {product_type.lower()}{(' ' + detail) if detail else ''} brings a polished note to {use.lower()}.",
            f"For the woman who styles with intention, this {product_type.lower()} adds a modern finishing point without taking over the look.",
            f"Layer it, let it stand alone, or make it part of the moment—this {product_type.lower()} is designed to keep her style feeling personal and polished.",
        ]
        closer = "It is the kind of detail that supports confident styling without competing with the woman wearing it."
    else:
        titles = [f"{product_type} — MVQueen", f"The {product_type}", f"{product_type} for Her"]
        openings = [
            f"A considered {product_type.lower()} for {use.lower()}, with a polished point of view.",
            f"This {product_type.lower()} keeps the experience simple, modern, and confidence-led.",
            f"For her everyday moments, this {product_type.lower()} brings an intentional finish to the way she chooses and uses what belongs in her world.",
        ]
        closer = "Simple, polished, and unmistakably personal."

    title = _choose(titles, record, "title")
    opening = _choose(openings, record, "opening")
    details: List[str] = []
    if material:
        details.append(f"Verified material: {material}.")
    if color:
        details.append(f"Verified color: {color}.")
    if ingredient:
        details.append(f"Verified ingredient: {ingredient}.")
    if finish:
        details.append(f"Verified finish: {finish}.")
    if not details and detail:
        details.append(f"Product detail: {detail}.")

    description_parts = [opening]
    if details:
        description_parts.append(" ".join(details))
    description_parts.append(closer)
    description = " ".join(description_parts)

    benefits = []
    if material:
        benefits.append(f"Verified {material.lower()} construction or material detail.")
    if color:
        benefits.append(f"A {color.lower()} color direction for intentional styling.")
    if finish:
        benefits.append(f"A verified {finish.lower()} finish.")
    if not benefits:
        benefits.append("Clear product details that support confident, informed selection.")

    return {
        "title": title,
        "short_description": opening,
        "description": description,
        "benefits": benefits,
        "features": details or [f"Product type: {product_type}."],
        "cta": "Shop MVQueen",
        "_editorial_category": category,
    }


def validate_editorial(record: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    copy = record.get("copy", {})
    text = " ".join(_text(copy.get(k)) for k in ("title", "short_description", "description", "cta"))
    if PLACEHOLDER_RE.search(text):
        errors.append("Editorial placeholder/template language detected")
    if FORBIDDEN_COPY_RE.search(text):
        errors.append("Unsupported or high-risk claim language detected in editorial copy")
    if GENERIC_RE.search(text):
        errors.append("Generic/robotic marketing phrase detected in editorial copy")
    facts = verified_facts(record)
    specific_values = [str(v).strip().lower() for v in facts.values() if _text(v)]
    if specific_values and not any(v in text.lower() for v in specific_values):
        errors.append("Customer-facing copy contains no verified product-specific detail")
    if not specific_values:
        errors.append("No verified product facts available for distinctive customer-facing copy")
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    if len(sentences) >= 3 and len({s[:30].lower() for s in sentences}) < 2:
        errors.append("Editorial sentence structure is excessively repetitive")
    if len(text.split()) < 18:
        warnings.append("Editorial copy is short; consider richer verified source data")
    return errors, warnings
