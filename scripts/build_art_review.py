#!/usr/bin/env python3
"""Print owner contact sheets from the accepted paintings.

Writes build/art-review/art-review.html and build/art-review/OWNER_ART_REVIEW.pdf.
Looking at the file is not approval.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_all  # noqa: E402

OUT = ROOT / "build" / "art-review"
HTML_PATH = OUT / "art-review.html"
PDF_PATH = OUT / "OWNER_ART_REVIEW.pdf"

INVENTORY = ROOT / "planning" / "phase4" / "ART_INVENTORY.json"

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


def figure(slot: dict) -> str:
    rel = slot["live_path"]
    label = f"{slot['id']}  {slot['title']}"
    src = Path("..") / ".." / rel
    return (
        "<figure>"
        f"<img src='{html.escape(src.as_posix())}' alt='{html.escape(label)}'/>"
        f"<figcaption>{html.escape(label)}</figcaption>"
        "</figure>"
    )


def chunk(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def main() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    slots = inventory["slots"]
    if len(slots) != 130 or any(slot.get("status") != "approved" for slot in slots):
        raise SystemExit("Art review requires 130 approved paintings.")
    for slot in slots:
        if not (ROOT / slot["live_path"]).is_file():
            raise SystemExit(f"Missing painting {slot['live_path']}")
    grouped = {
        "cover": [slot for slot in slots if slot["kind"] == "cover"],
        "part": [slot for slot in slots if slot["kind"] == "part"],
        "signature": [slot for slot in slots if slot["kind"] == "signature"],
        "chapter": [slot for slot in slots if slot["kind"] == "chapter"],
    }
    parts_html = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        "<title>Owner art review</title>",
        f"<style>{CSS}</style></head><body>",
        "<h1>Owner art review</h1>",
        "<p class='note'>These sheets show the 130 accepted paintings. "
        "Looking at this file is not approval. Owner approval remains open.</p>",
    ]
    sections = [
        ("Covers and title", grouped["cover"], "wide", 2),
        ("Part openers", grouped["part"], "wide", 4),
        ("Signature heroes", grouped["signature"], "wide", 2),
    ]
    for title, items, kind, size in sections:
        for index, group in enumerate(chunk(items, size), start=1):
            parts_html.append(f"<h2>{html.escape(title)} {index}</h2>")
            parts_html.append(f"<div class='grid {kind}'>")
            parts_html.extend(figure(slot) for slot in group)
            parts_html.append("</div>")
    for index, group in enumerate(chunk(grouped["chapter"], 9), start=1):
        first = group[0]["id"]
        last = group[-1]["id"]
        parts_html.append(f"<h2>Chapters {html.escape(first)}–{html.escape(last)}</h2>")
        parts_html.append("<div class='grid'>")
        parts_html.extend(figure(slot) for slot in group)
        parts_html.append("</div>")
    parts_html.append("</body></html>")
    OUT.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text("\n".join(parts_html), encoding="utf-8")
    build_all.print_pdf(HTML_PATH, PDF_PATH, error_path=OUT / "pdf-error.txt", timeout=300)
    print(f"WROTE  {PDF_PATH.relative_to(ROOT).as_posix()}  {PDF_PATH.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
