from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_ROOT = REPO_ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

"""CLI wrapper for the canonical offline recovery transformer."""

from mvqueen_engine.catalog_recovery_transform import main


if __name__ == "__main__":
    raise SystemExit(main())
