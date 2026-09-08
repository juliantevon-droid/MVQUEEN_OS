"""
MVQUEEN OMNILUXE SUPREME — UNIVERSAL BRAND BANKS
================================================
Canonical stabilization copy of the additive MVQueen brand-intelligence banks.

Design principles:
- Additive architecture: banks never overwrite protected Shopify source fields.
- Deterministic: assignment is derived from stable product keys.
- Self-contained: no Helper_Library.csv dependency.
- Cross-category: skincare, beauty, makeup, haircare, body care, fashion,
  accessories, bundles and editorial campaigns.
- Shopify-safe: validation is separate from enrichment.
- Scale target: 75,000+ products without O(n²) bundle construction here.
"""
from __future__ import annotations

import hashlib
from typing import Dict, Iterable, List, Sequence, Tuple

BRAND_NAME = "MVQueen"
ARCHITECTURE_VERSION = "OmniLuxe Supreme v10.0 Brand Banks"
PROTECTED_COLUMNS = (
    "handle", "sku", "inventory_quantity", "cost", "variant_tax_code",
    "status", "image_src", "published",
)
SHOPIFY_VALID_STATUSES = {"active", "draft", "archived"}
REQUIRED_IMPORT_FIELDS = ("Title", "Status")

BRAND_VOICE_BANK = {
    "mvqueen_core": ["elegant", "controlled", "modern luxury", "refined", "authoritative", "elevated", "polished", "timeless", "confident", "distinctive"],
    "soft_power": ["sensual", "smooth", "magnetic", "luminous", "feminine", "alluring", "intimate", "graceful", "radiant", "soft power"],
    "precision": ["clean", "professional", "performance-led", "precise", "focused", "results-driven", "refined performance", "expert", "disciplined", "clear"],
    "quiet_luxury": ["understated", "minimal", "discreet", "effortless", "curated", "considered", "subtle", "essential", "modern", "quietly elevated"],
    "statement_glam": ["bold", "dramatic", "expressive", "spotlight-ready", "high-glam", "statement", "amplified", "striking", "magnetic", "unforgettable"],
}

PERSONA_IDENTITY = [
    "sensual", "clinical", "executive", "magnetic", "radiant", "luminous", "opulent", "elevated", "refined", "bold", "minimalist", "sacred", "restorative", "power", "elite", "signature", "modern", "timeless", "glow", "luxury", "high-glam", "runway", "spotlight", "quiet", "polished", "confident", "feminine", "empowered", "editorial", "couture", "prestige", "iconic", "serene", "sensory", "disciplined", "expressive", "magnetic", "cultivated", "distinctive", "effortless", "aspirational", "transformative", "ceremonial", "exclusive", "signature", "modernist", "radiance-led",
]
PERSONA_CATEGORY = [
    "skincare", "beauty", "makeup", "haircare", "body care", "glam", "aesthetic", "ritual", "system", "formula", "treatment", "complex", "collection", "edit", "silhouette", "finish", "routine", "therapy", "glow", "essentials", "serum", "cream", "foundation", "conditioner", "lip color", "eye makeup", "fragrance ritual", "body ritual", "wardrobe", "accessories", "beauty edit", "luxury essentials", "daily ritual", "evening ritual", "signature look", "personal style", "beauty wardrobe",
]
PERSONA_PERFORMANCE = [
    "high-performance", "results-driven", "advanced", "precision", "dermatologist-grade", "lab-crafted", "skin-renewing", "barrier-repair", "hydration-boosting", "collagen-enhancing", "firming", "smoothing", "sculpting", "shine-amplifying", "glow-enhancing", "anti-aging", "repair-focused", "intensive", "professional-grade", "luxury-formulated", "performance-led", "expert-developed", "precision-crafted", "ritual-ready", "long-wear", "buildable", "high-impact", "soft-focus", "finish-enhancing",
]
PERSONA_EMOTIONAL = [
    "confidence", "authority", "soft power", "allure", "dominance", "renewal", "empowerment", "magnetism", "elegance", "clarity", "control", "indulgence", "transformation", "visibility", "presence", "boldness", "refinement", "self-expression", "radiance", "elevation", "devotion", "composure", "intimacy", "desire", "mastery", "restoration", "comfort", "protection", "balance", "freedom", "discipline", "sensuality", "celebration", "identity",
]
PERSONA_SENSORY = [
    "velvety", "satin-soft", "silken", "glossy", "matte", "sheer", "weightless", "cocooning", "amplified", "refined", "polished", "whisper-light", "dewy", "radiant", "luminous", "sleek", "smooth", "plush", "high-gloss", "airy", "creamy", "buttery", "silky", "melting", "soft-focus", "featherlight", "rich", "supple", "cashmere-soft", "mirror-like", "light-reflective",
]
PERSONA_INTENT = [
    "enhance natural radiance", "improve skin tone", "restore moisture", "reduce dryness", "support a healthy-looking complexion", "smooth texture", "create a luminous finish", "define and sculpt", "build a polished look", "elevate an everyday ritual", "prepare for an occasion", "refresh the routine", "protect the skin barrier", "nourish dry hair", "smooth frizz", "boost shine", "create soft glam", "create high glam", "refine the complexion", "complete the beauty look", "express personal style", "build a signature wardrobe",
]

