# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — BATCH PROCESSOR (BLOCK M)
# ---------------------------------------------------------

import csv
from concurrent.futures import ThreadPoolExecutor
from mvqueen_engine.engine import run


def process_row(text: str) -> dict:
    """
    Process a single text input through the Omniluxe Engine
    and return the Shopify-ready CSV row.
    """
    result = run(text)
    return result["csv_row"]


def process_csv(input_path: str, output_path: str, workers: int = 4):
    """
    Batch-process an input CSV containing an 'input_text' column.
    Produces a Shopify-ready CSV with deterministic column ordering.
    """

    # ---------------------------------------------------------
    # LOAD INPUT CSV
    # ---------------------------------------------------------
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if "input_text" not in reader.fieldnames:
            raise ValueError(
                "Input CSV must contain a column named 'input_text'."
            )

        texts = [row["input_text"] for row in reader]

    # ---------------------------------------------------------
    # PARALLEL PROCESSING
    # ---------------------------------------------------------
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(process_row, texts))

    if not results:
        raise ValueError("No rows were processed — input CSV may be empty.")

    # ---------------------------------------------------------
    # USE DETERMINISTIC COLUMN ORDER FROM FIRST ROW
    # ---------------------------------------------------------
    fieldnames = list(results[0].keys())

    # ---------------------------------------------------------
    # WRITE OUTPUT CSV
    # ---------------------------------------------------------
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    return output_path