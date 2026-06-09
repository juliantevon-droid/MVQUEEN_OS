# ============================================================
# BLOCK 40 — RUNTIME ENGINE (FINAL VERSION)
# ============================================================

from __future__ import annotations
from typing import Dict, Any

from engine.engine_core import (
    build_title,
)
from engine.handle_engine import generate_handle
from engine.editorial_engine import generate_editorial
from engine.seo_engine import generate_seo
from engine.metafield_engine import generate_metafields
from engine.price_engine import generate_price
from engine.image_engine import generate_image_data
from engine.validation_engine import validate_product


# ------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ------------------------------------------------------------

def run_mvqueen(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full MVQueen pipeline.
    Input:  raw product dict
    Output: enriched product dict with:
      - title
      - handle
      - editorial_html
      - seo (keywords, meta, alt, canonical, seo metafields)
      - metafields
      - price + compare_at + price tags/collections
      - image_data (colors, materials, finishes, textures, alt_text, tags)
      - validation report
    """

    # --------------------------------------------------------
    # 1. Title
    # --------------------------------------------------------
    product["title"] = build_title(product)

    # --------------------------------------------------------
    # 2. Handle
    # --------------------------------------------------------
    product["handle"] = generate_handle(product)

    # --------------------------------------------------------
    # 3. Editorial (HTML)
    # --------------------------------------------------------
    editorial_html = generate_editorial(product)
    product["editorial_html"] = editorial_html

    # --------------------------------------------------------
    # 4. SEO
    # --------------------------------------------------------
    seo = generate_seo(product)
    product["seo"] = seo
    product["primary_keyword"] = seo.get("primary_keyword")

    # --------------------------------------------------------
    # 5. Image Data
    # --------------------------------------------------------
    image_data = generate_image_data(product)
    product["image_data"] = image_data

    # --------------------------------------------------------
    # 6. Metafields
    # --------------------------------------------------------
    metafields = generate_metafields(product)
    product["metafields"] = metafields

    # --------------------------------------------------------
    # 7. Price
    # --------------------------------------------------------
    price_info = generate_price(product)
    product["price"] = price_info["price"]
    product["compare_at_price"] = price_info["compare_at_price"]
    product["price_tags"] = price_info["price_tags"]
    product["price_collections"] = price_info["price_collections"]

    # --------------------------------------------------------
    # 8. Validation
    # --------------------------------------------------------
    validation = validate_product(product)
    product["validation"] = validation

    return product