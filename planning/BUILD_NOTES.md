# Build notes

Measured 14 October 2026 from the project root. Pandoc and Typst are not used. Type is Palatino Linotype, Georgia, and Calibri. No font files are bundled.

`journal/private/` is not read. Source DOCX files under `source/` were checksum-checked and not modified.

## Commands

```bash
python scripts/build_all.py
python scripts/validate.py
python scripts/build_journal.py
python scripts/surprise_us.py --help
python scripts/surprise_us.py
```

`python scripts/surprise_us.py` with no filters prints one chapter. Filters (`--time-band`, `--energy`, `--emotional-intensity`, `--format`, `--mood`) are applied before that choice. If nothing matches, the script says so and keeps the filters unless `--relax` is passed. The paper method is `frontmatter/06-surprise-us.md`.

## Workbook

`python scripts/build_all.py` completed. PDF print used Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe` with `--headless=new`. No format failed. `build/pdf-print-error.txt` was not left on disk. `python scripts/validate.py` then passed, including the private-path guard and the source DOCX checksums.

| Path | Bytes | Result |
| --- | ---: | --- |
| `build/workbook.html` | 1958649 | written |
| `build/The_Closer_Project_Illustrated_Workbook_v1_draft.docx` | 861704 | written; opens |
| `build/The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` | 8670432 | written; 1140 pages; MediaBox 504 by 720 pt (7 by 10 in) |
| `build/The_Closer_Project_Reader_v1_draft.epub` | 850683 | written; mimetype stored first; XML parses |

The run included 6 front-matter files, 108 chapters, 6 signature sessions (`signature/S01` through `signature/S06`), and `research/BIBLIOGRAPHY.md`. Signature anchors are `signature-s01` style. Those files were checked for the chapter heading order and a motif path. An empty `signature/` folder still allows the book build.

Part openers use `assets/parts/01-opener.svg` through `assets/parts/13-opener.svg`. All 13 are referenced in the HTML. The print PDF and the EPUB carry those SVGs. The DOCX records each SVG path in a short note, because this toolchain does not embed SVG. A missing opener is skipped.

Indexes are generated at build time from chapter frontmatter and placed after the chapters and signature sessions, before the bibliography and the build note: alphabetical title, time band, emotional intensity, energy, format, mood, and repeatable chapters (revisit). Links use the existing `chapter-001` anchors.

`research/BIBLIOGRAPHY.md` is included as endmatter. B1992, S2007, and G1999 were added from the citation lines already in `research/CITATION_WHITELIST.md`.

DOCX zip entry dates are 14 October 2026. EPUB `dcterms:modified` is `2026-10-14T00:00:00Z`. The PDF is reprinted by Chrome on each run, so its bytes are not stable.

## Our Story companion

`python scripts/build_journal.py` completed. PDF print used the same Chrome headless path. No format failed. `build/journal/pdf-print-error.txt` was not left on disk.

| Path | Bytes | Result |
| --- | ---: | --- |
| `build/journal/our-story.html` | 254543 | written |
| `build/journal/Our_Story_Companion.docx` | 108395 | written |
| `build/journal/Our_Story_Companion.pdf` | 1243688 | written; 274 pages; MediaBox 612 by 792 pt (US Letter) |

Sources are `journal/COMPANION_STRUCTURE.md`, `journal/PROMPT_BANK.md`, and `journal/templates/*.md`, plus catalog titles for the cross-reference. Prompts are followed by eight handwriting rules. Personal answers are not filled in. The companion DOCX zip dates are 14 October 2026.

## Rebuild after copyedit

A later `python scripts/build_all.py` on 14 October 2026 included the copyedit in `review/copyedit/openings.md` and `review/copyedit/sensual-consent.md`, the part introductions, the front and back covers, eight handwriting rules on journal prompts, and PNG drawings inside the DOCX. `python scripts/validate.py` passed. The PDF is 1,452 pages, MediaBox 504 by 720 pt. Bytes: HTML 2,049,900; DOCX 1,925,421; EPUB 859,772; PDF 9,110,973.

Chapter 103's facilitator key and the following "Three ways to play" heading each start a new page. The solved grid does not share a sheet with the play text.

DOCX drawings are PNG screenshots of the SVG art, cached under `build/raster/` and embedded with `python-docx`. HTML, EPUB, and PDF still use the SVG files. No font files are bundled.

The Our Story companion rebuilt the same day no longer prints builder architecture, prompt-bank fences, or a `journal/private/` path. Bytes after that rebuild: HTML 219,587; DOCX 95,928; PDF 1,057,551.

`python scripts/build_cards.py` writes the printable packet from the card fences, the 103 shared hours card and sealed packets, a 100 weather log, and the blank templates named in the book. It does not reprint the 103 answer section or the solved S03 sample.

This is still a validated draft. A full print-size raster of every page has not been done. `release/` should be read against `EXPORT_MANIFEST.md` for the remaining limits.

## Rebuild after citation corrections

A later `python scripts/build_all.py` on 14 October 2026 picked up citation corrections in chapter 001 and signatures S01, S03, and S04. `python scripts/validate.py` passed. The PDF is 1,141 pages. Bytes: HTML 1,959,201; DOCX 861,929; EPUB 850,727; PDF 8,673,026. The Our Story companion from the earlier run was left in place. Developmental editing, copyediting, and independent QA were not part of this rebuild.
