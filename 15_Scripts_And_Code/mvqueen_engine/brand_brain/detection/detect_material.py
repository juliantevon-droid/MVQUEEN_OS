"""Material/fabric detection."""
from __future__ import annotations

MATERIALS = ("silk", "satin", "cashmere", "wool", "cotton", "linen", "leather", "suede", "denim", "velvet", "lace", "mesh", "nylon", "polyester", "rayon", "viscose", "spandex", "acrylic", "gold", "silver", "stainless steel", "ceramic", "glass")

def detect_material(text: str) -> str:
    value = str(text or "").lower()
    return next((material for material in MATERIALS if material in value), "unspecified")
