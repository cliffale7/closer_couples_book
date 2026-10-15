#!/usr/bin/env python3
"""Print and edit a blank Our Story packet that can be copied without limit."""

from __future__ import annotations

import html
import sys
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_all  # noqa: E402

HTML_PATH = ROOT / "build" / "journal" / "Our_Story_Repeatable_Session_Pack_v1.html"
DOCX_PATH = ROOT / "build" / "journal" / "Our_Story_Repeatable_Session_Pack_v1.docx"
PDF_PATH = ROOT / "build" / "journal" / "Our_Story_Repeatable_Session_Pack_v1.pdf"

PAGES = [
    (
        "How to file a repeat",
        "Copy this packet whenever you do an activity again, including years later. Write the ID (001–108 or S01–S06), the title, the date, and the attempt number on every sheet. Attempt 1 is the first sitting. Keep the old sheets. File by date, and keep a second stack by ID if you want to find one activity's whole history. A blank page is a real record.",
        [],
    ),
    (
        "Session cover",
        "Activity ID ________    Title ________________________________\nAttempt ________    Date ____________    Time ____________\nPlace ________________________________\nVersion played ________ (short, standard, extended, or your label)\nStatus: done ________    paused ________    passed ________\nPartner A initials ________    Partner B initials ________",
        ["What we came in wanting, if anything"],
    ),
    (
        "Partner A — my experience",
        "Private unless I mark it shared. Paste the Partner A prompt from the activity, or write the question you actually used.",
        ["The prompt I used", "What I want to keep"],
    ),
    (
        "Partner B — my experience",
        "Same paper and the same number of lines as Partner A. Paste a different prompt. This page is mine.",
        ["The prompt I used", "What I want to keep"],
    ),
    (
        "Shared page",
        "Either person may write. Neither rewrites the other's sentences.",
        ["What actually happened", "The line worth keeping", "What we might do next, if anything"],
    ),
    (
        "Then and now",
        "Earlier attempt ________ on ________. This attempt ________ on ________.",
        ["Then", "Now", "What I do not want overwritten"],
    ),
    (
        "Chronology",
        "One sitting, one pair of lines. Leave the second line blank if you would rather not summarize. Omit a private page unless the writer marks it indexable.",
        ["Date, ID, attempt, place", "Optional line we are willing to index"],
    ),
    (
        "Milestone",
        "A move, a repair, a joke that stayed, a hard week. Not a score. ID may be an activity, S01–S06, or the word milestone.",
        ["What happened", "Where the keepsake lives, if there is one"],
    ),
    (
        "Keepsake caption",
        "Date ________    ID ________    Who may see this ________\nThe file or the object stays in the house. This sheet does not publish it.",
        ["What this is", "Where it lives"],
    ),
    (
        "Annual reflection — Partner A",
        "ID: annual. Title: Chapters of us. Year ________",
        ["What this year contained for me, in scenes", "What I want more of next year"],
    ),
    (
        "Annual reflection — Partner B",
        "Equal space. A different page from Partner A.",
        ["What this year contained for me", "What I want protected next year"],
    ),
    (
        "Annual reflection — shared",
        "A few scenes, a difficulty you are willing to name, a delight, and what you are taking forward. No ranking of who grew more.",
        ["The year as a chapter"],
    ),
    (
        "Continuation",
        "Our Story · ID ________ · Date ________ · Attempt ________ · Whose page ________",
        ["Continued"],
    ),
    (
        "Signature revisit",
        "For S01–S06. Name the signature, the version, and whether a card, branch, key, or toast was skipped.",
        ["What we played", "What stayed covered or unopened", "What we want the next attempt to remember"],
    ),
]


def rules(count: int = 8) -> str:
    spans = "".join("<span></span>" for _ in range(count))
    return f'<div class="writing-lines">{spans}</div>'


def html_page() -> str:
    sections = []
    for title, intro, prompts in PAGES:
        bits = [f"<article><h1>{html.escape(title)}</h1>", f"<p>{html.escape(intro).replace(chr(10), '<br/>')}</p>"]
        for prompt in prompts:
            bits.append(f"<h2>{html.escape(prompt)}</h2>")
            bits.append(rules(8))
        if not prompts:
            bits.append(rules(8))
        bits.append("</article>")
        sections.append("\n".join(bits))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Our Story repeatable session pack</title>
<style>
@page {{ size: letter; margin: 0.85in 0.7in 0.75in 0.7in; }}
body {{ font-family: Georgia, serif; color: #241F1C; background: #FBF8F2; }}
h1 {{ font-family: "Palatino Linotype", Palatino, serif; font-size: 22pt; }}
h2 {{ font-family: Calibri, sans-serif; font-size: 13pt; color: #3E6464; break-after: avoid; }}
article {{ break-after: page; }}
.writing-lines span {{ display: block; height: 0.38in; border-bottom: 1px solid #D9CFC0; }}
</style></head><body>
{''.join(sections)}
</body></html>
"""


def write_docx(path: Path) -> None:
    document = Document()
    for title, intro, prompts in PAGES:
        document.add_heading(title, 0)
        for line in intro.split("\n"):
            document.add_paragraph(line)
        for prompt in prompts or ["Notes"]:
            document.add_heading(prompt, 2)
            for _ in range(8):
                paragraph = document.add_paragraph("________________________________________________________________")
                for run in paragraph.runs:
                    run.font.name = "Georgia"
                    run.font.size = Pt(12)
                    run.font.color.rgb = RGBColor(0xD9, 0xCF, 0xC0)
        document.add_page_break()
    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.7)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.75)
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(path)


def main() -> int:
    build_all.configure_stdio()
    if build_all.is_private_path(HTML_PATH):
        raise SystemExit("Refusing to write the repeat pack into journal/private.")
    page = html_page()
    build_all.write_bytes(HTML_PATH, page.encode("utf-8"))
    write_docx(DOCX_PATH)
    build_all.print_pdf(HTML_PATH, PDF_PATH, error_path=HTML_PATH.with_suffix(".pdf-error.txt"), timeout=180)
    print(f"html: {HTML_PATH}")
    print(f"docx: {DOCX_PATH}")
    print(f"pdf: {PDF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