PERSONA_PROFILES = {
    "The Muse": {"axis": "Soft Power / Sensual Luxury", "emotions": ["allure", "radiance", "confidence", "magnetism", "desire"], "terms": ["sensual luxury", "magnetic femininity", "luminous elegance", "elevated beauty ritual"]},
    "CEO Glow": {"axis": "Precision / Authority / Results", "emotions": ["control", "mastery", "authority", "discipline", "refinement"], "terms": ["clinical luxury", "executive beauty", "strategic glow", "performance skincare"]},
    "The Ritualist": {"axis": "Restoration / Nourishment", "emotions": ["comfort", "grounding", "protection", "balance", "renewal"], "terms": ["sacred self-care", "restorative ritual", "deep nourishment", "renewal beauty"]},
    "The Icon": {"axis": "Glam / Visibility / Statement", "emotions": ["confidence", "boldness", "visibility", "magnetism", "celebration"], "terms": ["spotlight glow", "runway radiance", "statement beauty", "high-glam luxury"]},
    "Minimalist Luxe": {"axis": "Quiet Luxury / Understated Wealth", "emotions": ["composure", "clarity", "calm", "confidence", "refinement"], "terms": ["quiet luxury", "refined simplicity", "elevated essentials", "effortless polish"]},
}

LUXURY_MODIFIERS = ["luxury", "premium", "elite", "signature", "exclusive", "high-end", "refined", "elevated", "opulent", "prestige", "couture", "top-tier", "ultra-luxe", "modern luxury", "timeless luxury", "quiet luxury", "editorial luxury", "signature luxury", "premium beauty", "luxury essential"]
LUXURY_ADJECTIVES = ["radiant", "luminous", "velvety", "silken", "glossy", "refined", "polished", "sleek", "smooth", "plush", "dewy", "hydrated", "firm", "sculpted", "weightless", "airy", "soft-touch", "high-gloss", "matte-perfect", "supple", "elegant", "sensual", "timeless", "distinctive", "modern", "iconic"]
SENSORY_VERBS = ["infuses", "enhances", "transforms", "revives", "restores", "replenishes", "elevates", "boosts", "smooths", "brightens", "hydrates", "nourishes", "softens", "firms", "sculpts", "defines", "polishes", "refines", "illuminates"]
BENEFIT_SYNONYMS = ["enhances radiance", "restores moisture", "repairs damage", "boosts glow", "hydrates deeply", "smooths texture", "firms skin", "supports elasticity", "brightens tone", "revives dullness", "nourishes dry hair", "boosts shine", "smooths frizz", "defines features", "refines the finish", "supports a polished look"]
INTENT_PHRASES = ["improve skin tone", "reduce dryness", "boost hydration", "enhance glow", "repair damage", "firm and lift", "smooth fine lines", "create soft glam", "create a polished finish", "build a signature look", "prepare for an occasion", "elevate everyday beauty", "refine personal style", "complete the ritual"]

