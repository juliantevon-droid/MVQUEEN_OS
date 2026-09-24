"""Invariant tests for the single MVQUEEN_OS production architecture."""
# Unified cleanup revision: 2
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_LEGACY_BRAND_PATHS = {
    "core/brand_linter.py",
    "15_Scripts_And_Code/mvqueen_engine/catalog_guard.py",
    "15_Scripts_And_Code/mvqueen_engine/catalog_safety.py",
    "30_System_Infrastructure/catalog/mvqueen_catalog_worker.py",
    "30_System_Infrastructure/automation/validate_theme_contract.py",
    "PRODUCTION_READINESS/MVQUEEN_CATALOG_CONTRACT_V1.md",
    "PRODUCTION_READINESS/UNIFIED_SYSTEM_CONTRACT.md",
}

TEXT_SUFFIXES = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".liquid",
    ".json", ".yml", ".yaml", ".toml", ".txt", ".css",
}


class UnifiedSystemContractTests(unittest.TestCase):
    def test_workspace_and_backup_junk_is_not_active(self):
        forbidden_roots = [".obsidian", "_BACKUPS", ".trash", ".ttxfolder"]
        for rel in forbidden_roots:
            self.assertFalse((ROOT / rel).exists(), rel)

        self.assertFalse((ROOT / "MVQUEEN_CONTEXT.md").exists())
        self.assertFalse((ROOT / "pull_phase1.sh").exists())

        tracked = subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True
        ).splitlines()
        for rel in tracked:
            if rel.startswith("98_Archive/"):
                continue
            self.assertNotIn("__pycache__", rel)
            self.assertNotRegex(Path(rel).name, re.compile(r"conflict", re.I))

    def test_python_intelligence_has_no_shopify_network_transport(self):
        roots = [
            ROOT / "15_Scripts_And_Code/mvqueen_engine",
            ROOT / "30_System_Infrastructure/catalog",
        ]
        forbidden = [
            "requests.post(",
            "requests.put(",
            "requests.patch(",
            "requests.delete(",
            "urllib.request",
            "X-Shopify-Access-Token",
            "SHOPIFY_ACCESS_TOKEN",
        ]
        for folder in roots:
            for path in folder.rglob("*.py"):
                text = path.read_text(encoding="utf-8", errors="replace")
                for marker in forbidden:
                    self.assertNotIn(marker, text, f"{marker} in {path.relative_to(ROOT)}")

    def test_react_app_is_only_declared_live_writer(self):
        text = (ROOT / "app/lib/product-processor.ts").read_text(encoding="utf-8")
        self.assertIn('MVQ_WRITE_ENABLED', text)
        self.assertIn('MVQ_APPROVED_PRODUCT_GIDS', text)
        self.assertIn('admin.graphql(PRODUCT_UPDATE', text)

    def test_drive_intake_never_pushes_to_git(self):
        text = (ROOT / ".github/workflows/mvqueen-drive-bridge.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", text)
        self.assertNotIn("git push", text)
        self.assertNotIn("git commit", text)

    def test_theme_is_self_contained(self):
        required = [
            "storefront/theme/config/settings_schema.json",
            "storefront/theme/config/settings_data.json",
            "storefront/theme/layout/theme.liquid",
            "storefront/theme/locales/en.default.json",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_active_brand_documents_use_miss_princess(self):
        legacy = re.compile(r"MISS\.?\s*QUEEN|Miss\.?\s+Queen")
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel.startswith("98_Archive/") or rel in ALLOWED_LEGACY_BRAND_PATHS:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            self.assertIsNone(legacy.search(text), f"legacy sister-brand reference in {rel}")


if __name__ == "__main__":
    unittest.main()
