"""Customer persona detection."""
from ._common import detect_one

VOCAB = {
    "Evening Elegance": ("gown", "satin", "silk", "evening", "formal"),
    "Street Luxe": ("denim", "oversized", "cargo", "street", "hoodie"),
    "Soft Glam": ("serum", "glow", "hydrating", "dewy", "radiance"),
    "Minimal Classic": ("tailored", "structured", "clean", "minimal"),
    "Quiet Luxury": ("cashmere", "refined", "timeless", "quiet luxury"),
    "Romantic Feminine": ("lace", "floral", "ruffle", "romantic"),
}

def detect_persona(text: str) -> str:
    return detect_one(text, VOCAB, seed="persona")
