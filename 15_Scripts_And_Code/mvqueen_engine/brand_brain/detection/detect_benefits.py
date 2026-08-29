"""Detect benefits only when supported by source wording."""
from __future__ import annotations

BENEFITS = {"comfort": ("comfortable", "comfort", "soft", "cozy", "breathable"), "durability": ("durable", "long lasting", "lasting", "resistant"), "lightweight": ("lightweight", "light weight", "featherlight"), "hydration": ("hydrating", "hydration", "moisturizing", "moisture"), "brightening": ("brightening", "brighten", "radiance", "luminous"), "soothing": ("soothing", "calming", "calm", "gentle"), "coverage": ("coverage", "full coverage", "buildable coverage")}

def detect_benefits(text: str) -> list[str]:
    value = str(text or "").lower()
    return [name for name, terms in BENEFITS.items() if any(term in value for term in terms)]
