"""Texture and tactile-signal detection."""
from ._common import detect_many

VOCAB = {
    "smooth": ("smooth",), "soft-touch": ("soft-touch", "soft touch"), "lightweight": ("lightweight", "light weight"),
    "structured": ("structured",), "velvety": ("velvet", "velvety"), "creamy": ("creamy", "cream texture"),
    "silky": ("silky", "silk-like"), "ribbed": ("ribbed", "rib knit"), "woven": ("woven",),
    "plush": ("plush",), "sheer": ("sheer",), "matte": ("matte",),
}

def detect_textures(text: str) -> list[str]:
    return detect_many(text, VOCAB)
