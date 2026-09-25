"""MVQueen Editorial Intelligence Engine V1.

Deterministic, category-aware customer-facing copy generation.
The engine only uses verified source facts as factual inputs. It does not
invent ingredients, materials, fit, performance, results, certifications,
or other product attributes.

Lexical variation is intentionally drawn from the canonical MVQueen voice:
quiet confidence, warm luxury, feminine precision, considered simplicity,
and polished restraint. Vocabulary changes framing, never product facts.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List, Tuple

PLACEHOLDER_RE = re.compile(r"\{[^}]+\}|\b(?:describe|close with|insert|add)\s+(?:the\s+)?(?:benefits?|features?|details?|cta|keyword|persona)\b", re.I)
FORBIDDEN_COPY_RE = re.compile(
    r"\b(cures?|treats?|prevents?|guaranteed?|clinically proven|medical[- ]grade|"
    r"hypoallergenic|non[- ]toxic|chemical[- ]free|organic|certified|#1|100%|"
    r"instant|permanent)\b", re.I
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

DEFAULT_USE = {
    "fashion": "everyday styling",
    "skincare": "her everyday routine",
    "cosmetics": "her everyday look",
    "jewelry": "everyday styling",
    "general": "everyday use",
}

VOICE_TONES = {
    "fashion": [
        "quiet confidence",
        "polished restraint",
        "intentional femininity",
        "refined simplicity",
        "modern composure",
        "considered ease",
    ],
    "skincare": [
        "quiet intention",
        "considered simplicity",
        "warm restraint",
        "clear purpose",
        "unhurried care",
        "refined simplicity",
    ],
    "cosmetics": [
        "polished expression",
        "modern confidence",
        "intentional definition",
        "refined simplicity",
        "composed glamour",
        "personal expression",
    ],
    "jewelry": [
        "quiet confidence",
        "polished restraint",
        "intentional detail",
        "refined simplicity",
        "modern femininity",
        "considered elegance",
    ],
    "general": [
        "quiet confidence",
        "polished simplicity",
        "intentional detail",
        "refined restraint",
        "modern clarity",
        "considered ease",
    ],
}

OPENING_FRAMES = {
    "fashion": [
        "For {use}, this {product_type}{detail_clause} brings {tone} to the way she dresses.",
        "A {product_type}{detail_clause} for {use}, defined by {tone} and room for her own styling.",
        "Built around {use}, this {product_type}{detail_clause} keeps the direction rooted in {tone}.",
        "For the woman who dresses with intention, this {product_type}{detail_clause} brings {tone} to {use}.",
        "This {product_type}{detail_clause} belongs in {use} when the mood calls for {tone}.",
        "Start with a {product_type}{detail_clause}; for {use}, the point of view is {tone}.",
    ],
    "skincare": [
        "For {use}, this {product_type}{detail_clause} brings {tone} to the routine.",
        "A more considered {use} starts with a {product_type}{detail_clause} and a sense of {tone}.",
        "This {product_type}{detail_clause} belongs in {use} when the routine calls for {tone}.",
        "For the part of {use} that deserves more intention, this {product_type}{detail_clause} keeps the mood rooted in {tone}.",
        "A {product_type}{detail_clause} gives {use} a point of view shaped by {tone}.",
        "Keep {use} focused: this {product_type}{detail_clause} brings {tone} without unnecessary noise.",
    ],
    "cosmetics": [
        "For {use}, this {product_type}{detail_clause} brings {tone} to the look.",
        "Build {use} around a {product_type}{detail_clause} with a point of view rooted in {tone}.",
        "This {product_type}{detail_clause} belongs in {use} when the direction is {tone}.",
        "For the woman who treats beauty as self-expression, this {product_type}{detail_clause} brings {tone} to {use}.",
        "A {product_type}{detail_clause} gives {use} a finishing direction shaped by {tone}.",
        "Start with a {product_type}{detail_clause}; the rest of {use} can follow with {tone}.",
    ],
    "jewelry": [
        "For {use}, this {product_type}{detail_clause} brings {tone} to the finishing details.",
        "A {product_type}{detail_clause} for {use}, chosen with {tone} rather than excess.",
        "This {product_type}{detail_clause} belongs in {use} when the direction is {tone}.",
        "For the woman who styles with intention, this {product_type}{detail_clause} adds {tone} to {use}.",
        "A small detail can set the tone; this {product_type}{detail_clause} brings {tone} to {use}.",
        "Start with a {product_type}{detail_clause}; for {use}, the finishing point is {tone}.",
    ],
    "general": [
        "For {use}, this {product_type}{detail_clause} brings {tone} to the experience.",
        "A {product_type}{detail_clause} for {use}, shaped by {tone} and a clear point of view.",
        "This {product_type}{detail_clause} belongs in {use} when the direction is {tone}.",
        "For the woman who chooses with intention, this {product_type}{detail_clause} brings {tone} to {use}.",
        "A considered choice for {use}, this {product_type}{detail_clause} is framed by {tone}.",
        "Start with a {product_type}{detail_clause}; the point of view is {tone}.",
    ],
}

CLOSERS = {
    "fashion": [
        "The finish is modern and feminine, with enough restraint for her own styling to lead.",
        "It keeps the look composed, personal, and easy to build around.",
        "The result is polished without feeling overworked.",
        "A considered foundation for a wardrobe built with intention.",
        "It carries the look with quiet confidence rather than excess.",
        "The piece does its part, then leaves room for her presence.",
    ],
    "skincare": [
        "A considered addition to a routine that values clarity, simplicity, and details she can trust.",
        "The experience stays focused, warm, and intentionally simple.",
        "A quiet step in the routine, grounded in the product details that are actually verified.",
        "It keeps the ritual clear and unhurried rather than overcomplicated.",
        "The point is thoughtful care with no invented promises.",
        "A refined routine starts with knowing exactly what belongs in it.",
    ],
    "cosmetics": [
        "The final look stays expressive, polished, and personal.",
        "It gives the beauty moment definition without making it feel overworked.",
        "The direction is modern, composed, and open to her own expression.",
        "A finishing choice that supports the look without speaking over it.",
        "The result feels intentional rather than overdone.",
        "It brings the look together while leaving the expression hers.",
    ],
    "jewelry": [
        "It supports confident styling without competing with the woman wearing it.",
        "The detail feels considered, polished, and easy to make personal.",
        "It finishes the look with restraint rather than noise.",
        "A small, intentional detail with enough presence to stand on its own.",
        "The piece adds definition while keeping the styling distinctly hers.",
        "It brings a refined finishing note to the edit.",
    ],
    "general": [
        "Simple, polished, and personal.",
        "A considered choice with a clear point of view.",
        "The experience stays intentional rather than overworked.",
        "A refined addition to the MVQueen edit.",
        "It brings quiet confidence to the everyday.",
        "The final impression is composed, useful, and distinctly personal.",
    ],
}

CTA_OPTIONS = [
    "Explore the MVQueen edit",
    "Discover the product details",
    "Make it part of her edit",
    "Shop the MVQueen edit",
    "See the full MVQueen details",
]


PRINCESS_VOICE_TONES = {
    "fashion": ["soft glamour", "playful polish", "romantic confidence", "bright femininity", "expressive ease", "color-led charm"],
    "skincare": ["soft ritual", "playful self-care", "gentle polish", "bright simplicity", "romantic ease", "fresh femininity"],
    "cosmetics": ["playful glamour", "bright expression", "soft definition", "color-led confidence", "romantic polish", "expressive femininity"],
    "jewelry": ["playful polish", "soft sparkle", "romantic detail", "bright femininity", "expressive charm", "color-led glamour"],
    "general": ["playful polish", "soft glamour", "bright femininity", "romantic ease", "expressive charm", "color-led confidence"],
}

PRINCESS_CLOSERS = {
    "fashion": [
        "The finish stays feminine, expressive, and polished enough to make the color feel intentional.",
        "It brings a playful point of view without losing the composed finish.",
        "The result feels bright, personal, and easy to make her own.",
        "A softer statement for a wardrobe that leaves room for color and personality.",
    ],
    "skincare": [
        "The ritual stays soft, clear, and grounded in the product details that are actually verified.",
        "A gentle, polished step for a routine that makes room for a little more play.",
        "The experience is bright and intentional without invented promises.",
        "A soft approach to self-care, built around what is actually known about the product.",
    ],
    "cosmetics": [
        "The final look stays expressive, feminine, and polished.",
        "It gives color room to play while keeping the finish considered.",
        "The result feels bright and personal rather than overworked.",
        "A playful finishing choice that still feels composed.",
    ],
    "jewelry": [
        "The detail brings soft glamour and a playful finishing note to the look.",
        "It adds color and personality while keeping the styling polished.",
        "A bright, feminine detail that is easy to make personal.",
        "The piece brings expressive charm without losing refinement.",
    ],
    "general": [
        "Soft, expressive, and polished.",
        "A playful choice with a clear point of view.",
        "The final impression is bright, feminine, and personal.",
        "A little more color, a little more play, with the details kept clear.",
    ],
}

PRINCESS_CTA_OPTIONS = [
    "Explore the Miss.Princess world",
    "Discover the playful edit",
    "Make it part of her Miss.Princess edit",
    "Shop the Miss.Princess world",
    "See the full Miss.Princess details",
]


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
    main_stone = _safe_value(_fact(facts, "main_stone"))
    if category == "jewelry" and main_stone:
        return f"featuring {main_stone}"
    if category == "skincare" and ingredient:
        return f"with {ingredient} listed among its ingredients"
    if category == "cosmetics" and finish:
        return f"with a {finish.lower()} finish"
    if texture:
        return f"with a {texture.lower()} texture"
    if material:
        return f"in {material}"
    if color:
        return f"in {color}"
    if size:
        return f"in the listed {size} specification"
    return ""


def generate(record: Dict[str, Any]) -> Dict[str, Any]:
    facts = verified_facts(record)
    product_type = _safe_value(_text(record.get("category", {}).get("product_type")), "piece")
    category = classify_category(product_type)
    brand_world = _text(record.get("intelligence", {}).get("brand_world")) or "mvqueen"
    brand_name = "Miss.Princess" if brand_world == "miss-princess" else "MVQueen"
    is_princess = brand_world == "miss-princess"
    detail = _product_specific_detail(facts, category)
    use = _safe_value(
        _fact(facts, "use_context", "usage", "occasion"),
        DEFAULT_USE.get(category, DEFAULT_USE["general"]),
    )
    color = _safe_value(_fact(facts, "color", "shade"))
    material = _safe_value(_fact(facts, "material", "fabric"))
    finish = _safe_value(_fact(facts, "finish"))
    ingredient = _safe_value(_fact(facts, "ingredient", "key_ingredient"))
    main_stone = _safe_value(_fact(facts, "main_stone"))
    main_stone_size = _safe_value(_fact(facts, "main_stone_size"))

    if category == "fashion":
        titles = [
            f"{color + ' ' if color else ''}{product_type}",
            f"The {color.lower() + ' ' if color else ''}{product_type.lower()}",
            f"{product_type} in {color}" if color else f"{product_type} — {brand_name}",
            f"{brand_name} {product_type}",
        ]
    elif category == "jewelry":
        titles = [
            f"{main_stone + ' ' if main_stone else ''}{product_type}",
            f"The {product_type}",
            f"{product_type} in {color}" if color else f"{product_type} — {brand_name}",
            f"{brand_name} {product_type}",
        ]
    elif category == "skincare":
        titles = [
            f"{product_type} for Her Routine",
            f"The {product_type}",
            f"{product_type} — {brand_name}",
            f"{brand_name} {product_type}",
        ]
    elif category == "cosmetics":
        titles = [
            f"{product_type} for the {brand_name} Look",
            f"The {product_type}",
            f"{product_type} in {color}" if color else f"{product_type} — {brand_name}",
            f"{brand_name} {product_type}",
        ]
    else:
        titles = [
            f"{product_type} — {brand_name}",
            f"The {product_type}",
            f"{product_type} for Her",
            f"{brand_name} {product_type}",
        ]

    tone_bank = PRINCESS_VOICE_TONES[category] if is_princess else VOICE_TONES[category]
    tone = _choose(tone_bank, record, "tone")
    frame = _choose(OPENING_FRAMES[category], record, "opening-frame")
    detail_clause = f" {detail}" if detail else ""
    opening = frame.format(
        use=use.lower(),
        product_type=product_type.lower(),
        detail_clause=detail_clause,
        tone=tone,
    )
    closer_bank = PRINCESS_CLOSERS[category] if is_princess else CLOSERS[category]
    closer = _choose(closer_bank, record, "closer")

    title = _choose(titles, record, "title")
    details: List[str] = []
    if material:
        details.append(f"Material: {material}.")
    if color:
        details.append(f"Color: {color}.")
    if ingredient:
        details.append(f"Ingredient listed: {ingredient}.")
    if finish:
        details.append(f"Finish: {finish}.")
    if main_stone:
        details.append(f"Main stone: {main_stone}.")
    if main_stone_size:
        details.append(f"Main stone size: {main_stone_size}.")
    if not details and detail:
        details.append(f"Product detail: {detail}.")

    description_parts = [opening]
    if details:
        description_parts.append(" ".join(details))
    description_parts.append(closer)
    description = " ".join(description_parts)

    benefits = []
    if material:
        benefits.append(f"The listed {material.lower()} material gives the product a clear factual foundation for styling or use.")
    if color:
        benefits.append(f"The {color.lower()} color direction gives the edit a defined visual starting point.")
    if finish:
        benefits.append(f"The listed {finish.lower()} finish helps define the final look.")
    if ingredient:
        benefits.append(f"Includes {ingredient} as a listed ingredient.")
    if main_stone:
        benefits.append(f"The listed {main_stone} stone gives the piece a clear focal detail.")
    if not benefits:
        benefits.append("Clear product details support a more confident, informed selection.")

    return {
        "title": title,
        "short_description": opening,
        "description": description,
        "benefits": benefits,
        "features": details or [f"Product type: {product_type}."],
        "cta": _choose(PRINCESS_CTA_OPTIONS if is_princess else CTA_OPTIONS, record, f"cta:{category}:{brand_world}"),
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
