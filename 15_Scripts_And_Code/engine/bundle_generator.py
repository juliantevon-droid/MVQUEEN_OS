# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — BUNDLE GENERATOR (BLOCK N)
# ---------------------------------------------------------

from mvqueen_engine.engine import run
from mvqueen_engine.utils.deterministic import deterministic_seed, deterministic_choice


def generate_bundle(texts: list[str], discount: float = 0.0) -> dict:
    """
    Generate a deterministic bundle from multiple input texts.

    Args:
        texts: List of product input texts.
        discount: Percentage discount to apply to total price (0.0–1.0).

    Returns:
        A dictionary representing the bundle:
        {
            "bundle_title": str,
            "bundle_handle": str,
            "products": [product_dicts],
            "total_price": float,
            "discounted_price": float,
            "tags": [...],
            "collections": [...],
            "metafields": {...}
        }
    """

    # ---------------------------------------------------------
    # PROCESS ALL PRODUCTS
    # ---------------------------------------------------------
    processed = [run(t)["product"] for t in texts]

    # ---------------------------------------------------------
    # BUILD BUNDLE TITLE (DETERMINISTIC)
    # ---------------------------------------------------------
    seed = deterministic_seed("||".join(texts))

    title_options = [
        "Curated Essentials Bundle",
        "Signature Style Set",
        "Omniluxe Capsule Pack",
        "MVQueen Premium Bundle",
        "Editorial Favorites Set",
    ]

    bundle_title = deterministic_choice(seed, title_options, salt="bundle_title")

    # ---------------------------------------------------------
    # BUILD BUNDLE HANDLE (DETERMINISTIC)
    # ---------------------------------------------------------
    handle_base = bundle_title.lower().replace(" ", "-")
    bundle_handle = f"{handle_base}-{seed % 99999}"

    # ---------------------------------------------------------
    # MERGE TAGS + COLLECTIONS
    # ---------------------------------------------------------
    all_tags = set()
    all_collections = set()

    for p in processed:
        all_tags.update(p.get("tags", []))
        all_collections.update(p.get("collections", []))

    # ---------------------------------------------------------
    # PRICE CALCULATION
    # ---------------------------------------------------------
    total_price = sum(p.get("price", 0) for p in processed)
    discounted_price = round(total_price * (1 - discount), 2)

    # ---------------------------------------------------------
    # BUNDLE METAFIELDS
    # ---------------------------------------------------------
    metafields = {
        "bundle_size": len(processed),
        "bundle_discount": discount,
        "bundle_original_price": total_price,
        "bundle_final_price": discounted_price,
        "bundle_products": [p.get("handle") for p in processed],
    }

    # ---------------------------------------------------------
    # FINAL BUNDLE OBJECT
    # ---------------------------------------------------------
    return {
        "bundle_title": bundle_title,
        "bundle_handle": bundle_handle,
        "products": processed,
        "total_price": total_price,
        "discounted_price": discounted_price,
        "tags": sorted(all_tags),
        "collections": sorted(all_collections),
        "metafields": metafields,
    }