"""Portable filesystem paths for Android, Colab, and desktop execution."""
from __future__ import annotations
from pathlib import Path
import os


def runtime_root() -> Path:
    configured = os.getenv("MVQ_RUNTIME_ROOT")
    return Path(configured).expanduser().resolve() if configured else Path.cwd().resolve()


def export_dir() -> Path:
    path = runtime_root() / "MVQ_Exports"
    path.mkdir(parents=True, exist_ok=True)
    return path


def input_path(filename: str = "shopify_input.csv") -> Path:
    return runtime_root() / filename
