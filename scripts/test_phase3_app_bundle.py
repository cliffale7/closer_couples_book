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
        registry = Path(cls.tmp.name) / "prompt_registry.json"
        cls.zip_path = app_export.build_bundle(Path(cls.tmp.name), "test", registry_path=registry)
        cls.second_zip = app_export.build_bundle(
            Path(cls.tmp.name) / "second",
            "test",
            previous_zip=cls.zip_path,
            registry_path=registry,
        )

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
        self.assertIn("assets/assets/signatures/S01-hero.jpg", names)
        self.assertIn("assets/assets/covers/cover-front.jpg", names)
        self.assertNotIn("assets/assets/signatures/S01-hero.svg", names)
        self.assertNotIn("assets/assets/covers/cover-front.svg", names)

    def test_spoilers_and_app_update_are_explicit(self):
        activities = self.read("activities.json")
        escape = next(item for item in activities if item["id"] == "103")
        hidden = next(section for section in escape["sections"] if section["heading"] == "Facilitator section: solution key")
        self.assertEqual(hidden["visibility"], "hidden")
        self.assertTrue(hidden["spoiler"])
        self.assertEqual(hidden["spoiler_source"], "registry")
        self.assertTrue(escape["requires_app_update"])
        opening = next(item for item in activities if item["id"] == "001")
        self.assertFalse(opening["requires_app_update"])
        self.assertEqual(opening["mechanics"]["kind"], "narrative")

    def test_initial_and_noop_changes(self):
        changes = self.read("CHANGES.json")
        self.assertEqual(changes["baseline"], "initial")
        self.assertIsNone(changes["from_bundle"])
        self.assertIn("001", changes["added_activity_ids"])
        self.assertEqual(changes["changed_activity_ids"], [])
        with zipfile.ZipFile(self.second_zip) as archive:
            second = json.loads(archive.read("CHANGES.json"))
        self.assertEqual(second["baseline"], "update")
        self.assertEqual(second["changed_activity_ids"], [])
        self.assertEqual(second["added_activity_ids"], [])
        self.assertEqual(second["removed_activity_ids"], [])
        self.assertEqual(second["changed_assets"], [])

    def test_prompt_ids_do_not_renumber_when_a_question_is_inserted(self):
        registry = app_export.empty_registry()
        first = [
            {"activity_id": "001", "seat": "partner_a", "text": "Alpha question"},
            {"activity_id": "001", "seat": "partner_a", "text": "Beta question"},
        ]
        bound, _tombstones, registry = app_export.bind_prompts(first, registry)
        self.assertEqual([item["id"] for item in bound], ["001.partner_a.1", "001.partner_a.2"])
        inserted = [
            {"activity_id": "001", "seat": "partner_a", "text": "Gamma question"},
            {"activity_id": "001", "seat": "partner_a", "text": "Alpha question"},
            {"activity_id": "001", "seat": "partner_a", "text": "Beta question"},
        ]
        rebound, _tombstones, registry = app_export.bind_prompts(inserted, registry)
        by_text = {item["text"]: item["id"] for item in rebound}
        self.assertEqual(by_text["Alpha question"], "001.partner_a.1")
        self.assertEqual(by_text["Beta question"], "001.partner_a.2")
        self.assertEqual(by_text["Gamma question"], "001.partner_a.3")
        remaining, tombstones, _registry = app_export.bind_prompts(first[:1], registry)
        self.assertEqual(remaining[0]["id"], "001.partner_a.1")
        self.assertIn("001.partner_a.2", {item["id"] for item in tombstones})

    def test_changed_bundle_reports_the_hash_difference(self):
        previous = {
            "name": "old.zip",
            "activities": [{"id": "001", "content_hash": "aaa"}, {"id": "002", "content_hash": "bbb"}],
            "prompts": [{"id": "001.shared.1", "text": "Old"}],
            "assets": {"assets/assets/covers/cover-front.svg": "111"},
        }
        current = {
            "activities": [{"id": "001", "content_hash": "ccc"}, {"id": "003", "content_hash": "ddd"}],
            "prompts": [{"id": "001.shared.1", "text": "New"}, {"id": "003.shared.1", "text": "Added"}],
            "assets": {"assets/assets/covers/cover-front.svg": "222", "assets/assets/covers/cover-back.svg": "333"},
        }
        changes = app_export.changes_from_payloads(previous, current, [])
        self.assertEqual(changes["baseline"], "update")
        self.assertEqual(changes["changed_activity_ids"], ["001"])
        self.assertEqual(changes["removed_activity_ids"], ["002"])
        self.assertEqual(changes["added_activity_ids"], ["003"])
        self.assertEqual(changes["changed_prompt_ids"], ["001.shared.1"])
        self.assertEqual(changes["added_prompt_ids"], ["003.shared.1"])
        self.assertEqual(changes["changed_assets"], ["assets/assets/covers/cover-front.svg"])
        self.assertEqual(changes["added_assets"], ["assets/assets/covers/cover-back.svg"])


if __name__ == "__main__":
    unittest.main()
