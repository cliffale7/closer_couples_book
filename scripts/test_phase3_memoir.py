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


def write_session(root: Path, name: str, meta: dict, bodies: dict[str, str], image: bool = False) -> None:
    folder = root / "sessions" / name
    folder.mkdir(parents=True)
    (folder / "session.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    for filename, text in bodies.items():
        (folder / filename).write_text(text, encoding="utf-8")
    if image:
        picture = folder / "toast.png"
        Image.new("RGB", (40, 20), (246, 241, 231)).save(picture)
        (folder / "mementos.yaml").write_text(
            yaml.safe_dump({"items": [{"file": "toast.png", "caption": "FICTIONAL toast"}]}),
            encoding="utf-8",
        )


def build_fixture(root: Path) -> None:
    common = {
        "schema": "our-story-session/1",
        "content_revision": "book-v1",
        "status": "done",
        "share": {"partner_a": "private", "partner_b": "private", "shared": "shared"},
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


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read("word/document.xml").decode("utf-8")


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
            self.assertIn("OLD_PROMPT_WORDING", text)
            self.assertIn("NEW_PROMPT_WORDING", text)
            self.assertLess(text.index("2020-01-01"), text.index("2024-05-02"))

    def test_partner_a_excludes_partner_b_private(self):
        docx, _pdf = self.export("partner-a")
        text = docx_text(docx)
        self.assertIn(MARKER_A, text)
        self.assertIn(MARKER_SHARED, text)
        self.assertNotIn(MARKER_B, text)
        self.assertIn("This page was left blank", text)

    def test_full_private_requires_both_authorizations(self):
        with self.assertRaises(SystemExit):
            self.export("full-private", {"partner-a"})
        docx, _pdf = self.export("full-private", {"partner-a", "partner-b"})
        text = docx_text(docx)
        self.assertIn(MARKER_A, text)
        self.assertIn(MARKER_B, text)

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
