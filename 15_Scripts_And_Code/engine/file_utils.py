# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — FILE UTILITIES
# ---------------------------------------------------------

import csv
from pathlib import Path
from typing import List, Dict, Optional


# ---------------------------------------------------------
# READ CSV
# ---------------------------------------------------------

def read_csv(path: str) -> List[Dict[str, str]]:
    """
    Safely read a CSV file and return a list of dictionaries.
    Returns an empty list if the file does not exist or is empty.
    """
    p = Path(path)

    if not p.exists() or p.stat().st_size == 0:
        return []

    with p.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader) if reader.fieldnames else []


# ---------------------------------------------------------
# WRITE CSV
# ---------------------------------------------------------

def write_csv(path: str, rows: List[Dict[str, str]], fieldnames: Optional[List[str]] = None):
    """
    Write rows to a CSV file with deterministic column ordering.
    If fieldnames are not provided, they are inferred from the first row.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        # Write an empty file with no header
        p.write_text("", encoding="utf-8")
        return

    # Infer fieldnames if not provided
    if fieldnames is None:
        fieldnames = list(rows[0].keys())

    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)