"""Product-type detection."""
from ._common import detect_one

VOCAB = {
    "dress": ("dress", "gown", "romper"), "top": ("top", "blouse", "shirt", "tee"),
    "outerwear": ("coat", "jacket", "trench", "blazer"), "bottom": ("pants", "trousers", "jeans", "skirt"),
    "serum": ("serum",), "moisturizer": ("moisturizer", "moisturiser", "cream"),
    "cleanser": ("cleanser", "face wash"), "mask": ("mask", "sheet mask"),
    "fragrance": ("perfume", "fragrance", "eau de"), "lip product": ("lipstick", "lip gloss", "lip oil"),
}

def detect_product_type(text: str) -> str:
    return detect_one(text, VOCAB, seed="product_type")
