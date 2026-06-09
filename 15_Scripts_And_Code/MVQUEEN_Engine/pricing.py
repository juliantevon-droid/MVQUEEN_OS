# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — PRICING ENGINE (BLOCK S)
# SIMPLE MULTIPLIER MODEL
# ---------------------------------------------------------

from mvqueen_engine.utils.deterministic import deterministic_seed
from mvqueen_engine.brand_brain.detection import (
    detect_category,
    detect_persona,
    detect_trend
)

CATEGORY_BASE = {
    "dress": 120,
    "top": 60,
    "bottom": 80,
    "outerwear": 180,
    "general": 50
}

PERSONA_MULTIPLIER = {
    "runway": 1.6,
    "minimalist": 1.2,
    "romantic": 1.3,
    "bold": 1.4,
    "classic": 1.25
}

TREND_MULTIPLIER = {
    "metallic": 1.3,
    "sheer": 1.2,
    "tailored": 1.25,
    "oversized": 1.15,
    "athleisure": 1.1
}

def generate_price_simple(text: str) -> float:
    category = detect_category(text)
    persona = detect_persona(text)
    trend = detect_trend(text)

    base = CATEGORY_BASE.get(category, 50)
    price = base * PERSONA_MULTIPLIER.get(persona, 1.0)
    price *= TREND_MULTIPLIER.get(trend, 1.0)

    return round(price, 2)