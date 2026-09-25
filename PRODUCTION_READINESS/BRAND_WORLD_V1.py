"""Deterministic dual-brand routing for the canonical product pipeline.

Brand-world assignment uses verified product facts first. It never guesses from
age, customer identity, or demographic attributes. Ambiguous products fail
closed to needs_review.
"""
from __future__ import annotations

from typing import Any, Dict

MISS_PRINCESS_COLORS = {
    "pink", "blush", "rose", "baby pink", "baby-pink", "hot pink", "hot-pink",
    "coral", "peach", "lavender", "lilac", "mint", "aqua", "turquoise",
    "sky blue", "sky-blue", "yellow", "lemon", "orange", "lime", "rainbow",
    "multicolor", "multi color", "pastel",
}
MVQUEEN_COLORS = {
    "black", "white", "ivory", "cream", "beige", "nude", "tan", "camel",
    "brown", "taupe", "khaki", "gray", "grey", "charcoal", "navy",
    "burgundy", "wine", "olive", "gold", "silver", "bronze", "champagne",
}
PRINCESS_STYLE_HINTS = {
    "playful", "soft", "sweet", "romantic", "cute", "pastel", "bright",
    "colorful", "youthful", "fun", "floral", "sparkle",
}
MVQUEEN_STYLE_HINTS = {
    "luxury", "elegant", "refined", "bold", "mature", "sleek", "tailored",
    "minimal", "structured", "classic", "polished", "statement",
}


def _verified_facts(record: Dict[str, Any]) -> Dict[str, str]:
    return {
        str(f.get("name", "")).strip().lower(): str(f.get("value", "")).strip().lower()
        for f in record.get("source_truth", {}).get("facts", [])
        if f.get("verified") is True and f.get("name") and f.get("value") is not None
    }


def classify_brand_world(record: Dict[str, Any]) -> Dict[str, str]:
    facts = _verified_facts(record)
    color = facts.get("color") or facts.get("shade") or ""
    normalized_color = " ".join(color.replace("_", " ").replace("-", " ").split())

    princess_colors = {" ".join(v.replace("-", " ").split()) for v in MISS_PRINCESS_COLORS}
    mvqueen_colors = {" ".join(v.replace("-", " ").split()) for v in MVQUEEN_COLORS}

    if normalized_color in princess_colors:
        return {
            "brand_world": "miss-princess",
            "brand_name": "Miss.Princess",
            "brand_tone": "soft-playful",
            "brand_routing_reason": f"verified_color:{normalized_color}",
            "brand_routing_confidence": "high",
        }

    if normalized_color in mvqueen_colors:
        return {
            "brand_world": "mvqueen",
            "brand_name": "MVQueen",
            "brand_tone": "neutral-mature",
            "brand_routing_reason": f"verified_color:{normalized_color}",
            "brand_routing_confidence": "high",
        }

    style_text = " ".join(
        facts.get(name, "")
        for name in ("style", "vibe", "mood", "aesthetic", "occasion", "finish")
    )
    princess_hits = sorted(hint for hint in PRINCESS_STYLE_HINTS if hint in style_text)
    mvqueen_hits = sorted(hint for hint in MVQUEEN_STYLE_HINTS if hint in style_text)

    if princess_hits and not mvqueen_hits:
        return {
            "brand_world": "miss-princess",
            "brand_name": "Miss.Princess",
            "brand_tone": "soft-playful",
            "brand_routing_reason": f"verified_style:{princess_hits[0]}",
            "brand_routing_confidence": "medium",
        }

    if mvqueen_hits and not princess_hits:
        return {
            "brand_world": "mvqueen",
            "brand_name": "MVQueen",
            "brand_tone": "neutral-mature",
            "brand_routing_reason": f"verified_style:{mvqueen_hits[0]}",
            "brand_routing_confidence": "medium",
        }

    return {
        "brand_world": "needs-review",
        "brand_name": "Needs Review",
        "brand_tone": "review",
        "brand_routing_reason": "ambiguous_verified_color_or_style",
        "brand_routing_confidence": "review",
    }


__all__ = ["classify_brand_world"]
