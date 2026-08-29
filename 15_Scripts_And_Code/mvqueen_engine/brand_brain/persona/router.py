"""Deterministic persona routing for MVQueen."""
from __future__ import annotations

from .profiles import DEFAULT_PERSONA, PERSONA_PROFILES, get_profile


def route_persona(context: dict | None = None) -> str:
    """Select the strongest persona from available product signals."""
    context = context or {}
    text = " ".join(str(context.get(key, "")) for key in ("title", "description", "category", "product_type", "vibe", "trend", "benefits", "target_audience", "persona" )).lower()
    explicit = str(context.get("persona", "")).strip()
    if explicit in PERSONA_PROFILES:
        return explicit
    scores = {name: 0 for name in PERSONA_PROFILES}
    for name, profile in PERSONA_PROFILES.items():
        scores[name] = sum(1 for keyword in profile["keywords"] if keyword in text)
    best = max(scores, key=scores.get)
    return best if scores[best] else DEFAULT_PERSONA


def route_profile(context: dict | None = None) -> dict:
    persona = route_persona(context)
    profile = get_profile(persona)
    profile["persona"] = persona
    return profile


__all__ = ["route_persona", "route_profile"]
