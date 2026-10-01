from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRAWLER = ROOT / "core" / "vault_crawler.py"


class VaultCrawlerContextTests(unittest.TestCase):
    def test_dates_and_reference_signatures_do_not_become_false_highs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "30_System_Infrastructure/system/state").mkdir(parents=True)
            (root / "PRODUCTION_READINESS").mkdir(parents=True)

            (root / "30_System_Infrastructure/system/state/system_state.json").write_text(
                json.dumps({"last_boot": "2026-10-01T11:00:00Z"}),
                encoding="utf-8",
            )

            write_token = "product" + "Update"
            request_token = "requests" + ".post"
            (root / "PRODUCTION_READINESS/deep_repo_audit.py").write_text(
                f'WRITE_MARKERS = ("{write_token}", "{request_token}")\n',
                encoding="utf-8",
            )
            (root / "PRODUCTION_READINESS/test_catalog_recovery_controls.py").write_text(
                f'FORBIDDEN_TRANSPORT = ("{write_token}(", "{request_token}(")\n',
                encoding="utf-8",
            )

            (root / "real_writer.py").write_text(
                f'QUERY = "mutation {{ {write_token}(input: $input) {{ product {{ id }} }} }}"\n',
                encoding="utf-8",
            )
            (root / "api_config.txt").write_text(
                "Canonical check fixture: Shopify API version " + "2026-" + "10\\n",
                encoding="utf-8",
            )

            report_path = root / "report.json"
            subprocess.run(
                [
                    sys.executable,
                    str(CRAWLER),
                    "--root",
                    str(root),
                    "--output",
                    str(report_path),
                    "--fail-on",
                    "none",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            report = json.loads(report_path.read_text(encoding="utf-8"))
            publishing = [
                f for f in report["findings"]
                if f["severity"] == "HIGH" and f["category"] == "publishing_boundary"
            ]
            drift = [
                f for f in report["findings"]
                if f["severity"] == "HIGH" and f["category"] == "config_drift"
            ]

            self.assertEqual([f["path"] for f in publishing], ["real_writer.py"])
            self.assertEqual(len(drift), 1)
            self.assertEqual(drift[0]["path"], "api_config.txt")
            self.assertNotIn(
                "30_System_Infrastructure/system/state/system_state.json",
                report["configuration"]["api_versions"].get("2026-" + "10", []),
            )


if __name__ == "__main__":
    unittest.main()
