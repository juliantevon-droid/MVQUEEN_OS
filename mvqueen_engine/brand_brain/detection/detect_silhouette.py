"""Garment silhouette detection."""
from ._common import detect_one

VOCAB = {
    "A-Line": ("a-line",), "Bodycon": ("bodycon", "fitted"), "Oversized": ("oversized",),
    "Straight": ("straight leg", "straight fit"), "Relaxed": ("relaxed fit", "relaxed"),
    "Tailored": ("tailored fit", "tailored"), "Cropped": ("cropped",), "Draped": ("draped",),
    "Wrap": ("wrap dress", "wrap skirt", "wrap"), "Maxi": ("maxi",), "Mini": ("mini",), "Midi": ("midi",),
}

def detect_silhouette(text: str) -> str:
    return detect_one(text, VOCAB, seed="silhouette")
