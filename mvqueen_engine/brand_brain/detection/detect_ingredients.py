"""Ingredient signal detection for beauty/skincare products."""
from ._common import detect_many

VOCAB = {
    "hyaluronic acid": ("hyaluronic acid", "sodium hyaluronate"), "niacinamide": ("niacinamide",),
    "vitamin c": ("vitamin c", "ascorbic acid"), "retinol": ("retinol", "retinoid"),
    "peptides": ("peptide", "peptides"), "ceramides": ("ceramide", "ceramides"),
    "salicylic acid": ("salicylic acid",), "glycolic acid": ("glycolic acid",),
    "lactic acid": ("lactic acid",), "squalane": ("squalane",), "aloe": ("aloe", "aloe vera"),
    "jojoba": ("jojoba",), "shea butter": ("shea butter",), "vitamin e": ("vitamin e", "tocopherol"),
    "green tea": ("green tea",), "caffeine": ("caffeine",), "honey": ("honey",),
}

def detect_ingredients(text: str) -> list[str]:
    return detect_many(text, VOCAB)
