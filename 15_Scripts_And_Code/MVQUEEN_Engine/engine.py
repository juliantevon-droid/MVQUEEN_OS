# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — PUBLIC ENTRY POINT (BLOCK J)
# ---------------------------------------------------------

from mvqueen_engine.catalog_processor.processor import process_product
from mvqueen_engine.catalog_processor.csv_loader import convert_to_csv_row

# ---------------------------------------------------------
# PUBLIC ENGINE WRAPPER
# ---------------------------------------------------------

def run(text: str) -> dict:
    """
    Public entry point for the MVQueen Omniluxe Engine.
    Returns:
        {
            "product": <full product dictionary>,
            "csv_row": <flattened Shopify-ready row>
        }
    """

    product = process_product(text)
    csv_row = convert_to_csv_row(product)

    return {
        "product": product,
        "csv_row": csv_row
    }