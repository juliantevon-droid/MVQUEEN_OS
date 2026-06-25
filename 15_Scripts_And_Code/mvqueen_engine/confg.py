# mvqueen_engine/control_panel/config.py
"""
PHASE 0 — PLATFORM CONFIGURATION
Controls:
- Engine behavior
- System behavior
- Platform behavior
- Editorial modes
- Persona intensity
- SEO modes
- Metafield modes
- Overwrite rules
- Android-safe settings
"""

from dataclasses import dataclass


# -----------------------------
# EDITORIAL SETTINGS
# -----------------------------
@dataclass
class EditorialSettings:
    description_length: str = "long"      # short | medium | long
    persona_mode: str = "full"            # off | light | full
    tone_mode: str = "dynamic"            # neutral | dynamic | persona
    include_benefits: bool = True
    include_ingredients: bool = True
    include_frames: bool = True
    include_sensory: bool = True
    include_storytelling: bool = True


# -----------------------------
# SEO SETTINGS
# -----------------------------
@dataclass
class SEOSettings:
    seo_mode: str = "enhanced"            # minimal | enhanced | aggressive
    max_title_length: int = 70
    max_description_length: int = 155
    include_keywords: bool = True
    include_semantic_variants: bool = True
    include_longtail: bool = True


# -----------------------------
# METAFIELD SETTINGS
# -----------------------------
@dataclass
class MetafieldSettings:
    generate_metafields: bool = True
    include_materials: bool = True
    include_silhouette: bool = True
    include_benefits: bool = True
    include_routine: bool = True
    include_texture: bool = True
    include_finish: bool = True
    include_emotion: bool = True
    include_quality_score: bool = True


# -----------------------------
# OVERWRITE RULES
# -----------------------------
@dataclass
class OverwriteRules:
    overwrite_titles: str = "smart"       # never | smart | always
    overwrite_descriptions: str = "smart" # never | smart | always
    overwrite_seo: str = "always"         # never | smart | always
    overwrite_metafields: str = "always"  # never | smart | always
    overwrite_tags: str = "always"        # never | smart | always


# -----------------------------
# ANDROID / MEMORY SETTINGS
# -----------------------------
@dataclass
class AndroidSettings:
    memory_safe_mode: bool = True
    chunk_size: int = 500                 # safe for Pydroid
    temp_directory: str = "/sdcard/mvqueen/tmp"


# -----------------------------
# SYSTEM SETTINGS
# -----------------------------
@dataclass
class SystemSettings:
    batch_size: int = 50
    dry_run: bool = False
    verbose: bool = True
    log_to_file: bool = True
    log_path: str = "mvqueen_logs.txt"


# -----------------------------
# PLATFORM CONFIG ROOT
# -----------------------------
@dataclass
class PlatformConfig:
    editorial: EditorialSettings = EditorialSettings()
    seo: SEOSettings = SEOSettings()
    metafields: MetafieldSettings = MetafieldSettings()
    overwrite: OverwriteRules = OverwriteRules()
    android: AndroidSettings = AndroidSettings()
    system: SystemSettings = SystemSettings()


# Global instance
CONFIG = PlatformConfig()