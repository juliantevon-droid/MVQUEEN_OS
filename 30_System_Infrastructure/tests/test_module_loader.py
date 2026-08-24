import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

LOADER_DIR = Path(__file__).resolve().parents[1] / "system" / "loader"
sys.path.insert(0, str(LOADER_DIR))
import module_loader


class ModuleLoaderTests(unittest.TestCase):
    def make_module(self, root, filename, content):
        path = root / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_module_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_module(root, "health.py", 'def boot():\n    return {"status": "ready"}\n')
            definition = {"name": "health", "path": ".", "entrypoint": "health.py", "enabled": True}
            with patch.object(module_loader, "REPO_ROOT", root), patch.object(module_loader, "MODULE_ROOT", root):
                self.assertEqual(module_loader.load_module(definition).boot()["status"], "ready")

    def test_missing_entrypoint_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            definition = {"name": "missing", "path": ".", "entrypoint": "missing.py", "enabled": True}
            with patch.object(module_loader, "REPO_ROOT", root), patch.object(module_loader, "MODULE_ROOT", root):
                with self.assertRaises(FileNotFoundError):
                    module_loader.load_module(definition)

    def test_module_without_boot_is_rejected_by_boot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_module(root, "no_boot.py", "VALUE = 123\n")
            definition = {"name": "no_boot", "path": ".", "entrypoint": "no_boot.py", "enabled": True}
            with patch.object(module_loader, "REPO_ROOT", root), patch.object(module_loader, "MODULE_ROOT", root), patch.object(module_loader, "load_registry", return_value={"system": "TEST", "modules": [definition]}), patch.object(module_loader, "load_state", return_value={}), patch.object(module_loader, "save_state"):
                result = module_loader.boot()
                self.assertEqual(result, [])

    def test_bad_boot_return_is_recorded_as_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_module(root, "bad.py", 'def boot():\n    return "ready"\n')
            definition = {"name": "bad", "path": ".", "entrypoint": "bad.py", "enabled": True}
            state = {}
            with patch.object(module_loader, "REPO_ROOT", root), patch.object(module_loader, "MODULE_ROOT", root), patch.object(module_loader, "load_registry", return_value={"system": "TEST", "modules": [definition]}), patch.object(module_loader, "load_state", return_value=state), patch.object(module_loader, "save_state"):
                module_loader.boot()
                self.assertEqual(len(state["module_errors"]), 1)
                self.assertIn("TypeError", state["module_errors"][0]["error"])

    def test_disabled_module_is_skipped(self):
        definition = {"name": "disabled", "path": ".", "entrypoint": "disabled.py", "enabled": False}
        with patch.object(module_loader, "load_registry", return_value={"system": "TEST", "modules": [definition]}), patch.object(module_loader, "load_state", return_value={}), patch.object(module_loader, "save_state"), patch.object(module_loader, "load_module") as mock_loader:
            self.assertEqual(module_loader.boot(), [])
            mock_loader.assert_not_called()

    def test_invalid_definition_is_recorded_without_crash(self):
        state = {}
        with patch.object(module_loader, "load_registry", return_value={"system": "TEST", "modules": [{"enabled": True}]}), patch.object(module_loader, "load_state", return_value=state), patch.object(module_loader, "save_state"):
            self.assertEqual(module_loader.boot(), [])
            self.assertEqual(len(state["module_errors"]), 1)

    def test_module_path_cannot_escape_module_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_root = root / "modules"
            module_root.mkdir()
            outside = root / "outside.py"
            outside.write_text("def boot(): return {'status': 'ready'}\n", encoding="utf-8")
            definition = {"name": "escape", "path": "modules/..", "entrypoint": "outside.py", "enabled": True}
            with patch.object(module_loader, "REPO_ROOT", root), patch.object(module_loader, "MODULE_ROOT", module_root):
                with self.assertRaises(ValueError):
                    module_loader.load_module(definition)


if __name__ == "__main__":
    unittest.main()
