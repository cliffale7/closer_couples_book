#!/usr/bin/env python3
"""Print owner contact sheets from the current SVG drawings.

Writes build/art-review/art-review.html and build/art-review/OWNER_ART_REVIEW.pdf.
Does not mark any drawing approved.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_all  # noqa: E402

OUT = ROOT / "build" / "art-review"
HTML_PATH = OUT / "art-review.html"
PDF_PATH = OUT / "OWNER_ART_REVIEW.pdf"

CORRECTED = {
    "assets/chapters/005/motif.svg",
    "assets/chapters/013/motif.svg",
    "assets/chapters/021/motif.svg",
    "assets/chapters/024/motif.svg",
    "assets/chapters/061/motif.svg",
    "assets/chapters/065/motif.svg",
    "assets/chapters/066/motif.svg",
    "assets/chapters/099/motif.svg",
    "assets/chapters/106/motif.svg",
    "assets/parts/05-opener.svg",
    "assets/parts/06-opener.svg",
    "assets/signatures/S01-hero.svg",
    "assets/signatures/S03-hero.svg",
}

CSS = """
@page { size: letter; margin: 0.5in; }
body { font-family: Calibri, sans-serif; color: #241F1C; background: #FBF8F2; }
h1, h2 { font-family: "Palatino Linotype", Palatino, serif; }
h1 { font-size: 22pt; }
h2 { break-before: page; font-size: 16pt; }
.note { font-size: 11pt; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px 12px; }
.wide { grid-template-columns: repeat(2, 1fr); }
figure { margin: 0; break-inside: avoid; }
img { width: 100%; height: auto; background: #F6F1E7; border: 1px solid #D9CFC0; }
figcaption { font-size: 8pt; line-height: 1.25; margin-top: 3px; }
.changed { color: #7C3A46; font-weight: 700; }
"""


def aria_label(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r'aria-label="([^"]+)"', text)
    return match.group(1) if match else path.name


def figure(rel: str) -> str:
    path = ROOT / rel
    label = aria_label(path)
    mark = " <span class='changed'>Corrected. Awaiting owner.</span>" if rel in CORRECTED else ""
    src = Path("..") / ".." / rel
    return (
        "<figure>"
        f"<img src='{html.escape(src.as_posix())}' alt='{html.escape(label)}'/>"
        f"<figcaption>{html.escape(rel)}{mark}<br/>{html.escape(label)}</figcaption>"
        "</figure>"
    )


def chunk(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def main() -> int:
    covers = [
        "assets/covers/cover-front.svg",
        "assets/covers/cover-back.svg",
        "assets/covers/title-page.svg",
    ]
    parts = [f"assets/parts/{number:02d}-opener.svg" for number in range(1, 14)]
    heroes = [f"assets/signatures/S0{number}-hero.svg" for number in range(1, 7)]
    motifs = [f"assets/chapters/{number:03d}/motif.svg" for number in range(1, 109)]
    for rel in covers + parts + heroes + motifs:
        if not (ROOT / rel).is_file():
            raise SystemExit(f"Missing drawing {rel}")
    parts_html = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        "<title>Owner art review</title>",
        f"<style>{CSS}</style></head><body>",
        "<h1>Owner art review</h1>",
        "<p class='note'>These sheets show the drawings in the current source. "
        "Thirteen were redrawn after the art audit. Looking at this file is not approval. "
        "Owner approval remains open.</p>",
        "<ul>",
    ]
    for rel in sorted(CORRECTED):
        parts_html.append(f"<li>{html.escape(rel)} — {html.escape(aria_label(ROOT / rel))}</li>")
    parts_html.append("</ul>")
    sections = [
        ("Covers", covers, "wide", 2),
        ("Part openers", parts, "wide", 4),
        ("Signature heroes", heroes, "wide", 2),
    ]
    for title, items, kind, size in sections:
        for index, group in enumerate(chunk(items, size), start=1):
            parts_html.append(f"<h2>{html.escape(title)} {index}</h2>")
            parts_html.append(f"<div class='grid {kind}'>")
            parts_html.extend(figure(rel) for rel in group)
            parts_html.append("</div>")
    for index, group in enumerate(chunk(motifs, 9), start=1):
        first = group[0].split("/")[2]
        last = group[-1].split("/")[2]
        parts_html.append(f"<h2>Chapter motifs {first}–{last}</h2>")
        parts_html.append("<div class='grid'>")
        parts_html.extend(figure(rel) for rel in group)
        parts_html.append("</div>")
    parts_html.append("</body></html>")
    OUT.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text("\n".join(parts_html), encoding="utf-8")
    build_all.print_pdf(HTML_PATH, PDF_PATH, error_path=OUT / "pdf-error.txt", timeout=300)
    print(f"WROTE  {PDF_PATH.relative_to(ROOT).as_posix()}  {PDF_PATH.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
