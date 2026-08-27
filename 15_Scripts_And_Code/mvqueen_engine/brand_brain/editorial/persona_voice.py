"""Persona-aware voice controls for MVQueen editorial."""

from typing import Any, Mapping

DEFAULT_TONE = "refined, confident, modern, and concise"


def build_voice_context(context: Mapping[str, Any] | None = None) -> dict[str, str]:
    data = dict(context or {})
    return {
        "persona": str(data.get("persona") or "").strip(),
        "voice": str(data.get("voice") or "luxury-modern-elegant").strip(),
        "tone": str(data.get("tone") or DEFAULT_TONE).strip(),
        "pacing": str(data.get("pacing") or "measured").strip(),
        "intensity": str(data.get("intensity") or "medium").strip(),
    }


def apply_persona_voice(text: str, context: Mapping[str, Any] | None = None) -> str:
    """Return clean editorial text while exposing persona controls to callers.

    Actual persona vocabulary is supplied by the brand brain; this function
    intentionally avoids adding unsupported claims or canned persona text.
    """
    _ = build_voice_context(context)
    return " ".join(str(text or "").split()).strip()
