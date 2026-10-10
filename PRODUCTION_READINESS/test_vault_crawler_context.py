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
    def test_recovered_references_keep_security_checks_without_configuration_false_alarms(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            refs = root / "31_AI_Knowledge_Base/brand_sources/recovered"
            refs.mkdir(parents=True)
            historical = refs / "historical.txt"
            historical.write_text(
                "Shopify API version " + "2024-" + "01\n"
                + "historical-example" + ".myshopify.com\n"
                + "product" + "Update\n"
                + 'client_secret = "[REDACTED]"\n', encoding="utf-8",
            )
            output = root / "report.json"
            command = [sys.executable, str(CRAWLER), "--root", str(root), "--output", str(output), "--fail-on", "high"]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(output.read_text())
            self.assertEqual(report["configuration"]["api_versions"], {})
            self.assertEqual(report["configuration"]["shopify_domains"], {})
            self.assertEqual(report["findings"], [])
            (refs / "active_writer.py").write_text('QUERY = "product' + 'Update"\n', encoding="utf-8")
            result = subprocess.run(command, capture_output=True, text=True)
            report = json.loads(output.read_text())
            self.assertEqual(result.returncode, 1)
            self.assertTrue(any(f["category"] == "publishing_boundary" for f in report["findings"]))
            (refs / "active_writer.py").unlink()
            historical.write_text('client_secret = "' + "sensitive" + '-example-value"\n', encoding="utf-8")
            result = subprocess.run(command, capture_output=True, text=True)
            report = json.loads(output.read_text())
            self.assertEqual(result.returncode, 1)
            self.assertTrue(any(f["category"] == "security" and f["severity"] == "CRITICAL" for f in report["findings"]))

    def test_shopify_dates_are_ignored_without_suppressing_real_api_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            future_api = "2026-" + "10"
            (root / "status.md").write_text(
                "## Always-on Shopify product automation verification — "
                + future_api + "-02\n",
                encoding="utf-8",
            )
            (root / "health.json").write_text(
                json.dumps({
                    "webhook_checked_at": future_api + "-02T03:15:36Z",
                    "shopify_quarter_checks": [
                        "2026-" + quarter + "-02" for quarter in ("01", "04", "07", "10")
                    ],
                }),
                encoding="utf-8",
            )
            report_path = root / "report.json"
            command = [
                sys.executable, str(CRAWLER), "--root", str(root),
                "--output", str(report_path), "--fail-on", "high",
            ]

            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(report["configuration"]["api_versions"], {})
            self.assertEqual(report["findings"], [])

            # A dated note can still contain a genuine API version mismatch.
            (root / "status.md").write_text(
                "Shopify verified " + future_api + "-02; API version " + future_api + "\n",
                encoding="utf-8",
            )
            (root / "api_config.toml").write_text(
                'api_version = "' + future_api + '"\n', encoding="utf-8",
            )
            (root / "admin_api.txt").write_text(
                "/admin/api/" + future_api + "/graphql.json\n", encoding="utf-8",
            )
            report_path.unlink()
            report_path.with_suffix(".md").unlink()

            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(
                report["configuration"]["api_versions"],
                {future_api: ["admin_api.txt", "api_config.toml", "status.md"]},
            )
            self.assertEqual(len(report["findings"]), 1)
            self.assertEqual(report["findings"][0]["severity"], "HIGH")
            self.assertEqual(report["findings"][0]["category"], "config_drift")

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
