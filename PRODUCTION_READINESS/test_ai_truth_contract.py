#!/usr/bin/env python3
"""Regression tests for MVQUEEN AI factual-truth boundaries."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_PROMPT_FILES = (
    "10_AI_Systems/AI_Prompt_Library.md",
    "10_AI_Systems/Product_Description_Prompts.md",
    "10_AI_Systems/Ad_Copy_Prompts.md",
    "10_AI_Systems/AI_Workflows.md",
)

UNSAFE_EXAMPLE_PATTERNS = (
    "Visible difference in 4 days",
    "Glow in 4 days",
    "The serum our customers repurchase most",
    "The most repurchased product in our collection",
    "8-hour wear",
    "Guaranteed.",
)

class AITruthContractTests(unittest.TestCase):
    def read(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_active_prompt_files_exist(self):
        for rel in ACTIVE_PROMPT_FILES:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_master_prompt_has_truth_gate(self):
        text = self.read("10_AI_Systems/AI_Prompt_Library.md")
        self.assertIn("PRODUCT & COMMERCE TRUTH GATE", text)
        self.assertIn("verified source facts outrank stylistic goals", text)

    def test_product_prompt_has_truth_gate(self):
        text = self.read("10_AI_Systems/Product_Description_Prompts.md")
        self.assertIn("Factual Product Truth Gate", text)
        self.assertIn("When a fact is missing, omit it", text)

    def test_ad_prompt_has_evidence_gate(self):
        text = self.read("10_AI_Systems/Ad_Copy_Prompts.md")
        self.assertIn("MVQueen Advertising Evidence Gate", text)
        self.assertIn("Never invent reviews", text)

    def test_workflow_requires_canonical_evidence(self):
        text = self.read("10_AI_Systems/AI_Workflows.md")
        self.assertIn("No AI output may invent product or store facts", text)

    def test_known_unsupported_examples_are_absent(self):
        combined = "\n".join(self.read(rel) for rel in ACTIVE_PROMPT_FILES)
        for pattern in UNSAFE_EXAMPLE_PATTERNS:
            self.assertNotIn(pattern, combined, pattern)

    def test_learning_cannot_override_truth(self):
        text = self.read("agents/PRODUCTION_SPECIALIST_AGENT_SYSTEM.md")
        self.assertIn("protected data and factual truth", text)
        self.assertIn("Learning never grants new permissions", text)

if __name__ == "__main__":
    unittest.main()
