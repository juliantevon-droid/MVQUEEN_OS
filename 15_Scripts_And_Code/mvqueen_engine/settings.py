# control_panel/settings.py
"""
MVQueen Global Engine Settings
------------------------------

Provides admin-level settings that extend config.py.
These settings are static defaults that rarely change,
but can be overridden by config.json.
"""

from typing import Dict, Any

ENGINE_SETTINGS: Dict[str, Any] = {
    "max_description_length": 1200,
    "max_seo_block_length": 800,
    "max_frames": 3,
    "default_persona": "editorial",
    "default_vibe": "luxury",
    "default_trend": "timeless",
}

__all__ = ["ENGINE_SETTINGS"]