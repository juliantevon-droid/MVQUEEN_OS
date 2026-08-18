"""Seasonality detection."""
from ._common import detect_one

VOCAB = {
    "Spring": ("floral", "lightweight", "pastel", "spring"), "Summer": ("linen", "breezy", "sun", "summer"),
    "Fall": ("wool", "layered", "warm", "fall", "autumn"), "Winter": ("coat", "thermal", "heavy", "winter"),
    "Year-Round": ("classic", "timeless", "everyday", "essential"),
}

def detect_season(text: str) -> str:
    return detect_one(text, VOCAB, seed="season")
