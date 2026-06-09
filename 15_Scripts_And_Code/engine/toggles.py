# control_panel/toggles.py
"""
MVQueen Feature Toggle Definitions
----------------------------------

Defines all available feature toggles that can be
enabled or disabled via config.py.
"""

FEATURE_TOGGLES = {
    "enable_frames": "Controls editorial framing paragraphs",
    "enable_persona_voice": "Controls persona-tone blending",
    "enable_seo_block": "Controls SEO block generation",
    "enable_bundle_generation": "Controls bundle creation",
    "enable_business_tiers": "Controls business tier vocab",
}

__all__ = ["FEATURE_TOGGLES"]