# mvqueen_engine/utils/price_logic.py
"""
PHASE 0 — PRICE LOGIC

Shared helpers:
- calculate_compare_price
"""

def calculate_compare_price(price: float) -> float:
    """
    28% / 35% / 42% uplift based on price tiers.
    """
    try:
        p = float(price)
    except (TypeError, ValueError):
        return 0.0

    if p < 20:
        return round(p * 1.28, 2)
    elif p < 60:
        return round(p * 1.35, 2)
    else:
        return round(p * 1.42, 2)