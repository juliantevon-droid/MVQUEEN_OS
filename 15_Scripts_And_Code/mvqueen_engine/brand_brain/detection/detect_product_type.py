"""Fine-grained product type detection."""
from __future__ import annotations

PRODUCT_TYPES = ["dress", "top", "blouse", "shirt", "skirt", "pants", "jeans", "jacket", "coat", "sweater", "bodysuit", "romper", "jumpsuit", "handbag", "clutch", "wallet", "necklace", "earrings", "bracelet", "ring", "sunglasses", "lipstick", "lip gloss", "mascara", "foundation", "concealer", "blush", "serum", "cleanser", "moisturizer", "toner", "sunscreen", "face mask"]

def detect_product_type(text: str) -> str:
    value = str(text or "").lower()
    matches = [term for term in PRODUCT_TYPES if term in value]
    return matches[0] if matches else "unknown"
