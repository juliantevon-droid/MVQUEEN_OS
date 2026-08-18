"""Benefit signal detection."""
from ._common import detect_many

VOCAB = {
    "hydration": ("hydrate", "hydrating", "moisture", "moisturizing"),
    "radiance": ("radiance", "glow", "luminous", "brightening"),
    "soothing": ("soothe", "calm", "comfort", "sensitive"),
    "firming": ("firm", "firming", "elasticity"),
    "anti-aging": ("anti-aging", "fine lines", "wrinkles"),
    "nourishing": ("nourish", "nourishing", "nutrient"),
    "softness": ("soft", "smooth", "silky"),
    "confidence": ("confidence", "empower", "statement"),
    "comfort": ("comfortable", "comfort", "lightweight"),
    "versatility": ("versatile", "day-to-night", "everyday"),
}

def detect_benefits(text: str) -> list[str]:
    return detect_many(text, VOCAB)
