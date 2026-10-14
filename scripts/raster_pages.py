"""Rasterize the workbook PDF at 7 by 10 inches and review every page.

Writes build/page-raster/page-NNNN.png and review/PAGE_RASTER.md.
Does not read journal/private/.
"""
from __future__ import annotations

from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "The_Closer_Project_Illustrated_Workbook_v1_draft.pdf"
OUT = ROOT / "build" / "page-raster"
REPORT = ROOT / "review" / "PAGE_RASTER.md"

DPI = 144
SCALE = DPI / 72
EXPECTED = (int(7 * DPI), int(10 * DPI))
PARCHMENT = (246, 241, 231)
# CSS margins: 0.62in top, 0.68in sides, 0.72in bottom.
TOP = round(0.62 * DPI)
SIDE = round(0.68 * DPI)
BOTTOM = round(0.72 * DPI)
INK_DISTANCE = 28
# A few antialiased pixels at the content edge are not clipping.
EDGE_SLACK = 4
INK_LIMIT = 80


def ink_mask(image: Image.Image) -> Image.Image:
    paper = Image.new("RGB", image.size, PARCHMENT)
    diff = ImageChops.difference(image, paper)
    red, green, blue = diff.split()
    peak = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    return peak.point(lambda value: 255 if value > INK_DISTANCE else 0)


def ink_count(mask: Image.Image, box: tuple[int, int, int, int]) -> int:
    crop = mask.crop(box)
    return crop.histogram()[255]


def inspect(image: Image.Image, number: int) -> list[str]:
    problems = []
    if image.size != EXPECTED:
        problems.append(f"size {image.size[0]}x{image.size[1]}, expected {EXPECTED[0]}x{EXPECTED[1]}")
    width, height = image.size
    mask = ink_mask(image)
    content = ink_count(mask, (SIDE, TOP, width - SIDE, height - BOTTOM))
    if content < 40:
        problems.append(f"almost blank content area ({content} ink pixels)")
    boxes = [
        (0, TOP, SIDE - EDGE_SLACK, height - BOTTOM),
        (width - (SIDE - EDGE_SLACK), TOP, width, height - BOTTOM),
        (0, 0, int(width * 0.22), TOP),
        (int(width * 0.78), 0, width, TOP),
        (0, height - BOTTOM, int(width * 0.22), height),
        (int(width * 0.78), height - BOTTOM, width, height),
    ]
    margin = sum(ink_count(mask, box) for box in boxes)
    if margin > INK_LIMIT:
        problems.append(f"ink in the margin ({margin} pixels)")
    return problems


def main() -> int:
    if not PDF.is_file():
        raise SystemExit(f"Missing {PDF}")
    OUT.mkdir(parents=True, exist_ok=True)
    document = pdfium.PdfDocument(str(PDF))
    flagged: list[tuple[int, list[str]]] = []
    try:
        total = len(document)
        for index in range(total):
            page = document[index]
            image = page.render(scale=SCALE).to_pil().convert("RGB")
            image.save(OUT / f"page-{index + 1:04d}.png", compress_level=1)
            problems = inspect(image, index + 1)
            if problems:
                flagged.append((index + 1, problems))
            page.close()
            if (index + 1) % 100 == 0 or index + 1 == total:
                print(f"reviewed {index + 1}/{total}  flagged {len(flagged)}", flush=True)
    finally:
        document.close()
    lines = [
        "# Workbook page raster",
        "",
        f"Source: `{PDF.relative_to(ROOT).as_posix()}`",
        f"Pages reviewed: {total}",
        f"Raster: {DPI} dpi, {EXPECTED[0]} by {EXPECTED[1]} pixels (7 by 10 inches).",
        f"Images: `{OUT.relative_to(ROOT).as_posix()}/page-NNNN.png`",
        "",
        "Each page was opened as an image. Ink inside the running head and the page number is expected. Ink in the side margins, or in the header and footer outside the center, is recorded below.",
        "",
    ]
    if not flagged:
        lines.append("No page was flagged.")
    else:
        lines.append(f"Flagged pages: {len(flagged)}")
        lines.append("")
        for number, problems in flagged:
            lines.append(f"- Page {number}: {'; '.join(problems)}")
    lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"WROTE {REPORT.relative_to(ROOT)}  flagged {len(flagged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
