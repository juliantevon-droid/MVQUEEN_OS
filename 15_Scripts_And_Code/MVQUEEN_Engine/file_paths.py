# android/file_paths.py
"""
MVQueen File Path Manager — Enterprise Edition
----------------------------------------------

Provides deterministic, Android-safe file paths for:
- Data storage
- Cache
- Exports
- Engine-level directories
"""

import os
from control_panel.config import load_config


# ------------------------------------------------------------
# GET ROOT PATHS FROM CONFIG
# ------------------------------------------------------------
def get_engine_paths() -> dict:
    """
    Returns all engine paths from config, ensuring directories exist.
    """

    cfg = load_config()
    paths = cfg.get("paths", {})

    resolved = {
        "data": os.path.abspath(paths.get("data_root", "data/")),
        "cache": os.path.abspath(paths.get("cache_root", "cache/")),
        "export": os.path.abspath(paths.get("export_root", "exports/")),
    }

    # Ensure directories exist
    for p in resolved.values():
        if not os.path.exists(p):
            os.makedirs(p, exist_ok=True)

    return resolved


__all__ = ["get_engine_paths"]