"""Aesthetic vibe detection."""
from ._common import detect_one

VOCAB = {
    "Romantic": ("lace", "soft", "delicate", "floral"), "Edgy": ("leather", "hardware", "black", "distressed"),
    "Minimal": ("clean", "simple", "structured", "minimal"), "Glam": ("satin", "shine", "glow", "sequined"),
    "Elevated": ("luxury", "refined", "polished", "prestige"), "Street Luxe": ("cargo", "oversized", "street", "utility"),
}

def detect_vibe(text: str) -> str:
    return detect_one(text, VOCAB, seed="vibe")
