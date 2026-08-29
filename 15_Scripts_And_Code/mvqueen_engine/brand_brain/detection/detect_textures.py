"""Texture and tactile finish detection."""
from __future__ import annotations

TEXTURES = ("smooth", "soft", "soft-touch", "silky", "creamy", "velvety", "plush", "lightweight", "structured", "ribbed", "textured", "buttery", "powdery", "gel", "balmy", "dewy", "matte")

def detect_textures(text: str) -> list[str]:
    value = str(text or "").lower()
    return [texture for texture in TEXTURES if texture in value]
