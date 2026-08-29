"""Brand mood/vibe detection."""
from __future__ import annotations

VIBES = {"quiet_luxury": ("quiet luxury", "minimal", "understated", "refined"), "statement": ("statement", "bold", "dramatic", "standout"), "romantic": ("romantic", "feminine", "floral", "lace"), "modern": ("modern", "contemporary", "clean", "sleek"), "effortless": ("effortless", "easy", "relaxed", "lightweight")}

def detect_vibe(text: str) -> str:
    value = str(text or "").lower()
    scores = {name: sum(term in value for term in terms) for name, terms in VIBES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "refined"
