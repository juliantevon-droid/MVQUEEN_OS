"""Deterministic dual-brand routing for the canonical product pipeline.

MVQueen favors deep, saturated, rich, authoritative palettes. Miss.Princess
favors vivid, high-light, youthful spring/summer palettes. Generic shared base
colors such as pink, yellow, blue, and orange do not decide a brand without
shade, companion, or style evidence.
"""
from __future__ import annotations

from typing import Any, Dict

MVQUEEN_AUTHORITY_COLORS = {
    "black", "charcoal", "gold", "rich gold", "deep gold", "metallic gold",
    "burgundy", "wine", "oxblood", "espresso", "chocolate", "deep brown",
    "navy", "midnight blue", "royal blue", "emerald", "forest green",
    "deep green", "plum", "aubergine", "royal purple",
    "fuchsia", "magenta", "hot pink", "bold pink",
    "sun yellow", "sunflower yellow", "golden yellow", "mustard",
    "silver", "bronze", "champagne",
}
MVQUEEN_LUXE_NEUTRALS = {
    "white", "ivory", "cream", "beige", "nude", "tan", "camel",
    "brown", "taupe", "khaki", "gray", "grey", "olive",
}
MISS_PRINCESS_VIVID_COLORS = {
    "sky blue", "baby blue", "powder blue", "electric blue",
    "aqua", "turquoise", "mint", "seafoam",
    "lavender", "lilac", "periwinkle",
    "baby pink", "blush", "soft pink", "light pink", "bubblegum pink",
    "coral", "peach", "lime", "lemon", "pastel yellow", "light yellow",
    "tangerine", "bright orange", "rainbow", "multicolor", "pastel",
}
SHARED_BASE_COLORS = {"pink", "yellow", "blue", "orange"}

MVQUEEN_STYLE_HINTS = {
    "bold", "rich", "deep", "saturated", "authority", "authoritative",
    "luxury", "luxe", "elegant", "refined", "dramatic", "sleek", "tailored",
    "minimal", "structured", "classic", "polished", "statement",
    "jewel tone", "jewel toned", "metallic",
}
PRINCESS_STYLE_HINTS = {
    "bright", "vivid", "high light", "light intensity", "spring", "summer",
    "energetic", "energy", "youthful", "playful", "fresh", "airy", "soft",
    "sweet", "cute", "pastel", "colorful", "romantic", "fun", "floral",
    "sparkle",
}


def _verified_facts(record: Dict[str, Any]) -> Dict[str, str]:
    return {
        str(f.get("name", "")).strip().lower(): str(f.get("value", "")).strip().lower()
        for f in record.get("source_truth", {}).get("facts", [])
        if f.get("verified") is True and f.get("name") and f.get("value") is not None
    }


def _normalize(value: str) -> str:
    return " ".join(value.replace("_", " ").replace("-", " ").split()).lower()


def classify_brand_world(record: Dict[str, Any]) -> Dict[str, str]:
    facts = _verified_facts(record)
    color = _normalize(facts.get("color") or facts.get("shade") or "")

    mvqueen_score = 0
    princess_score = 0
    mvqueen_reason = ""
    princess_reason = ""

    if color in MVQUEEN_AUTHORITY_COLORS:
        mvqueen_score += 3
        mvqueen_reason = f"verified_color:{color}"
    elif color in MVQUEEN_LUXE_NEUTRALS:
        mvqueen_score += 2
        mvqueen_reason = f"verified_color:{color}"
    elif color in MISS_PRINCESS_VIVID_COLORS:
        princess_score += 3
        princess_reason = f"verified_color:{color}"
    elif color in SHARED_BASE_COLORS:
        # Shared base colors require additional verified style/shade context.
        pass

    style_text = " ".join(
        _normalize(facts.get(name, ""))
        for name in ("style", "vibe", "mood", "aesthetic", "occasion", "finish")
    )

    mvqueen_hits = sorted(hint for hint in MVQUEEN_STYLE_HINTS if hint in style_text)
    princess_hits = sorted(hint for hint in PRINCESS_STYLE_HINTS if hint in style_text)

    if mvqueen_hits:
        mvqueen_score += 1
        mvqueen_reason = mvqueen_reason or f"verified_style:{mvqueen_hits[0]}"
    if princess_hits:
        princess_score += 1
        princess_reason = princess_reason or f"verified_style:{princess_hits[0]}"

    if mvqueen_score > princess_score:
        return {
            "brand_world": "mvqueen",
            "brand_name": "MVQueen",
            "brand_tone": "bold-authoritative",
            "brand_routing_reason": mvqueen_reason or "palette:deep-saturated-authority",
            "brand_routing_confidence": "high" if mvqueen_score - princess_score >= 2 else "medium",
        }

    if princess_score > mvqueen_score:
        return {
            "brand_world": "miss-princess",
            "brand_name": "Miss.Princess",
            "brand_tone": "vivid-youthful",
            "brand_routing_reason": princess_reason or "palette:vivid-high-light-youthful",
            "brand_routing_confidence": "high" if princess_score - mvqueen_score >= 2 else "medium",
        }

    return {
        "brand_world": "needs-review",
        "brand_name": "Needs Review",
        "brand_tone": "review",
        "brand_routing_reason": (
            "balanced_verified_palette_signals"
            if mvqueen_score or princess_score
            else "ambiguous_verified_color_or_style"
        ),
        "brand_routing_confidence": "review",
    }


__all__ = ["classify_brand_world"]
