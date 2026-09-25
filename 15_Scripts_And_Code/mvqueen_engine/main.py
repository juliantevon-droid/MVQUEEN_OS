"""Command-line entrypoint for governed offline CSV curation."""
from __future__ import annotations

import argparse

from mvqueen_engine.phase1_csv import run_products_csv


def cli() -> int:
    parser = argparse.ArgumentParser(
        description="Run MVQueen offline editorial curation. No Shopify writes are performed."
    )
    parser.add_argument("input_csv")
    parser.add_argument("output_csv")
    args = parser.parse_args()
    run_products_csv(args.input_csv, args.output_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
