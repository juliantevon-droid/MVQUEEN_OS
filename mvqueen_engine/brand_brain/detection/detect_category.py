"""Category detection."""
from ._common import detect_one

VOCAB = {
    "fashion": ("dress", "gown", "top", "blouse", "shirt", "jacket", "coat", "pants", "jeans", "skirt"),
    "beauty": ("lipstick", "mascara", "eyeshadow", "fragrance", "perfume", "makeup"),
    "skincare": ("serum", "moisturizer", "lotion", "cleanser", "mask", "exfoliant", "toner", "cream"),
    "accessories": ("bag", "handbag", "purse", "earrings", "necklace", "bracelet", "scarf", "belt"),
}

def detect_category(text: str) -> str:
    return detect_one(text, VOCAB, seed="category")
