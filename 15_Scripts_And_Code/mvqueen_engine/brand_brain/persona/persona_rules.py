"""Rules controlling persona-driven editorial behavior."""
from __future__ import annotations

from .profiles import DEFAULT_PERSONA, PERSONA_PROFILES

FORBIDDEN_GENERIC_CLAIMS = ("best", "#1", "number one", "guaranteed")


def get_persona_rules(persona: str | None) -> dict:
    """Return deterministic editorial rules for the selected persona."""
    key = persona if persona in PERSONA_PROFILES else DEFAULT_PERSONA
    profile = PERSONA_PROFILES[key]
    return {
        "persona": key,
        "tone": profile["tone"],
        "voice": profile["voice"],
        "keywords": tuple(profile["keywords"]),
        "forbidden_generic_claims": FORBIDDEN_GENERIC_CLAIMS,
        "preserve_source_facts": True,
        "invent_product_claims": False,
    }


def validate_copy(text: str, persona: str | None = None) -> str:
    """Remove only prohibited generic superlatives; preserve factual copy."""
    rules = get_persona_rules(persona)
    output = str(text or "")
    for phrase in rules["forbidden_generic_claims"]:
        output = output.replace(phrase, "")
    return " ".join(output.split())


__all__ = ["FORBIDDEN_GENERIC_CLAIMS", "get_persona_rules", "validate_copy"]
