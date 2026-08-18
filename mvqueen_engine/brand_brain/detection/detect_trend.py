"""Trend detection."""
from ._common import detect_one

VOCAB = {
    "Soft Glam": ("glow", "dewy", "radiance"), "Structured Minimalism": ("structured", "clean lines"),
    "Street Utility": ("cargo", "oversized", "utility"), "Romantic Lace": ("lace", "delicate"),
    "Quiet Luxury": ("quiet luxury", "cashmere", "understated"), "Modern Tailoring": ("tailored", "blazer", "suiting"),
}

def detect_trend(text: str) -> str:
    return detect_one(text, VOCAB, seed="trend")
