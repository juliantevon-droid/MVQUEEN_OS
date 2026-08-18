"""High-level persona router."""

from __future__ import annotations

from collections.abc import Mapping

from .persona_rules import choose_persona
from .profiles import get_persona_profile


def route_persona(text: str, detected: Mapping[str, object] | None = None, stable_key: str = "") -> dict:
    """Return a complete persona decision for downstream editorial systems."""
    key = choose_persona(text, detected=detected, stable_key=stable_key)
    profile = get_persona_profile(key)
    return {
        "key": key,
        "name": profile["name"],
        "voice": profile["voice"],
        "adjectives": list(profile["adjectives"]),
        "cta": list(profile["cta"]),
        "seo_focus": list(profile["seo_focus"]),
    }
