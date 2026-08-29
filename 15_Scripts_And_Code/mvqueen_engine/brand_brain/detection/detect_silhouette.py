"""Fashion silhouette detection."""
from __future__ import annotations

SILHOUETTES = ("oversized", "relaxed", "fitted", "slim", "tailored", "bodycon", "a-line", "wrap", "cropped", "wide-leg", "straight-leg", "high-rise", "low-rise", "asymmetric", "structured")

def detect_silhouette(text: str) -> str:
    value = str(text or "").lower()
    return next((item for item in SILHOUETTES if item in value), "unspecified")
