"""Printable card and worksheet packet.

Reads chapter and signature card fences, plus the blank journal templates the
book names. Does not read journal/private/. Does not copy a solution key.
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_all  # noqa: E402

OUT = ROOT / "build" / "print"
HTML_PATH = OUT / "cards.html"
DOCX_PATH = OUT / "Printable_Cards_and_Worksheets_v1_draft.docx"
PDF_PATH = OUT / "Printable_Cards_and_Worksheets_v1_draft.pdf"
SOURCE_PATH = ROOT / "print" / "CARDS_AND_WORKSHEETS.md"

TEMPLATES = [
    "session-log.md",
    "yes-no-maybe.md",
    "hundred-points.md",
    "letter-page.md",
    "postcard.md",
    "museum-label.md",
    "civilization-charter.md",
    "escape-clue-sheet.md",
    "memento-caption.md",
]

CSS = """
@page { size: letter; margin: 0.55in 0.5in 0.6in 0.5in;
  @bottom-center { content: counter(page); font-family: Calibri, sans-serif; font-size: 9pt; color: #7C3A46; } }
@page :first { @bottom-center { content: none; } }
* { box-sizing: border-box; }
html, body { margin: 0; background: #F6F1E7; color: #241F1C;
  font-family: Georgia, "Times New Roman", serif; font-size: 11pt; line-height: 1.35;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
h1, h2, h3 { font-family: "Palatino Linotype", Palatino, "Book Antiqua", serif; font-weight: normal; color: #1B2433; }
h1 { font-size: 22pt; margin: 0 0 0.2in; }
h2 { font-size: 16pt; break-before: page; margin: 0 0 0.12in; }
h2.keep { break-before: auto; }
h3 { font-size: 13pt; margin: 0.2in 0 0.08in; }
p, li { margin: 0.06in 0; }
.kicker { font-family: Calibri, sans-serif; letter-spacing: 0.12em; text-transform: uppercase; color: #A85A32; font-size: 9pt; }
.note { font-family: Calibri, sans-serif; font-size: 10pt; }
.deck { display: grid; grid-template-columns: 1fr 1fr; gap: 0.16in; margin-top: 0.12in; }
.card { border: 0.75pt dashed #7C3A46; min-height: 2.15in; padding: 0.14in 0.16in 0.16in;
  break-inside: avoid; background: #FBF8F2; }
.card .label { font-family: Calibri, sans-serif; font-size: 8pt; letter-spacing: 0.08em; text-transform: uppercase; color: #3E6464; }
.card h3 { margin: 0.04in 0 0.06in; font-size: 12pt; }
.sheet { break-before: page; }
.sheet h1 { font-size: 18pt; }
.rule { border-bottom: 0.6pt solid #D9CFC0; height: 0.32in; }
table { width: 100%; border-collapse: collapse; margin: 0.12in 0; }
th, td { border: 0.6pt solid #2C3544; padding: 0.08in; text-align: left; vertical-align: top; }
th { font-family: Calibri, sans-serif; font-size: 9pt; letter-spacing: 0.06em; text-transform: uppercase; }
.seal { border: 1.5pt solid #1B2433; padding: 0.2in; background: #FBF8F2; }
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def fences(body: str, lang: str) -> list[str]:
    found = []
    parts = body.split("```")
    for index in range(1, len(parts), 2):
        block = parts[index]
        first, _, rest = block.partition("\n")
        if first.strip() == lang:
            found.append(rest.strip("\n"))
    return found


def strip_fences(text: str) -> str:
    parts = text.split("```")
    kept = [parts[0]]
    for index in range(1, len(parts)):
        if index % 2 == 0:
            kept.append(parts[index])
    return "".join(kept).strip()


def load_sources() -> list[tuple[str, str, str, list[tuple[str, str]]]]:
    decks = []
    for path in build_all.collect_paths(False):
        rel = build_all.rel_posix(path)
        if not rel.startswith("chapters/") and not rel.startswith("signature/"):
            continue
        text = path.read_text(encoding="utf-8-sig")
        meta, body = build_all.split_frontmatter(text, rel)
        blocks = fences(body, "cards")
        if not blocks:
            continue
        cards = []
        for block in blocks:
            cards.extend(build_all.parse_cards(block))
        ident = str(meta.get("id") or path.stem[:3])
        title = str(meta.get("title") or path.stem)
        decks.append((ident, title, rel, cards))
    return decks


def reference_103() -> str:
    path = ROOT / "chapters" / "part-13" / "103-the-relationship-escape-room.md"
    text = path.read_text(encoding="utf-8")
    if "Hours are only 6, 8, and 10" not in text:
        raise SystemExit("103 no longer states the shared hours. No packet was written.")
    return """
<section class="sheet">
<p class="kicker">103 · print and leave face up</p>
<h1>Shared reference card</h1>
<div class="seal">
<p><strong>Hours are only 6, 8, and 10.</strong> Evenings are Cedar, Harbor, and Lantern. Foods are oranges, soup, and bread. First moves are a question, a toast, and a walk. Each item is used once.</p>
<p>Both players read this aloud before either packet is opened. It is not sealed inside an envelope. The packets do not restate this sentence.</p>
</div>
<h3>Blank grid</h3>
<table>
<thead><tr><th>Evening</th><th>Hour</th><th>Food</th><th>First move</th><th>Clue numbers we cited</th></tr></thead>
<tbody>
<tr><td>Cedar</td><td></td><td></td><td></td><td></td></tr>
<tr><td>Harbor</td><td></td><td></td><td></td><td></td></tr>
<tr><td>Lantern</td><td></td><td></td><td></td><td></td></tr>
</tbody>
</table>
</section>
<section class="sheet">
<p class="kicker">103 · seal · North only</p>
<h1>Packet North</h1>
<div class="seal">
<p>Give this only to North, after the shared reference card is face up. Do not hand it across during play.</p>
<ul>
<li>N1. The toast happens at 8.</li>
<li>N2. Cedar begins two hours before the soup.</li>
<li>N3. Harbor is not the walk.</li>
<li>N4. Bread is not served at the earliest hour.</li>
</ul>
</div>
</section>
<section class="sheet">
<p class="kicker">103 · seal · South only</p>
<h1>Packet South</h1>
<div class="seal">
<p>Give this only to South, after the shared reference card is face up. Do not hand it across during play.</p>
<ul>
<li>S1. Lantern is the walk.</li>
<li>S2. Bread is served at 10.</li>
<li>S3. The question is asked two hours before Harbor.</li>
<li>S4. Soup is not served at 10.</li>
</ul>
</div>
</section>
<section class="sheet">
<p class="kicker">103 · blank slips</p>
<h1>Place slip and reason slip</h1>
<p>One place slip stays in your own envelope. One reason slip goes into your partner's envelope, back folded shut.</p>
<div class="deck">
<article class="card"><p class="label">Place slip</p><h3>A shared place</h3><p>A short phrase. Do not show it.</p><div class="rule"></div><div class="rule"></div></article>
<article class="card"><p class="label">Reason slip · front</p><h3>A food, song, or object</h3><div class="rule"></div><div class="rule"></div></article>
<article class="card"><p class="label">Reason slip · back</p><h3>Why, in a sentence or two</h3><p>Fold this side shut.</p><div class="rule"></div><div class="rule"></div></article>
</div>
</section>
"""


def weather_log() -> str:
    rows = "".join(
        "<tr><td></td><td></td><td></td><td></td><td></td></tr>" for _ in range(8)
    )
    return f"""
<section class="sheet">
<p class="kicker">100 · optional log</p>
<h1>Emotional weather log</h1>
<p>Columns from activity 100. A blank asking cell is a finished report. Missing days are none of the log's business. This is a memory, not a compliance chart.</p>
<table>
<thead><tr><th>Date</th><th>Region</th><th>Forecast</th><th>Help I will arrange</th><th>Anything I am explicitly asking</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</section>
"""


def markdown_sheet(name: str, text: str) -> str:
    body = strip_fences(text)
    parts = ['<section class="sheet">', f'<p class="kicker">Worksheet · {esc(name)}</p>']
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            parts.append("<p>" + "<br>".join(esc(line) for line in paragraph) + "</p>")
            paragraph.clear()

    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        if line.startswith("# "):
            flush()
            parts.append(f"<h1>{esc(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            flush()
            parts.append(f"<h3>{esc(line[3:].strip())}</h3>")
        elif line.startswith("**") and line.endswith("**") and len(line) > 4:
            flush()
            parts.append(f"<h3>{esc(line.strip('* '))}</h3>")
        elif line.startswith("> "):
            paragraph.append(line[2:])
        elif line.startswith("- "):
            flush()
            parts.append(f"<p>{esc(line)}</p>")
        else:
            paragraph.append(line)
    flush()
    parts.append("</section>")
    return "\n".join(parts)


def html_document(decks: list[tuple[str, str, str, list[tuple[str, str]]]]) -> str:
    parts = [
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">",
        "<title>Printable Cards and Worksheets</title>",
        f"<style>{CSS}</style></head><body>",
        "<p class=\"kicker\">The Closer Project · draft packet</p>",
        "<h1 class=\"keep\">Cards and worksheets</h1>",
        "<p>Cut on the dashed line. Each card is 3.5 inches wide. A long card grows downward; leave the white gap before the next cut. These sheets are blank of your life. A card result is not consent to touch or sex.</p>",
        "<p class=\"note\">Activity 103 prints the shared hours before either packet. The covered answer section in the chapter is not reprinted here. Signature S03's solved sample is not in this packet. Print Partner A's and Partner B's private sheets on separate paper.</p>",
    ]
    for ident, title, _rel, cards in decks:
        parts.append(f"<h2>{esc(ident)} · {esc(title)}</h2>")
        parts.append(f"<p class=\"note\">{len(cards)} cards. Cut on the dashed border.</p>")
        parts.append('<div class="deck">')
        for label, body in cards:
            parts.append('<article class="card">')
            parts.append(f'<p class="label">{esc(ident)}</p>')
            if label:
                parts.append(f"<h3>{esc(label)}</h3>")
            if body:
                parts.append(f"<p>{esc(body)}</p>")
            parts.append("</article>")
        parts.append("</div>")
    parts.append(reference_103())
    parts.append(weather_log())
    for name in TEMPLATES:
        path = ROOT / "journal" / "templates" / name
        parts.append(markdown_sheet(name, read_public(path)))
    parts.append("</body></html>")
    page = "\n".join(parts)
    banned = ["journal/private", "The Tuesday is 10 March", "The remaining hour, 10, is the walk", "scavenger"]
    for token in banned:
        if token in page:
            raise SystemExit(f"Packet contained {token!r}. No files were written.")
    if "Hours are only 6, 8, and 10" not in page:
        raise SystemExit("Shared hours card missing. No files were written.")
    return page


def write_docx(decks: list[tuple[str, str, str, list[tuple[str, str]]]]) -> None:
    document = Document()
    section = document.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)
    normal = document.styles["Normal"]
    normal.font.name = "Georgia"
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0x24, 0x1F, 0x1C)
    document.add_heading("Cards and worksheets", 0)
    intro = document.add_paragraph(
        "Editable card text for the draft packet. Cut guides live in the PDF. A card result is not consent to touch or sex."
    )
    intro.runs[0].font.name = "Calibri"
    intro.runs[0].font.size = Pt(10)
    for ident, title, _rel, cards in decks:
        document.add_heading(f"{ident} · {title}", 1)
        for label, body in cards:
            paragraph = document.add_paragraph()
            if label:
                run = paragraph.add_run(label)
                run.bold = True
                run.font.name = "Calibri"
                paragraph.add_run(" — ")
            if body:
                paragraph.add_run(body)
    document.add_heading("103 · Shared reference card", 1)
    document.add_paragraph("Hours are only 6, 8, and 10. Evenings are Cedar, Harbor, and Lantern. Foods are oranges, soup, and bread. First moves are a question, a toast, and a walk. Each item is used once.")
    document.add_paragraph("Print this before either packet. The covered answer section in the chapter is not reprinted here.")
    for name, lines in (
        ("Packet North", ["N1. The toast happens at 8.", "N2. Cedar begins two hours before the soup.", "N3. Harbor is not the walk.", "N4. Bread is not served at the earliest hour."]),
        ("Packet South", ["S1. Lantern is the walk.", "S2. Bread is served at 10.", "S3. The question is asked two hours before Harbor.", "S4. Soup is not served at 10."]),
    ):
        document.add_heading(name, 2)
        for line in lines:
            document.add_paragraph(line, style="List Bullet")
    document.add_heading("100 · Emotional weather log", 1)
    document.add_paragraph("Date, region, forecast, help I will arrange for myself, and anything I am explicitly asking. A blank asking cell is a finished report.")
    for name in TEMPLATES:
        text = strip_fences(read_public(ROOT / "journal" / "templates" / name))
        first = True
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith(">"):
                if line.startswith(">"):
                    document.add_paragraph(line[1:].strip())
                continue
            if line.startswith("#"):
                document.add_heading(line.lstrip("#").strip(), 1 if first else 2)
                first = False
            else:
                document.add_paragraph(line.strip("*"))
    document.save(DOCX_PATH)


def write_source(decks: list[tuple[str, str, str, list[tuple[str, str]]]]) -> None:
    lines = [
        "# Cards and worksheets",
        "",
        "Editable source for the printable packet. Card text is copied from the chapter fences. The facilitator key for 103 and the solved sample for S03 are not included.",
        "",
        "A card result is not consent to touch or sex.",
        "",
    ]
    for ident, title, rel, cards in decks:
        lines.append(f"## {ident} · {title}")
        lines.append("")
        lines.append(f"Source: `{rel}`")
        lines.append("")
        for label, body in cards:
            if label:
                lines.append(f"- **{label}.** {body}")
            else:
                lines.append(f"- {body}")
        lines.append("")
    lines.extend([
        "## 103 · Shared reference card",
        "",
        "Hours are only 6, 8, and 10. Evenings are Cedar, Harbor, and Lantern. Foods are oranges, soup, and bread. First moves are a question, a toast, and a walk. Each item is used once.",
        "",
        "Print this face up before Packet North or Packet South is opened.",
        "",
        "## 100 · Emotional weather log",
        "",
        "Date, region, forecast, help I will arrange for myself, and anything I am explicitly asking. A blank asking cell is a finished report.",
        "",
    ])
    SOURCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SOURCE_PATH.write_text("\n".join(lines), encoding="utf-8")


def read_public(path: Path) -> str:
    rel = path.resolve().relative_to(ROOT).as_posix()
    if rel.startswith("journal/private"):
        raise SystemExit(f"Refusing to read {rel}. No files were written.")
    return path.read_text(encoding="utf-8")


def main() -> int:
    decks = load_sources()
    if not any(ident == "104" and len(cards) == 12 for ident, _t, _r, cards in decks):
        raise SystemExit("104 must contribute 12 event cards. No files were written.")
    if not any(ident == "S01" and len(cards) == 12 for ident, _t, _r, cards in decks):
        raise SystemExit("S01 must contribute 12 questions. No files were written.")
    page = html_document(decks)
    OUT.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(page, encoding="utf-8")
    write_docx(decks)
    write_source(decks)
    if "--no-pdf" in sys.argv:
        print(f"WROTE  {HTML_PATH.relative_to(ROOT)}  {HTML_PATH.stat().st_size} bytes")
        print(f"WROTE  {DOCX_PATH.relative_to(ROOT)}  {DOCX_PATH.stat().st_size} bytes")
        print(f"WROTE  {SOURCE_PATH.relative_to(ROOT)}  {SOURCE_PATH.stat().st_size} bytes")
        return 0
    build_all.print_pdf(HTML_PATH, PDF_PATH, OUT / "pdf-print-error.txt", kept="HTML and DOCX were kept.")
    print(f"WROTE  {HTML_PATH.relative_to(ROOT)}  {HTML_PATH.stat().st_size} bytes")
    print(f"WROTE  {DOCX_PATH.relative_to(ROOT)}  {DOCX_PATH.stat().st_size} bytes")
    print(f"WROTE  {SOURCE_PATH.relative_to(ROOT)}  {SOURCE_PATH.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
