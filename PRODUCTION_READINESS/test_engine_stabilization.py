from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT / "15_Scripts_And_Code"
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))


class EngineStabilizationTests(unittest.TestCase):
    def test_canonical_engine_modules_import(self):
        modules = [
            "mvqueen_engine.config",
            "mvqueen_engine.deterministic",
            "mvqueen_engine.brand_governance",
            "mvqueen_engine.catalog_safety",
            "mvqueen_engine.catalog_guard",
            "mvqueen_engine.catalog_dry_run",
            "mvqueen_engine.catalog_recovery_transform",
            "mvqueen_engine.catalog_processor.processor",
            "mvqueen_engine.catalog_processor.csv_loader",
            "mvqueen_engine.phase1_csv",
            "mvqueen_engine.main",
            "mvqueen_engine.control_panel",
        ]
        for name in modules:
            with self.subTest(module=name):
                importlib.import_module(name)

    def test_legacy_all_in_one_engine_fails_closed(self):
        engine = importlib.import_module("mvqueen_engine.engine")
        with self.assertRaisesRegex(RuntimeError, "legacy generative engine is retired"):
            engine.run("sample")

    def test_python_direct_shopify_path_fails_closed(self):
        processor = importlib.import_module("mvqueen_engine.catalog_processor.processor")
        with self.assertRaisesRegex(RuntimeError, "Direct Shopify catalog processing is disabled"):
            processor.process_shopify_catalog()

    def test_old_price_and_runtime_bypass_removed_from_phase1(self):
        text = (ENGINE_ROOT / "mvqueen_engine" / "phase1_csv.py").read_text(encoding="utf-8")
        self.assertNotIn("run_mvqueen", text)
        self.assertNotIn("Variant Compare At Price", text)

    def test_control_panel_has_no_live_shopify_action(self):
        text = (ENGINE_ROOT / "mvqueen_engine" / "control_panel.py").read_text(encoding="utf-8")
        self.assertNotIn("process_shopify_catalog", text)
        self.assertNotIn("Run Shopify Mode", text)
        self.assertNotIn("Full Pipeline (CSV", text)

    def test_brand_term_matching_uses_real_word_boundaries(self):
        governance = importlib.import_module("mvqueen_engine.brand_governance")
        self.assertTrue(governance.contains_term("MYS Brand Lipstick", "MYS"))
        self.assertFalse(governance.contains_term("a mysterious fragrance", "MYS"))
        self.assertFalse(governance.contains_term("nail grinder", "grind"))
        self.assertTrue(governance.contains_term("grind culture", "grind"))

    def test_deterministic_compatibility_is_stable(self):
        d = importlib.import_module("mvqueen_engine.deterministic")
        seed = d.deterministic_seed("MVQUEEN")
        self.assertEqual(seed, d.deterministic_seed("MVQUEEN"))
        self.assertEqual(
            d.deterministic_choice(seed, ["a", "b", "c"], salt="x"),
            d.deterministic_choice(seed, ["a", "b", "c"], salt="x"),
        )


    def test_legacy_runtime_and_processor_fail_closed(self):
        runtime = importlib.import_module("mvqueen_engine.runtime")
        with self.assertRaisesRegex(RuntimeError, "legacy runtime is retired"):
            runtime.run_mvqueen({"title": "sample"})

        processors = importlib.import_module("mvqueen_engine.processors")
        with self.assertRaisesRegex(RuntimeError, "legacy Omniluxe processor is retired"):
            processors.process_product("sample")

    def test_legacy_metafield_generators_fail_closed(self):
        direct = importlib.import_module("mvqueen_engine.metafield_engine")
        with self.assertRaisesRegex(RuntimeError, "legacy metafield generator is retired"):
            direct.generate_metafields("sample")

        nested = importlib.import_module("mvqueen_engine.metafields.metafield_engine")
        with self.assertRaisesRegex(RuntimeError, "legacy metafield generator is retired"):
            nested.generate_metafields("sample")


if __name__ == "__main__":
    unittest.main()
