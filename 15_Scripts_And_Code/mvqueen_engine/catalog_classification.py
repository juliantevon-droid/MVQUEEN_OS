"""Deterministic MVQUEEN recovery taxonomy.

Classification is derived from existing product identity text only. It does not
invent ingredients, materials, efficacy, pricing, inventory, or other product
facts.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Classification:
    category: str
    product_type: str
    confidence: str
    rule: str


def _blob(*parts: str) -> str:
    return " ".join(str(p or "") for p in parts).casefold()


def _has(text: str, *phrases: str) -> bool:
    return any(phrase.casefold() in text for phrase in phrases)


def _word(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, re.I))


def classify_product(
    *,
    title: str = "",
    handle: str = "",
    tags: str = "",
    description: str = "",
) -> Classification:
    # Title + handle + tags are primary identity signals. Description is last
    # because supplier prose can contain incidental words.
    primary = _blob(title, handle, tags)
    full = _blob(title, handle, tags, description)

    def hit(category: str, product_type: str, rule: str, *terms: str):
        if _has(primary, *terms):
            return Classification(category, product_type, "high", rule)
        return None

    # Fragrance
    result = hit("fragrance", "perfume", "fragrance/perfume",
                 "perfume", "eau de toilette", "eau de parfum", "cologne")
    if result:
        return result
    if _has(primary, "fragrance") and not _has(primary, "hair fragrance"):
        return Classification("fragrance", "fragrance", "high", "fragrance")

    # Haircare
    rules = (
        ("shampoo", ("shampoo",)),
        ("conditioner", ("conditioner", "deep conditioner")),
        ("hair mask", ("hair mask", "keratin mask", "hair treatment mask")),
        ("hair oil", ("hair oil", "hair essential oil", "rosemary oil for hair", "argan oil")),
        ("hair serum", ("hair serum", "hair essence", "hair growth serum", "scalp serum")),
        ("hair spray", ("hair spray", "hairspray", "sea salt spray", "leave-in spray")),
        ("hair styling", ("hair wax", "styling wax", "styling gel", "dreadlocks gel", "edge control", "wig setting")),
        ("hair styling powder", ("hair styling powder", "volumizing powder")),
        ("scalp scrub", ("hair scrub", "scalp scrub")),
        ("hair treatment", ("hair growth", "hair nutrition", "hair follicle", "keratin cream", "hair repair", "protectant leave-in")),
        ("hair tool", ("hair curler", "curling iron", "straightener", "detangling brush", "hair brush", "hair comb", "scalp massag")),
    )
    if _has(primary, "hair", "scalp", "wig", "dreadlock"):
        for ptype, terms in rules:
            if _has(primary, *terms):
                return Classification("haircare", ptype, "high", f"haircare:{ptype}")
        return Classification("haircare", "hair care", "medium", "haircare fallback")
    if "haircare" in primary:
        return Classification("haircare", "hair care", "medium", "haircare tag")

    # Eye makeup / lashes
    if _has(primary, "false eyelash", "false eyelashes", "fake eyelash", "mink lash", "magnetic eyelash", "magnetic lash"):
        return Classification("beauty", "false eyelashes", "high", "false eyelashes")
    if _has(primary, "eyelash glue", "lash glue", "adhesive eyeliner"):
        return Classification("beauty", "eyelash adhesive", "high", "eyelash adhesive")
    if _has(primary, "eyelash curler", "lash curler"):
        return Classification("beauty", "eyelash tool", "high", "eyelash tool")
    if _has(primary, "mascara", "eye black"):
        return Classification("beauty", "mascara", "high", "mascara")
    if _has(primary, "eyeliner", "eye liner"):
        return Classification("beauty", "eyeliner", "high", "eyeliner")
    if _has(primary, "eyebrow", "brow pencil", "brow gel", "brow tint", "brow powder", "brow brush"):
        return Classification("beauty", "eyebrow makeup", "high", "eyebrow")
    if _has(primary, "eye shadow", "eyeshadow"):
        return Classification("beauty", "eyeshadow", "high", "eyeshadow")
    if _has(primary, "double eyelid"):
        return Classification("beauty", "eye makeup", "high", "double eyelid")

    # Lip makeup / lip care
    if _has(primary, "lipstick", "lip stick"):
        return Classification("beauty", "lipstick", "high", "lipstick")
    if _has(primary, "lip gloss", "lipgloss", "lip glaze", "lip tint", "lip oil", "lip honey",
            "lipliner", "lip liner", "lip pencil", "lip plumper", "lip color"):
        return Classification("beauty", "lip color", "high", "lip color")
    if _has(primary, "lip balm", "lip essence", "lip care"):
        return Classification("skincare", "lip care", "high", "lip care")

    # Complexion / makeup
    if _has(primary, "foundation", "bb cream", "cc cream", "air cushion"):
        return Classification("beauty", "foundation", "high", "foundation")
    if _has(primary, "concealer", "camouflage makeup"):
        return Classification("beauty", "concealer", "high", "concealer")
    if _has(primary, "blush", "blusher"):
        return Classification("beauty", "blush", "high", "blush")
    if _has(primary, "highlighter", "highlighting powder", "highlight stick", "highlight powder", "brightening repair disc"):
        return Classification("beauty", "highlighter", "high", "highlighter")
    if _has(primary, "bronzer", "contouring powder", "contour stick", "contour palette", "nose shadow"):
        return Classification("beauty", "contour", "high", "contour")
    if _has(primary, "loose powder", "setting powder", "pressed powder", "face powder",
            "baking powder", "honey powder"):
        return Classification("beauty", "face powder", "high", "face powder")
    if _has(primary, "primer", "makeup base", "makeup pre", "pre-milk"):
        return Classification("beauty", "primer", "high", "primer")
    if _has(primary, "setting spray", "makeup holding spray", "makeup fixing spray"):
        return Classification("beauty", "setting spray", "high", "setting spray")
    if _has(primary, "body glitter", "body highlight", "highlight spray"):
        return Classification("beauty", "body makeup", "high", "body makeup")
    if _has(primary, "makeup set", "make up set", "beauty blind box"):
        return Classification("beauty", "makeup set", "high", "makeup set")

    # Makeup tools/accessories
    if _has(primary, "makeup brush", "make up brush", "cosmetic brush", "powder brush", "eye brush"):
        return Classification("beauty", "makeup brush", "high", "makeup brush")
    if _has(primary, "makeup sponge", "make up sponge", "powder puff", "makeup puff", "remover puff", "make up egg"):
        return Classification("beauty", "makeup sponge", "high", "makeup sponge")
    if _has(primary, "makeup mirror", "cosmetic mirror", "magnifying mirror"):
        return Classification("accessories", "makeup mirror", "high", "makeup mirror")
    if _has(primary, "makeup organizer", "cosmetic storage", "beauty rack"):
        return Classification("accessories", "beauty organizer", "high", "beauty organizer")
    if _has(primary, "ipl ", "hair remover", "facial cleansing instrument", "beauty instrument",
            "beauty massager", "face massager", "face roller", "massage roller", "ice compress"):
        return Classification("accessories", "beauty tool", "high", "beauty tool")

    # Nails
    if _has(primary, "nail polish", "nail art", "manicure", "nail gel", "nail glue",
            "nail remover", "nail grinder", "wearable nail", "press on nail", "press-on nail",
            "fake nail", "nail patch", "nail extension", "polygel", "poly gel", "crystal powder nail"):
        return Classification("beauty", "nail care", "high", "nail care")

    # Skincare
    if _has(primary, "cleanser", "face wash", "facial cleanser", "cleansing soap", "face soap"):
        return Classification("skincare", "cleanser", "high", "cleanser")
    if _has(primary, "toner", "soothing pad", "cotton pad") and _has(full, "skin", "face", "facial", "hydrating"):
        return Classification("skincare", "toner", "high", "toner/pad")
    if _has(primary, "facial scrub", "face scrub", "exfoliat", "body exfoliating"):
        return Classification("skincare", "exfoliator", "high", "exfoliator")
    if _has(primary, "face serum", "facial serum", "skin serum", "ampoule serum", "firming serum",
            "hyaluronic serum", "retinol serum", "vitamin c serum", "face care essence",
            "hydrating essence", "facial treatment essence"):
        return Classification("skincare", "serum", "high", "serum")
    if _has(primary, "moisturizer", "moisturising cream", "moisturizing cream", "face cream",
            "facial cream", "day cream", "night cream", "collagen cream", "skin care cream",
            "hydrating cream", "neck firming cream"):
        return Classification("skincare", "moisturizer", "high", "moisturizer")
    if _has(primary, "face mask", "facial mask", "sheet mask", "eye mask", "skin mask",
            "peel-off mask", "peel off mask", "jelly mask", "tear mask"):
        return Classification("skincare", "mask", "high", "mask")
    if _has(primary, "eye cream"):
        return Classification("skincare", "eye cream", "high", "eye cream")
    if _has(primary, "sunscreen", "sun cream", "uv protection") and _has(full, "skin", "face", "lotion", "cream"):
        return Classification("skincare", "sunscreen", "high", "sunscreen")
    if _has(primary, "acne treatment", "pimple", "blackhead"):
        return Classification("skincare", "acne care", "high", "acne")
    if _has(primary, "face lifting patch", "face lifter", "shaping patch", "skin tightening", "thin chin"):
        return Classification("skincare", "facial patch", "high", "facial patch")
    if _has(primary, "facial essential oil", "face oil"):
        return Classification("skincare", "facial oil", "high", "facial oil")
    if _has(primary, "body wash", "body lotion", "body cream", "body scrub", "body oil", "bath oil",
            "body care", "hand soap", "skin repair gel", "skin care gel"):
        return Classification("skincare", "body care", "high", "body care")
    if _has(primary, "skin", "facial", "face ") and _has(primary, "serum", "cream", "gel", "essence", "lotion", "spray"):
        return Classification("skincare", "skin treatment", "medium", "skin treatment")

    # Jewelry
    if _has(primary, "necklace", "pendant"):
        return Classification("jewelry", "necklace", "high", "necklace")
    if _has(primary, "earring"):
        return Classification("jewelry", "earrings", "high", "earrings")
    if _has(primary, "bracelet", "bangle"):
        return Classification("jewelry", "bracelet", "high", "bracelet")
    if _word(primary, r"\bring\b") and not _has(primary, "ring light"):
        return Classification("jewelry", "ring", "high", "ring")

    # Fashion / accessories / shoes
    if _has(primary, "dress", "gown"):
        return Classification("fashion", "dress", "high", "dress")
    if _has(primary, "lingerie", " bra ", "panties", "underwear"):
        return Classification("fashion", "lingerie", "high", "lingerie")
    if _has(primary, "coat", "jacket", "blazer"):
        return Classification("fashion", "outerwear", "high", "outerwear")
    if _has(primary, "tank top", "crop top", "blouse", " t-shirt", " tee ", "shirt"):
        return Classification("fashion", "top", "high", "top")
    if _has(primary, "pants", "trousers", "leggings", "jeans", "skirt", "shorts"):
        return Classification("fashion", "bottom", "high", "bottom")
    if _has(primary, "two-piece", "2-piece", "2 piece", "co-ord", "coord"):
        return Classification("fashion", "two-piece set", "high", "two-piece")
    if _has(primary, "handbag", "shoulder bag", "crossbody", "purse", "wallet", "tote bag"):
        return Classification("accessories", "bag", "high", "bag")
    if _has(primary, "sunglasses"):
        return Classification("accessories", "sunglasses", "high", "sunglasses")
    if _has(primary, "belt", "scarf", " hat ", " cap "):
        return Classification("accessories", "fashion accessory", "medium", "fashion accessory")
    if _has(primary, "heels", "sandals", "sneakers", "shoes", "boots", "slippers"):
        return Classification("shoes", "shoes", "high", "shoes")

    # Home
    if _has(primary, "lamp", "bedside light"):
        return Classification("home", "lamp", "high", "lamp")
    if _has(primary, "rug", "carpet"):
        return Classification("home", "rug", "high", "rug")
    if _has(primary, "bedding", "duvet", "pillow", "blanket", "bed set"):
        return Classification("home", "bedding", "high", "bedding")

    # Evidence-based domain fallbacks from source tags.
    if "fragrance" in primary or "perfume" in primary:
        return Classification("fragrance", "fragrance", "medium", "fragrance tag")
    if "haircare" in primary:
        return Classification("haircare", "hair care", "medium", "haircare tag")
    if "skincare" in primary:
        return Classification("skincare", "skin care", "medium", "skincare tag")
    if "beauty" in primary:
        return Classification("beauty", "beauty product", "medium", "beauty tag")

    return Classification("unclassified", "unclassified", "low", "no confident rule")


__all__ = ["Classification", "classify_product"]
