"""Product category detection."""
from __future__ import annotations
import re

RULES = {
    "fashion": ("dress", "top", "blouse", "shirt", "skirt", "pant", "trouser", "jacket", "coat", "jean", "legging", "romper", "jumpsuit", "cardigan", "sweater", "bodysuit"),
    "beauty": ("makeup", "lipstick", "lip gloss", "foundation", "concealer", "mascara", "eyeliner", "blush", "bronzer", "highlighter", "cosmetic"),
    "skincare": ("serum", "moisturizer", "cleanser", "toner", "essence", "cream", "lotion", "sunscreen", "spf", "face mask", "exfoliant", "retinol"),
    "accessories": ("bag", "handbag", "purse", "wallet", "clutch", "belt", "scarf", "hat", "sunglasses", "jewelry", "necklace", "earring", "bracelet", "ring"),
}

def detect_category(text: str) -> str:
    value = str(text or "").lower()
    scores = {k: sum(bool(re.search(r"\b" + re.escape(term) + r"\b", value)) for term in terms) for k, terms in RULES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "uncategorized"
