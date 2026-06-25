# ---------------------------------------------------------
# MVQUEEN OMNILUXE — VARIANT ENGINE
# ---------------------------------------------------------

from mvqueen_engine.utils.deterministic import (
    deterministic_seed,
    deterministic_choice
)

SIZES = ["XS", "S", "M", "L", "XL"]
COLORS = ["Black", "White", "Beige", "Navy", "Olive"]

def generate_variants(text: str) -> list:
    seed = deterministic_seed(text)

    # Deterministic color selection
    color = deterministic_choice(seed, COLORS, salt="variant_color")

    variants = []
    for size in SIZES:
        sku = f"{size}-{color}-{seed}"

        variants.append(
            {
                "option1": size,
                "option2": color,
                "sku": sku,
                "inventory_quantity": 50,
            }
        )

    return variants