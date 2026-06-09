# ---------------------------------------------------------
# MVQUEEN OMNILUXE — ADVANCED PRICING ENGINE (BLOCK T)
# ---------------------------------------------------------

from mvqueen_engine.utils.deterministic import (
    deterministic_seed,
    deterministic_choice
)

from mvqueen_engine.brand_brain.detection import (
    detect_category,
    detect_persona,
    detect_trend,
)

CATEGORY_BASE = {
    "dress": 120,
    "top": 60,
    "bottom": 80,
    "outerwear": 180,
    "general": 50,
}

PERSONA_CURVES = {
    "runway":     [1.40, 1.55, 1.70],
    "minimalist": [1.10, 1.20, 1.30],
    "romantic":   [1.15, 1.25, 1.35],
    "bold":       [1.20, 1.35, 1.50],
    "classic":    [1.12, 1.22, 1.32],
}

TREND_SURCHARGE = {
    "metallic":   18,
    "sheer":      12,
    "tailored":   15,
    "oversized":  10,
    "athleisure": 8,
}

DISCOUNT_TIERS = [
    0.00,
    0.05,
    0.10,
    0.15,
]

def generate_price_advanced(text: str) -> float:
    seed = deterministic_seed(text)

    category = detect_category(text)
    persona = detect_persona(text)
    trend = detect_trend(text)

    base = CATEGORY_BASE.get(category, 50)

    curve = PERSONA_CURVES.get(persona, [1.0, 1.0, 1.0])
    persona_multiplier = deterministic_choice(seed, curve, salt="persona_curve")

    surcharge = TREND_SURCHARGE.get(trend, 0)

    discount = deterministic_choice(seed, DISCOUNT_TIERS, salt="discount_tier")

    price = base * persona_multiplier
    price += surcharge
    price *= (1 - discount)

    return round(price, 2)