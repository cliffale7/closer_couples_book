#!/usr/bin/env python3
"""Privacy checks for the local memoir export. Uses a temporary fictional journal."""

from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import pypdfium2 as pdfium
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_private_memoir as memoir  # noqa: E402

MARKER_A = "FICTIONAL_PRIVATE_A_ONLY"
MARKER_B = "FICTIONAL_PRIVATE_B_ONLY"
MARKER_SHARED = "FICTIONAL_SHARED_KEEP"


def write_session(root: Path, name: str, meta: dict, bodies: dict[str, str], image: bool = False, mementos: list | None = None) -> None:
    folder = root / "sessions" / name
    folder.mkdir(parents=True)
    (folder / "session.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    for filename, text in bodies.items():
        (folder / filename).write_text(text, encoding="utf-8")
    items = []
    if image:
        picture = folder / "toast.png"
        Image.new("RGB", (40, 20), (246, 241, 231)).save(picture)
        items.append({"file": "toast.png", "caption": "UNMARKED_CAPTION_ONLY"})
    for item in mementos or []:
        stored = dict(item)
        if stored.pop("png", False):
            raw = str(stored["file"]).encode("utf-8")
            Image.new("RGB", (32, 18), (raw[0], raw[1], 90)).save(folder / stored["file"])
        items.append(stored)
    if items:
        (folder / "mementos.yaml").write_text(yaml.safe_dump({"items": items}), encoding="utf-8")


def build_fixture(root: Path) -> None:
    common = {
        "schema": "our-story-session/1",
        "content_revision": "book-v1",
        "status": "done",
        "share": {"partner_a": "private", "partner_b": "private", "shared": "shared"},
        "field_visibility": {"date": "shared"},
    }
    write_session(
        root,
        "2020-01-01-001-attempt-1",
        {
            **common,
            "session_id": "s-001-1",
            "activity_id": "001",
            "title": "The Stranger Across From Me",
            "attempt": 1,
            "date": "2020-01-01",
            "version_played": "short",
            "prompts": [{"id": "001.partner_a.1", "text_at_answer": "OLD_PROMPT_WORDING"}],
        },
        {
            "partner-a.md": f"FICTIONAL\n\n{MARKER_A} first",
            "partner-b.md": f"FICTIONAL\n\n{MARKER_B} first",
            "shared.md": f"FICTIONAL\n\n{MARKER_SHARED} first",
        },
        image=True,
    )
    write_session(
        root,
        "2024-05-02-001-attempt-2",
        {
            **common,
            "session_id": "s-001-2",
            "activity_id": "001",
            "title": "The Stranger Across From Me",
            "attempt": 2,
            "date": "2024-05-02",
            "version_played": "standard",
            "prompts": [{"id": "001.partner_a.2", "text_at_answer": "NEW_PROMPT_WORDING"}],
        },
        {
            "partner-a.md": f"FICTIONAL\n\n{MARKER_A} second",
            "partner-b.md": f"FICTIONAL\n\n{MARKER_B} second",
            "shared.md": f"FICTIONAL\n\n{MARKER_SHARED} second",
        },
    )
    write_session(
        root,
        "2021-06-01-S01",
        {
            **common,
            "session_id": "s-S01",
            "activity_id": "S01",
            "title": "The Long Table",
            "attempt": 1,
            "date": "2021-06-01",
            "version_played": "short",
        },
        {
            "partner-a.md": "FICTIONAL\n\nA left the far card down.",
            "partner-b.md": "FICTIONAL\n\nB passed a middle card.",
            "shared.md": "FICTIONAL\n\nThe far card stayed down.",
        },
    )
    write_session(
        root,
        "2022-01-01-blank",
        {
            **common,
            "session_id": "s-blank",
            "activity_id": "032",
            "title": "The Everyday Devotion Experiment",
            "attempt": 1,
            "date": "2022-01-01",
            "status": "paused",
        },
        {"partner-a.md": "FICTIONAL\n\nA wrote one line.", "shared.md": ""},
    )
    write_session(
        root,
        "2023-03-03-mixed",
        {
            **common,
            "session_id": "s-mixed",
            "activity_id": "S03",
            "title": "PRIVATE_TITLE_A",
            "place": "PRIVATE_PLACE_B",
            "date": "2023-03-03",
            "field_visibility": {"date": "shared", "title": "partner_a", "place": "partner_b"},
            "prompts": [
                {"id": "legacy", "text_at_answer": "LEGACY_PROMPT_NO_SEAT"},
                {"id": "S03.partner_b.1", "text_at_answer": "PRIVATE_PROMPT_B"},
                {"id": "S03.shared.1", "text_at_answer": "SHARED_PROMPT_OK"},
            ],
        },
        {"shared.md": "FICTIONAL\n\nMIXED_SHARED_BODY", "partner-a.md": "FICTIONAL\n\nA mixed note", "partner-b.md": "FICTIONAL\n\nB mixed note"},
        mementos=[
            {"file": "a.png", "caption": "CAPTION_A_ONLY", "visibility": "partner_a", "png": True},
            {"file": "b.png", "caption": "CAPTION_B_ONLY", "visibility": "partner_b", "png": True},
            {"file": "s.png", "caption": "CAPTION_SHARED_ONLY", "visibility": "shared", "png": True},
            {"file": "u.png", "caption": "UNKNOWN_VISIBILITY", "visibility": "nope", "png": True},
        ],
    )


def pdf_text(path: Path) -> str:
    document = pdfium.PdfDocument(str(path))
    try:
        pages = []
        for index in range(len(document)):
            page = document[index]
            textpage = page.get_textpage()
            pages.append(textpage.get_text_bounded())
            textpage.close()
            page.close()
        return "\n".join(pages)
    finally:
        document.close()


def pdf_image_count(path: Path) -> int:
    document = pdfium.PdfDocument(str(path))
    try:
        count = 0
        for index in range(len(document)):
            page = document[index]
            try:
                objects = page.get_objects(filter=(pdfium.raw.FPDF_PAGEOBJ_IMAGE,), max_depth=4)
                count += len(list(objects))
            finally:
                page.close()
        return count
    finally:
        document.close()


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read("word/document.xml").decode("utf-8")


def docx_media_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return sum(1 for name in archive.namelist() if name.startswith("word/media/"))


def grant_full_private(root: Path) -> None:
    folder = root / "authorizations"
    folder.mkdir(exist_ok=True)
    for person in ("partner-a", "partner-b"):
        (folder / f"{person}.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema": "our-story-export-authorization/1",
                    "person": person,
                    "scope": "full-private",
                    "granted": True,
                    "date": "2026-10-14",
                }
            ),
            encoding="utf-8",
        )


class MemoirExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.root = Path(self.tmp.name) / "journal"
        self.root.mkdir()
        build_fixture(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def export(self, mode: str, authorize: set[str] | None = None):
        return memoir.export_memoir(self.root, mode, "2026-10-14", authorize or set())

    def test_shared_hides_private_pages(self):
        docx, pdf = self.export("shared")
        for text in (docx_text(docx), pdf_text(pdf)):
            self.assertIn(MARKER_SHARED, text)
            self.assertNotIn(MARKER_A, text)
            self.assertNotIn(MARKER_B, text)
            self.assertIn("S01", text)
            self.assertNotIn("OLD_PROMPT_WORDING", text)
            self.assertNotIn("NEW_PROMPT_WORDING", text)
            self.assertNotIn("UNMARKED_CAPTION_ONLY", text)
            self.assertIn("CAPTION_SHARED_ONLY", text)
            self.assertIn("SHARED_PROMPT_OK", text)
            self.assertIn("MIXED_SHARED_BODY", text)
            for hidden in (
                "CAPTION_A_ONLY",
                "CAPTION_B_ONLY",
                "PRIVATE_TITLE_A",
                "PRIVATE_PLACE_B",
                "LEGACY_PROMPT_NO_SEAT",
                "PRIVATE_PROMPT_B",
                "UNKNOWN_VISIBILITY",
            ):
                self.assertNotIn(hidden, text)
            self.assertLess(text.index("2020-01-01"), text.index("2024-05-02"))
        self.assertEqual(docx_media_count(docx), 1)
        self.assertEqual(pdf_image_count(pdf), 1)
        self.assertIn("PRIVATE_MEMOIR", docx.name)
        self.assertNotIn("UNMARKED", docx.name)

    def test_partner_a_excludes_partner_b_private(self):
        docx, pdf = self.export("partner-a")
        text = docx_text(docx)
        self.assertIn(MARKER_A, text)
        self.assertIn(MARKER_SHARED, text)
        self.assertNotIn(MARKER_B, text)
        self.assertIn("OLD_PROMPT_WORDING", text)
        self.assertNotIn("UNMARKED_CAPTION_ONLY", text)
        self.assertIn("CAPTION_A_ONLY", text)
        self.assertIn("PRIVATE_TITLE_A", text)
        self.assertIn("CAPTION_SHARED_ONLY", text)
        hidden = ("CAPTION_B_ONLY", "PRIVATE_PLACE_B", "PRIVATE_PROMPT_B", "LEGACY_PROMPT_NO_SEAT", "UNKNOWN_VISIBILITY")
        for marker in hidden:
            self.assertNotIn(marker, text)
            self.assertNotIn(marker, pdf_text(pdf))
        self.assertIn("This page was left blank", text)
        self.assertEqual(docx_media_count(docx), 2)
        self.assertEqual(pdf_image_count(pdf), 2)

    def test_full_private_requires_both_authorizations(self):
        with self.assertRaises(SystemExit):
            self.export("full-private", {"partner-a"})
        with self.assertRaises(SystemExit):
            self.export("full-private", {"partner-a", "partner-b"})
        grant_full_private(self.root)
        docx, pdf = self.export("full-private", {"partner-a", "partner-b"})
        text = docx_text(docx)
        pdf_body = pdf_text(pdf)
        for marker in (MARKER_A, MARKER_B, "UNMARKED_CAPTION_ONLY", "CAPTION_A_ONLY", "CAPTION_B_ONLY", "UNKNOWN_VISIBILITY", "LEGACY_PROMPT_NO_SEAT"):
            self.assertIn(marker, text)
            self.assertIn(marker, pdf_body)
        self.assertGreaterEqual(docx_media_count(docx), 5)
        self.assertGreaterEqual(pdf_image_count(pdf), 5)
        with self.assertRaises(SystemExit):
            self.export("full-private", {"partner-a", "partner-b"})

    def test_release_and_escape_are_refused(self):
        with self.assertRaises(SystemExit):
            memoir.export_memoir(ROOT / "release", "shared", "2026-10-14", set())
        outside = Path(self.tmp.name) / "outside.txt"
        outside.write_text("SECRET_OUTSIDE", encoding="utf-8")
        leaked = self.root / "sessions" / "2020-01-01-001-attempt-1" / "mementos.yaml"
        leaked.write_text(
            yaml.safe_dump({"items": [{"file": str(outside), "caption": "no"}]}),
            encoding="utf-8",
        )
        with self.assertRaises(SystemExit):
            self.export("shared")


if __name__ == "__main__":
    unittest.main()
