"""Material/fabric detection."""
from ._common import detect_one

VOCAB = {
    "Satin": ("satin",), "Silk": ("silk",), "Wool": ("wool",), "Cashmere": ("cashmere",),
    "Denim": ("denim",), "Cotton": ("cotton",), "Linen": ("linen",), "Leather": ("leather",),
    "Suede": ("suede",), "Velvet": ("velvet",), "Lace": ("lace",), "Knit": ("knit", "knitted"),
    "Polyester": ("polyester",), "Nylon": ("nylon",), "Mesh": ("mesh",),
}

def detect_material(text: str) -> str:
    return detect_one(text, VOCAB, seed="material")
