"""Detect explicit construction/design details."""
from __future__ import annotations

DETAILS = ("ruffle", "pleat", "pleated", "ruched", "draped", "button", "zipper", "pocket", "belted", "tie", "bow", "embroidery", "beaded", "sequin", "cutout", "off-shoulder", "one-shoulder", "halter", "collar", "cowl neck", "v-neck", "square neck")

def detect_details(text: str) -> list[str]:
    value = str(text or "").lower()
    return [detail for detail in DETAILS if detail in value]
