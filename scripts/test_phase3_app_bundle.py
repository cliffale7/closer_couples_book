#!/usr/bin/env python3
"""Checks for the public Android content bundle."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_app_content as app_export  # noqa: E402


class AppBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.zip_path = app_export.build_bundle(Path(cls.tmp.name), "test")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def read(self, name: str):
        with zipfile.ZipFile(self.zip_path) as archive:
            return json.loads(archive.read(name))

    def test_ids_and_variants(self):
        activities = self.read("activities.json")
        ids = [item["id"] for item in activities if item["kind"] == "chapter"]
        signatures = [item["id"] for item in activities if item["kind"] == "signature"]
        self.assertEqual(ids, [f"{number:03d}" for number in range(1, 109)])
        self.assertEqual(signatures, [f"S0{number}" for number in range(1, 7)])
        chapter = next(item for item in activities if item["id"] == "001")
        short = next(item for item in chapter["variants"] if item["variant_id"] == "short")
        self.assertEqual(short["estimated_minutes"], 10)
        self.assertEqual(short["time_category"], "5-10")
        self.assertTrue(chapter["prompt_ids"])
        prompts = self.read("prompts.json")
        self.assertEqual(len({item["id"] for item in prompts}), len(prompts))

    def test_hidden_key_and_no_private_paths(self):
        activities = self.read("activities.json")
        escape = next(item for item in activities if item["id"] == "103")
        hidden = [section for section in escape["sections"] if section["visibility"] == "hidden"]
        self.assertTrue(hidden)
        with zipfile.ZipFile(self.zip_path) as archive:
            names = "\n".join(archive.namelist())
            blob = archive.read("activities.json")
        self.assertNotIn("journal/private", names)
        self.assertNotIn(b"DO_NOT_COMMIT", blob)


if __name__ == "__main__":
    unittest.main()
