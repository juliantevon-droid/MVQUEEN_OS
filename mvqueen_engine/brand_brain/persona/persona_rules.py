"""Persona routing rules and deterministic scoring."""

from __future__ import annotations

from collections.abc import Mapping

from .profiles import PERSONA_PROFILES
from ...utils.deterministic import seed_int

# Signals are intentionally broad. Existing detection can pass structured values,
# while raw CSV text can use the same router without a separate implementation.
PERSONA_SIGNALS = {
    "soft_luxury": {"satin", "silk", "soft", "romantic", "luminous", "glow", "delicate"},
    "clinical_chic": {"clean", "precise", "minimal", "tailored", "structured", "polished"},
    "modern_confident": {"bold", "sculpted", "bodycon", "statement", "confident", "power"},
    "mvqueen_signature": {"luxury", "elevated", "refined", "signature", "timeless", "premium"},
    "miss_queen_style": {"cute", "playful", "flirty", "sweet", "youthful", "fun"},
    "editorial_couture": {"couture", "runway", "editorial", "dramatic", "sculptural", "statement"},
    "minimalist_luxe": {"quiet", "understated", "capsule", "simple", "clean", "minimal"},
    "sensory_beauty": {"velvety", "buttery", "cooling", "breathable", "texture", "second-skin"},
    "runway_modernity": {"architectural", "angular", "directional", "future", "sharp", "modern"},
    "feminine_empowerment": {"empowering", "radiant", "strong", "feminine", "presence", "confidence"},
}


def _tokens(text: str) -> set[str]:
    return {token.strip(".,;:!?()[]{}\"'").lower() for token in str(text or "").split() if token.strip()}


def score_personas(text: str, detected: Mapping[str, object] | None = None) -> dict[str, float]:
    """Score every persona from raw text plus optional detector output."""
    combined = str(text or "").lower()
    if detected:
        combined += " " + " ".join(str(v).lower() for v in detected.values() if v is not None)
    tokens = _tokens(combined)
    scores: dict[str, float] = {}
    for key in PERSONA_PROFILES:
        signals = PERSONA_SIGNALS.get(key, set())
        exact = sum(1 for signal in signals if signal in tokens or signal in combined)
        scores[key] = float(exact)
    return scores


def choose_persona(text: str, detected: Mapping[str, object] | None = None, stable_key: str = "") -> str:
    """Choose the highest-scoring persona with deterministic tie-breaking."""
    scores = score_personas(text, detected)
    best = max(scores.values(), default=0.0)
    candidates = [key for key, value in scores.items() if value == best]
    if not candidates:
        return "mvqueen_signature"
    return candidates[seed_int(stable_key or text, "persona") % len(candidates)]
