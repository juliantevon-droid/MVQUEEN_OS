"""Deprecated Android path wrapper retained for compatibility.

No hard-coded device path or import-time execution remains.
"""
from __future__ import annotations

from mvqueen_engine.main import cli


if __name__ == "__main__":
    raise SystemExit(cli())
