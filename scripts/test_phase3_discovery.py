#!/usr/bin/env python3
"""Discovery regression cases for Phase 3 time shelves and Surprise Us."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import catalog_variants  # noqa: E402
import surprise_us  # noqa: E402


def by_id(rows):
    found = {}
    for row in rows:
        found.setdefault(row.activity_id, []).append(row)
    return found


class VariantShelfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = [row for row in catalog_variants.load_variants() if row.time_category]
        cls.grouped = by_id(cls.rows)

    def variant(self, activity_id, variant_id):
        matches = [row for row in self.grouped[activity_id] if row.variant_id == variant_id]
        self.assertEqual(len(matches), 1, f"{activity_id} {variant_id}")
        return matches[0]

    def test_001_short_and_standard(self):
        short = self.variant("001", "short")
        standard = self.variant("001", "standard")
        self.assertEqual(short.estimated_minutes, 10)
        self.assertEqual(short.time_category, "5-10")
        self.assertEqual(standard.estimated_minutes, 30)
        self.assertEqual(standard.time_category, "20-45")
        self.assertEqual(short.anchor, "chapter-001")
        self.assertTrue(short.link_anchor.endswith("three-ways-to-play"))

    def test_017_short_gaze(self):
        short = self.variant("017", "short")
        self.assertEqual(short.estimated_minutes, 8)
        self.assertEqual(short.time_category, "5-10")
        self.assertFalse(short.touch)

    def test_043_short_twenty(self):
        short = self.variant("043", "short")
        self.assertEqual(short.estimated_minutes, 20)
        self.assertEqual(short.time_category, "10-20")

    def test_071_is_one_day(self):
        short = self.variant("071", "short")
        standard = self.variant("071", "standard")
        self.assertEqual(short.estimated_minutes, 240)
        self.assertEqual(standard.estimated_minutes, 720)
        self.assertEqual(short.time_category, "long-day")
        self.assertEqual(standard.time_category, "long-day")
        self.assertFalse(short.is_multi_day)
        self.assertFalse(any(row.variant_id == "extended" for row in self.grouped["071"]))

    def test_s01_variants(self):
        short = self.variant("S01", "short")
        standard = self.variant("S01", "standard")
        self.assertEqual(short.estimated_minutes, 45)
        self.assertEqual(short.time_category, "20-45")
        self.assertEqual(standard.estimated_minutes, 120)
        self.assertEqual(standard.time_category, "90-180")
        self.assertEqual(short.anchor, "signature-s01")

    def test_s02_about_prefix(self):
        short = self.variant("S02", "short")
        standard = self.variant("S02", "standard")
        self.assertEqual(short.estimated_minutes, 30)
        self.assertEqual(short.time_category, "20-45")
        self.assertEqual(standard.estimated_minutes, 90)
        self.assertEqual(standard.time_category, "45-90")

    def test_multi_day_closing_talk_is_not_a_quick_session(self):
        for activity_id in ("032", "048", "099"):
            rows = self.grouped[activity_id]
            self.assertTrue(rows)
            self.assertTrue(all(row.time_category == "multi-day" for row in rows), activity_id)

    def test_signatures_present(self):
        for activity_id in ("S01", "S02", "S03", "S04", "S05", "S06"):
            self.assertIn(activity_id, self.grouped)

    def test_every_indexed_variant_has_a_shelf(self):
        for row in self.rows:
            self.assertIn(row.time_category, catalog_variants.SHELF_ORDER)


class SurpriseFilterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = [row for row in catalog_variants.load_variants() if row.time_category]

    def test_quick_shelf_can_select_001_short(self):
        chosen = surprise_us.eligible(self.rows, {"time_band": {"5-10"}})
        keys = {(row.activity_id, row.variant_id) for row in chosen}
        self.assertIn(("001", "short"), keys)
        self.assertNotIn(("001", "standard"), keys)
        self.assertTrue(all(row.time_category == "5-10" for row in chosen))

    def test_strict_low_energy(self):
        chosen = surprise_us.eligible(self.rows, {"energy": {"low"}})
        self.assertTrue(chosen)
        self.assertTrue(all(row.energy == "low" for row in chosen))

    def test_strict_touch_no_keeps_017(self):
        chosen = surprise_us.eligible(self.rows, {"touch": {"no"}})
        self.assertTrue(all(row.touch is False for row in chosen))
        keys = {(row.activity_id, row.variant_id) for row in chosen}
        self.assertIn(("017", "short"), keys)

    def test_no_match_does_not_relax(self):
        script = ROOT / "scripts" / "surprise_us.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--format", "not-a-real-format", "--seed", "1"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("No activity matches", proc.stdout)
        self.assertIn("not relaxed", proc.stdout)
        self.assertNotIn("Relaxed by dropping", proc.stdout)

    def test_relax_does_not_drop_touch(self):
        script = ROOT / "scripts" / "surprise_us.py"
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--time-band",
                "5-10",
                "--touch",
                "no",
                "--format",
                "not-a-real-format",
                "--relax",
                "--seed",
                "1",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("touch: false", proc.stdout)
        self.assertNotIn("touch", proc.stdout.split("Relaxed by dropping:", 1)[-1])


if __name__ == "__main__":
    unittest.main()
