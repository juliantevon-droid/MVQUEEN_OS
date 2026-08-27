"""Editorial framing primitives for MVQueen copy generation."""

from typing import Any, Mapping

FRAMES = {
    "luxury": "Position the product through refined design, quality, and elevated everyday use.",
    "confidence": "Position the product around confidence, self-expression, and effortless presence.",
    "minimal": "Position the product through clean design, intentional details, and understated appeal.",
    "occasion": "Position the product around the supplied occasion and the experience it supports.",
}


def select_frame(context: Mapping[str, Any] | None = None) -> str:
    data = dict(context or {})
    requested = str(data.get("frame") or "").strip().lower()
    if requested in FRAMES:
        return requested
    mood = str(data.get("mood") or "").lower()
    if any(x in mood for x in ("confident", "empowered")):
        return "confidence"
    if any(x in mood for x in ("minimal", "composed", "refined")):
        return "minimal"
    if data.get("occasion"):
        return "occasion"
    return "luxury"


def render_frame(context: Mapping[str, Any] | None = None) -> str:
    return FRAMES[select_frame(context)]
