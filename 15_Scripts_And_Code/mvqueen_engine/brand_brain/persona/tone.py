"""Tone policy derived from canonical persona profiles."""
from __future__ import annotations

from .profiles import DEFAULT_PERSONA, get_profile


def resolve_tone(persona: str | None) -> str:
    """Return the canonical tone descriptor for a persona."""
    return get_profile(persona or DEFAULT_PERSONA)["tone"]


def resolve_voice(persona: str | None) -> str:
    """Return the canonical brand voice for a persona."""
    return get_profile(persona or DEFAULT_PERSONA)["voice"]


def tone_context(persona: str | None) -> dict[str, str]:
    """Return the stable tone/voice context consumed by editorial code."""
    return {"persona": persona or DEFAULT_PERSONA, "tone": resolve_tone(persona), "voice": resolve_voice(persona)}


__all__ = ["resolve_tone", "resolve_voice", "tone_context"]
