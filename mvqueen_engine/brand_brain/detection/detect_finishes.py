"""Finish/surface detection."""
from ._common import detect_many

VOCAB = {
    "polished": ("polished",), "satin": ("satin",), "refined matte": ("refined matte",),
    "softly luminous": ("softly luminous",), "clean-finished": ("clean-finished", "clean finished"),
    "luminous": ("luminous", "luminous finish"), "matte elegance": ("matte elegance",),
    "glossy": ("glossy", "high shine", "gloss"), "metallic": ("metallic",), "sheer": ("sheer",),
}

def detect_finishes(text: str) -> list[str]:
    return detect_many(text, VOCAB)