CATEGORY_BANKS = {
    "skincare": {"keywords": ["hydration", "barrier care", "radiance", "brightening", "firming", "renewal", "serum", "moisturizer", "cleanser", "mask"], "outcomes": ["radiant complexion", "supple hydration", "smooth texture", "balanced-looking skin", "refined glow"]},
    "beauty": {"keywords": ["beauty ritual", "glow", "radiance", "polish", "beauty essential", "signature look", "elevated routine"], "outcomes": ["refined beauty", "luminous finish", "confident expression", "effortless polish"]},
    "makeup": {"keywords": ["soft glam", "full coverage", "natural finish", "high-shine", "lip color", "blush", "complexion", "highlight", "contour", "eye makeup"], "outcomes": ["smooth complexion", "defined features", "luminous finish", "statement color", "long-wear polish"]},
    "haircare": {"keywords": ["hydration", "repair", "shine", "smoothness", "scalp care", "strength", "conditioner", "hair mask", "styling"], "outcomes": ["silky softness", "healthy-looking shine", "smooth finish", "supple strands", "refined styling"]},
    "body": {"keywords": ["body care", "hydration", "body glow", "nourishment", "smooth skin", "body ritual", "body oil", "body cream"], "outcomes": ["supple skin", "radiant body glow", "silky softness", "nourished skin"]},
    "fashion": {"keywords": ["modern luxury", "quiet luxury", "tailored", "silhouette", "statement piece", "wardrobe essential", "couture-inspired"], "outcomes": ["effortless elegance", "refined silhouette", "confident presence", "polished style"]},
    "bundles": {"keywords": ["ritual set", "beauty edit", "curated collection", "signature set", "complete routine", "luxury bundle"], "outcomes": ["complete ritual", "coordinated routine", "elevated experience", "gift-ready presentation"]},
}

SEO_LANGUAGE_BANK = {
    "en": {"luxury": "luxury", "glow": "glow", "beauty": "beauty", "ritual": "ritual", "premium": "premium"},
    "fr": {"luxury": "luxe", "glow": "éclat", "beauty": "beauté", "ritual": "rituel", "premium": "premium"},
    "es": {"luxury": "lujo", "glow": "luminosidad", "beauty": "belleza", "ritual": "ritual", "premium": "premium"},
    "de": {"luxury": "luxus", "glow": "ausstrahlung", "beauty": "beauty", "ritual": "ritual", "premium": "premium"},
    "it": {"luxury": "lusso", "glow": "luminosità", "beauty": "bellezza", "ritual": "rituale", "premium": "premium"},
    "pt": {"luxury": "luxo", "glow": "luminosidade", "beauty": "beleza", "ritual": "ritual", "premium": "premium"},
}
PRICE_TIERS = ((0.0, 20.0, "Entry"), (20.0, 60.0, "Core"), (60.0, 100.0, "Premium"), (100.0, float("inf"), "Luxury"))
COLLECTION_BANK = ["Core Collection", "Premium Line", "Seasonal Edit", "Glow Ritual", "Clean Beauty Edit", "Minimal Essentials", "Night Glam Series", "Hydration Authority", "Barrier Repair System", "Luxury Body Ritual", "Signature Beauty Edit", "Quiet Luxury Essentials", "Soft Power Collection", "CEO Glow Collection", "The Icon Edit", "The Ritualist Collection"]


def stable_seed(value: str) -> Tuple[int, ...]:
    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return tuple(int(digest[i:i + 8], 16) for i in range(0, 64, 8))


def choose(pool: Sequence[str], seed: int) -> str:
    return pool[seed % len(pool)] if pool else ""


def generate_persona_keywords(limit: int = 1000) -> List[str]:
    results = set()
    for identity in PERSONA_IDENTITY:
        for category in PERSONA_CATEGORY:
            results.add(f"{identity} {category}")
    for performance in PERSONA_PERFORMANCE:
        for category in PERSONA_CATEGORY:
            results.add(f"{performance} {category}")
    for sensory in PERSONA_SENSORY:
        for category in PERSONA_CATEGORY:
            results.add(f"{sensory} {category}")
    for identity in PERSONA_IDENTITY:
        for emotion in PERSONA_EMOTIONAL:
            results.add(f"{identity} {emotion}")
    for intent in PERSONA_INTENT:
        for identity in PERSONA_IDENTITY:
            results.add(f"{identity} {intent}")
    for sensory in PERSONA_SENSORY:
        results.update((f"{sensory} glow", f"{sensory} finish", f"{sensory} effect"))
    return sorted(results)[:limit]

PERSONA_KEYWORDS = generate_persona_keywords(1000)


def assign_persona(product_key: str) -> str:
    return tuple(PERSONA_PROFILES.keys())[stable_seed(product_key)[0] % len(PERSONA_PROFILES)]


def assign_brand_voice(product_key: str) -> str:
    return tuple(BRAND_VOICE_BANK.keys())[stable_seed(product_key)[1] % len(BRAND_VOICE_BANK)]


def assign_keywords(product_key: str, count: int = 12) -> List[str]:
    if not PERSONA_KEYWORDS:
        return []
    seeds = stable_seed(product_key)
    size = len(PERSONA_KEYWORDS)
    return [PERSONA_KEYWORDS[(seeds[i % len(seeds)] + i * 97) % size] for i in range(count)]


