import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXECUTOR_PATH = ROOT / "30_System_Infrastructure/overseer/agent_executor.py"
REGISTRY_PATH = ROOT / "30_System_Infrastructure/overseer/agent_registry.json"

spec = importlib.util.spec_from_file_location("mvq_agent_executor", EXECUTOR_PATH)
executor = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(executor)


class AgentExecutionLayerTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_has_all_production_specialists_and_no_write_authority(self):
        ids = {a["id"] for a in self.registry["agents"]}
        self.assertEqual(
            ids,
            {
                "catalog", "editorial", "seo", "merchandising", "conversion",
                "mobile_ux", "theme", "shopify", "data", "performance",
                "accessibility", "security", "qa", "release",
            },
        )
        self.assertEqual(len(ids), 14)
        self.assertFalse(any(a["can_mutate_production"] for a in self.registry["agents"]))
        self.assertFalse(self.registry["execution_policy"]["production_mutation_allowed"])

    def test_blocking_finding_executes_but_remains_on_release_hold(self):
        assignments = {
            "source": "fixture",
            "assignments": [{
                "finding_id": "MVQ-FINDING-00001",
                "owner": "security",
                "reviewers": ["qa", "release"],
                "severity": "CRITICAL",
                "category": "security",
                "path": "example.py",
                "message": "possible secret",
                "confidence": "verified",
                "conversion_impact": "none",
                "state": "triage",
                "production_blocking": True,
                "required_flow": [
                    "specialist_analysis", "recommendation", "qa_verification",
                    "release_disposition", "outcome_record",
                ],
            }],
        }
        report = executor.execute(assignments, self.registry)
        self.assertEqual(report["registered_agent_count"], 14)
        self.assertEqual(report["run_count"], 1)
        self.assertFalse(report["production_mutation_performed"])
        run = report["runs"][0]
        self.assertEqual(run["specialist_analysis"]["state"], "completed")
        self.assertEqual(run["qa_verification"]["state"], "pending_change")
        self.assertEqual(run["release_disposition"]["state"], "HOLD")
        self.assertFalse(run["specialist_analysis"]["automatic_production_mutation"])

    def test_unknown_agent_fails_closed(self):
        assignments = {
            "assignments": [{
                "finding_id": "MVQ-FINDING-00002",
                "owner": "unknown-agent",
                "reviewers": ["qa"],
                "severity": "LOW",
                "category": "unknown",
            }]
        }
        with self.assertRaises(ValueError):
            executor.execute(assignments, self.registry)


if __name__ == "__main__":
    unittest.main()
