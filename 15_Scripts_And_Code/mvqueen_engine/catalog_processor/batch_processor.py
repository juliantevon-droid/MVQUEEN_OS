"""Memory-safe batch orchestration for MVQueen catalog processing."""
from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path

import pandas as pd

from .csv_loader import iter_csv_chunks

DEFAULT_CHUNK_SIZE = 850


def _validate_chunk_size(chunk_size: int) -> None:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")


def process_chunks(
    input_path: str | Path,
    processor: Callable[[pd.DataFrame], pd.DataFrame],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> Iterable[pd.DataFrame]:
    """Process a CSV incrementally so large catalogs do not require full RAM."""
    _validate_chunk_size(chunk_size)
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"CSV not found: {source}")
    for chunk in iter_csv_chunks(str(source), chunk_size=chunk_size):
        result = processor(chunk.copy())
        if not isinstance(result, pd.DataFrame):
            raise TypeError("processor must return a pandas DataFrame")
        yield result


def write_processed_chunks(
    input_path: str | Path,
    output_path: str | Path,
    processor: Callable[[pd.DataFrame], pd.DataFrame],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> str:
    """Write processed chunks to one CSV with a single header."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    first = True
    for result in process_chunks(input_path, processor, chunk_size):
        result.to_csv(destination, mode="w" if first else "a", header=first, index=False)
        first = False
    if first:
        pd.DataFrame().to_csv(destination, index=False)
    return str(destination)


def process_dataframe_in_batches(
    df: pd.DataFrame,
    processor: Callable[[pd.DataFrame], pd.DataFrame],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> pd.DataFrame:
    """Process an existing DataFrame in bounded batches while preserving order."""
    _validate_chunk_size(chunk_size)
    pieces: list[pd.DataFrame] = []
    for start in range(0, len(df), chunk_size):
        result = processor(df.iloc[start:start + chunk_size].copy())
        if not isinstance(result, pd.DataFrame):
            raise TypeError("processor must return a pandas DataFrame")
        pieces.append(result)
    return pd.concat(pieces, ignore_index=True) if pieces else df.copy()


__all__ = [
    "DEFAULT_CHUNK_SIZE",
    "process_chunks",
    "write_processed_chunks",
    "process_dataframe_in_batches",
]