def price_tier(price: float) -> str:
    for low, high, label in PRICE_TIERS:
        if low <= price < high:
            return label
    return "Luxury"


def compare_at_price(price: float) -> float:
    if price <= 0:
        return 0.0
    if price < 20:
        return round(price * 1.28, 2)
    if price < 60:
        return round(price * 1.35, 2)
    return float(round(price * 1.42))


def build_bundle_candidates(product_key: str, candidate_keys: Iterable[str], limit: int = 20) -> List[str]:
    target = stable_seed(product_key)[0]
    scored = []
    for key in candidate_keys:
        if key == product_key:
            continue
        scored.append((abs(target - stable_seed(key)[0]), key))
    scored.sort(key=lambda item: (item[0], item[1]))
    return [key for _, key in scored[:limit]]


def validate_shopify_row(row: Dict[str, str]) -> List[str]:
    errors: List[str] = []
    title = str(row.get("Title", "")).strip()
    status = str(row.get("Status", "")).strip().lower()
    if not title:
        errors.append("Title can't be blank")
    if status not in SHOPIFY_VALID_STATUSES:
        errors.append("Status isn't valid. Set the status as active, draft, or archived.")
    return errors


def enrich_metadata(product_key: str, price: float = 0.0) -> Dict[str, object]:
    seed = stable_seed(product_key)
    persona = assign_persona(product_key)
    voice = assign_brand_voice(product_key)
    keywords = assign_keywords(product_key)
    hero_probability = round((seed[3] % 101) / 100, 2)
    routine_fit = round((seed[4] % 101) / 100, 2)
    search_match = round((seed[5] % 101) / 100, 2)
    return {
        "metafield.custom.persona": persona,
        "metafield.custom.persona_axis": PERSONA_PROFILES[persona]["axis"],
        "metafield.custom.persona_emotion": choose(PERSONA_PROFILES[persona]["emotions"], seed[1]),
        "metafield.custom.persona_keywords": ", ".join(keywords),
        "metafield.custom.brand_voice": voice,
        "metafield.custom.price_psychology_tier": price_tier(price),
        "metafield.custom.prestige_score": round(40 + (seed[2] % 61), 2),
        "metafield.custom.hero_probability": hero_probability,
        "metafield.custom.routine_integration_score": routine_fit,
        "metafield.custom.search_intent_match": search_match,
        "metafield.custom.conversion_index": round((hero_probability + routine_fit + search_match) / 3, 4),
        "metafield.custom.bundle_affinity": round((seed[6] % 101) / 100, 2),
        "metafield.custom.collection": choose(COLLECTION_BANK, seed[7]),
        "compare_at_price_suggestion": compare_at_price(price),
    }

BRAND_BANK = {
    "version": ARCHITECTURE_VERSION, "brand_name": BRAND_NAME,
    "persona_keywords": PERSONA_KEYWORDS, "persona_profiles": PERSONA_PROFILES,
    "brand_voice": BRAND_VOICE_BANK, "luxury_modifiers": LUXURY_MODIFIERS,
    "luxury_adjectives": LUXURY_ADJECTIVES, "sensory_verbs": SENSORY_VERBS,
    "benefit_synonyms": BENEFIT_SYNONYMS, "intent_phrases": INTENT_PHRASES,
    "category_banks": CATEGORY_BANKS, "seo_languages": SEO_LANGUAGE_BANK,
    "collections": COLLECTION_BANK, "price_tiers": PRICE_TIERS,
    "protected_columns": PROTECTED_COLUMNS, "required_import_fields": REQUIRED_IMPORT_FIELDS,
}

PERSONA_BANK = {"persona_keywords": PERSONA_KEYWORDS, "profiles": PERSONA_PROFILES}

__all__ = [
    "ARCHITECTURE_VERSION", "BRAND_BANK", "BRAND_NAME", "BRAND_VOICE_BANK",
    "CATEGORY_BANKS", "COLLECTION_BANK", "LUXURY_ADJECTIVES", "LUXURY_MODIFIERS",
    "PERSONA_BANK", "PERSONA_EMOTIONAL", "PERSONA_KEYWORDS", "PERSONA_PROFILES",
    "PROTECTED_COLUMNS", "SEO_LANGUAGE_BANK", "SENSORY_VERBS", "assign_brand_voice",
    "assign_keywords", "assign_persona", "build_bundle_candidates", "compare_at_price",
    "enrich_metadata", "generate_persona_keywords", "stable_seed", "validate_shopify_row",
]
