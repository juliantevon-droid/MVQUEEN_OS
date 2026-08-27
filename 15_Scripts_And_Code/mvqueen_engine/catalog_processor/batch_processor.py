"""Memory-safe batch orchestration for MVQueen catalog processing."""
from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import pandas as pd

from .csv_loader import iter_csv_chunks


def process_chunks(
    input_path: str,
    processor: Callable[[pd.DataFrame], pd.DataFrame],
    chunk_size: int = 850,
) -> Iterable[pd.DataFrame]:
    """Process a CSV incrementally so large catalogs do not require full RAM."""
    for chunk in iter_csv_chunks(input_path, chunk_size=chunk_size):
        result = processor(chunk.copy())
        if not isinstance(result, pd.DataFrame):
            raise TypeError("processor must return a pandas DataFrame")
        yield result


def write_processed_chunks(
    input_path: str,
    output_path: str,
    processor: Callable[[pd.DataFrame], pd.DataFrame],
    chunk_size: int = 850,
) -> str:
    """Write processed chunks to one CSV with a single header."""
    first = True
    for result in process_chunks(input_path, processor, chunk_size):
        result.to_csv(output_path, mode="w" if first else "a", header=first, index=False)
        first = False
    if first:
        pd.DataFrame().to_csv(output_path, index=False)
    return output_path
