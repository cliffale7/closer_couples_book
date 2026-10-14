# Final QA report

**Date:** 14 October 2026  
**Edition under test:** files in `build/` after the workbook rebuild  
**Verdict:** not a release. `python scripts/validate.py` passing does not close this audit.

11 checklist items fail. Nothing in this pass was corrected. Chapter files, signature files, build scripts, and build outputs were not edited. `journal/private/` was not opened.

## Failing checklist

- [ ] **Developmental editing is not complete.** `planning/STATUS.json` records phase `5-signatures-and-build` and state `drafted` for all 114 tracked entries (108 chapters and 6 signatures). No entry is `developmental_review`. `planning/BUILD_NOTES.md` states that developmental editing was not part of this rebuild. `review/developmental/MANUSCRIPT_NOTES.md` exists and says the chapters, signatures, and build outputs were left as they are. **Fix:** apply that pass to the manuscript, then advance each ID only after the revised file is on disk.

- [ ] **Copyediting is not complete.** No copyedit record is in `review/`. No entry in `planning/STATUS.json` is `copyedited`. `planning/BUILD_NOTES.md` states that copyediting was not part of this rebuild. **Fix:** copyedit the 108 chapters, 6 signatures, front matter, and companion prose, then rebuild.

- [ ] **The workbook DOCX does not contain the drawings.** `build/The_Closer_Project_Illustrated_Workbook_v1_draft.docx` opens as a zip (21 entries, `[Content_Types].xml`, `word/document.xml`). `word/media/` is empty. The document has no `w:drawing`, `a:blip`, or `w:pict`. It does contain the path text `01-opener.svg`, `assets/chapters/001/motif.svg`, and `S01-hero.svg`. This is the limit already recorded in `planning/BUILD_NOTES.md`: SVG art is in the HTML, the EPUB, and the PDF, and the DOCX stores the SVG path instead of embedding the drawing. EPUB evidence: 127 SVG entries (13 part openers, 6 signature heroes, 108 motifs). PDF evidence: illustrated pages contain curve and line objects (page 901, chapter 097). **Fix:** embed a drawing or a print-resolution fallback for every motif, opener, and hero, or keep shipping the DOCX as a text edition and stop describing it as the illustrated file.

- [ ] **Cover art is not in the workbook.** `assets/covers/cover-front.svg` and `assets/covers/cover-back.svg` are on disk. `build/workbook.html` does not reference either file. The EPUB zip has no cover entry. PDF page 1 is the type title only: four text boxes and five rectangles, no image and no curve objects. The visible text is the draft kicker, “The Closer Project,” “Illustrated workbook,” and the deck. **Fix:** place the front cover on the title page of the HTML, PDF, and EPUB, and the back cover on the closing page, and embed the same art in the DOCX when drawings are embedded.

- [ ] **The release package is not assembled.** `release/` exists and contains no files. `EXPORT_MANIFEST.md` is not in the project root, `release/`, or `planning/`. The versioned PDF, DOCX, and EPUB are only under gitignored `build/`. **Fix:** copy the public blank exports into `release/` and add `EXPORT_MANIFEST.md` with paths, byte sizes, the DOCX drawing limit, test evidence, and the open editorial items in this report.

- [ ] **The printable cards and worksheets packet is missing.** The work order names `Printable_Cards_and_Worksheets_v1_draft.pdf`. No file with `printable`, `worksheet`, or `cards` in the name exists, other than the chapter `chapters/part-13/099-the-invisible-postcards.md`. Editable pieces exist as `journal/templates/*.md` (14 files). They are not a cut-ready packet with trim marks. **Fix:** build one PDF packet, plus an editable source, for the question cards, scenario decks, session logs, Yes/No/Maybe sheet, letter paper, postcards, hundred-point sheet, and the other game pieces the chapters name.

- [ ] **The thirteen part openers have no introductory prose.** Each HTML opener is a kicker, the SVG, and an `h1`. PDF page 900, the Part 13 opener, extracts as “PART 13 / The Inventor’s Workshop: Original Proposals” and the page number. **Fix:** write a short introduction for each of the 13 parts and print it on that opener page.

- [ ] **The S03 sample solution is not covered.** In `signature/S03-the-case-of-the-missing-tuesday.md` and in `build/workbook.html`, “Stop here if you are playing the sample.” is the last player instruction, and the next heading is “How Rowan and Vale closed it,” which states the solved Tuesday. PDF page 1052 contains the case file, “Leave the key covered.”, the stop line, and the solution heading with Rowan’s first sentences, including “The Tuesday is 10 March.” The line “Cover this until the sample case is finished.” is on page 1058, after that solution and after the journal pages. The stylesheet does not start that heading on a new sheet. **Fix:** end the player-facing sample at the stop line, start the walkthrough and the sample answer key on a new page whose first line is “Cover this,” and keep that sheet face down during play.

- [ ] **In-book journal rules are shorter than the eight-line instruction printed beside them.** `build/workbook.html` has 1,305 `writing-lines` blocks: 114 with two rules and 1,191 with three. None have eight. Chapters 099, 101, 103, 104, and 106 say, in the paragraph immediately before the spread, that printed prompts want at least eight handwriting lines. Rule spacing in `styles/workbook.css` is 0.38 in, which clears the 0.32 in minimum. The count does not. The companion prompt bank does use eight rules (see the passing companion check below). **Fix:** draw eight rules under each in-book prompt, or point that sentence at the companion sheet and label the in-book block as a short capture.

- [ ] **The Our Story companion prints builder material into the couple-facing files.** `build/journal/Our_Story_Companion.pdf` page 2 begins “Our Story — companion architecture” and addresses builders. Page 41 prints the postcard template as YAML (`activity: "099"`, `lines_per_prompt: 8`). Page 81 prints fenced markers such as `id: "012"` and `lines_per_prompt: 8` between prompts. The DOCX is the same HTML export. **Fix:** export only the title page, the couple’s instructions, the blank sheets, and the 108 prompt spreads. Leave `journal/COMPANION_STRUCTURE.md` and the expansion markers out of the PDF and DOCX.

- [ ] **A full print-size raster scan of the 1,141-page workbook was not done.** Text and layout objects were read for the sample pages listed below. That sample cannot clear clipping, overflow, or low-contrast rules on the pages that were not opened. Body ink `#241F1C` on parchment `#F6F1E7` calculates to 14.49:1. Handwriting rules `#D9CFC0` on `#FBF8F2` calculate to 1.45:1, which is a pale guide line rather than body text. **Fix:** rasterize the workbook and the companion at print size, review every page for clipped tables, card grids, running heads, and writable rules, and record the page numbers that change.

## Checks that passed

### Inventory and navigation

- 108 chapter files, IDs `001`–`108`, one file each. Titles and part numbers match `source/experience_catalog.json`. Entries `097`–`108` are `original-formulation`. Required chapter headings are present and in contract order. No `TBD`, `TK`, `TODO`, or lorem ipsum in chapter or signature bodies. Body word counts, excluding frontmatter and fenced blocks, run from 1,669 to 3,433. Fifteen chapters exceed 2,200 words; the contract allows longer games. None are under 1,200.
- Six signature files: `S01` through `S06`.
- `build/workbook.html` has 108 unique `chapter-001`–`chapter-108` anchors and six unique `signature-s01`–`signature-s06` anchors.
- All 13 part-opener SVGs and all 6 signature-hero SVGs exist and are referenced from that HTML. All 108 `assets/chapters/NNN/motif.svg` files exist, are referenced, and have 108 distinct SHA-256 hashes.
- 1,499 internal `href="#..."` links resolve to an id in the HTML. Broken links: 0.
- The time index contains `5-10`, `10-20`, `20-45`, `45-90`, `90-180`, and `multi-day`. Alphabetical, intensity, energy, format, mood, and revisit indexes are present, as are the contents and the bibliography.
- The string `scavenger` occurs 0 times in `build/workbook.html`, 0 times in the workbook DOCX document, and 0 times in the decompressed workbook PDF bytes.

### Workbook exports

| File | Bytes | What was measured |
| --- | ---: | --- |
| `build/The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` | 8,673,026 | Header `%PDF-1.4`. 1,141 pages. Every MediaBox is `0 0 504 720` pt, which is 7 by 10 in. pdfminer extracts selectable text. |
| `build/The_Closer_Project_Illustrated_Workbook_v1_draft.docx` | 861,929 | Opens as a zip. No zip part whose name contains `journal/private`. |
| `build/The_Closer_Project_Reader_v1_draft.epub` | 850,727 | First local-file entry is `mimetype`, stored (method 0), extra-field length 0, contents `application/epub+zip`. No `journal/private` entry. Nav contains `chapter-001` and `signature-s01`. |

The workbook DOCX and the HTML colophon mention the folder `journal/private/` as a path that is not read, and chapter 099 names `journal/private/mementos/` as local storage that this project does not upload. Those are sentences. They are not a packaged private journal. `git ls-files journal/private` is empty. `git check-ignore` matches `.gitignore` line 2.

### Our Story companion, personal answers

Both companion files exist:

- `build/journal/Our_Story_Companion.pdf`, 1,243,688 bytes, `%PDF-1.4`, 274 pages, MediaBox `0 0 612 792` pt (US Letter).
- `build/journal/Our_Story_Companion.docx`, 108,395 bytes, opens as a zip, no `journal/private` part.

`build/journal/our-story.html` has 108 activity headings and 432 prompt blocks (Partner A, Partner B, Shared, Revisit for each ID). All 432 have eight empty handwriting rules. The title page has two blank “Name or initials” lines. The HTML says “No real memory is supplied here” and “The names Rowan and Vale appear only in one clearly marked fictional layout sample.” All 10 Rowan/Vale mentions sit in a window that also says fictional or “not the readers.” The labeled sample line is “Burnt toast still counts.” No email address appears. The DOCX contains “Fictional,” “not the readers,” “Burnt toast,” and “No personal answers are filled in.” This audit found no fabricated answers for a real couple. The builder prose in those same files is failing item 10 above.

### Playable-rule spot checks

- **Chapter 103.** The hours rule is present and comes before the packets. In the markdown and the HTML, “Hours are only 6, 8, and 10.” sits in “What you both see before either packet is opened,” with the shared card face up and outside either envelope. PDF page 960 prints that sentence and says both players can see the closed set before North reads Packet North. Packet North begins on PDF page 962.
- **S01.** The card fence has 12 questions: Near 1–4, Middle 1–4, Far 1–4. Far 4 is specified face down. It turns only after both people say yes to “Do we turn it?” The same twelve questions and the face-down rule are in `build/workbook.html`. The text also says a printed book may already show the wording, and it gives an unseen substitute for that case.
- **S03 cover rule.** The sentences “Leave the key covered.” and “Cover this until the sample case is finished.” exist. They do not keep the solution off the player’s page. That is failing item 8.

## Sample pages inspected

Text was extracted with pdfminer. Layout objects were counted on the pages marked below. No raster page images were written.

| PDF page | What is on it |
| --- | --- |
| Workbook 1 | Type title only. Objects: 4 text boxes, 5 rectangles. |
| Workbook 2–3 | Contents, including front matter and parts 1–6. |
| Workbook 21 and 401 | Shared journal prompts. Writing rules are rectangles, not text. |
| Workbook 900 | Part 13 title only. |
| Workbook 901 | Chapter 097 opening, with curve and line objects from the motif. |
| Workbook 960–962 | Chapter 103 shared hours, blank grid, then Packet North and Packet South. |
| Workbook 1049–1052 | S03 cards, then the sample case and the uncovered solution on page 1052. |
| Workbook 1058 | “Sample answer key” and “Cover this until the sample case is finished.” |
| Workbook 1101 | Time index, including the `5-10` and `10-20` bands. |
| Workbook 1141 | Closing build note. Extracted text includes “No referenced image was missing.” |
| Companion 1 | Blank name lines. |
| Companion 2 | Builder architecture, which should not be in the couple’s book. |
| Companion 16 | Cross-reference table. pdfminer reading order interleaves wrapped part titles with activity titles; that alone is not proof of a collision. |
| Companion 41 and 81 | Template YAML and fenced markers printed in the journal. |

## Known toolchain limit

Recorded from `planning/BUILD_NOTES.md` and rechecked on these files: SVG art is present in the HTML, the EPUB, and the PDF. The DOCX stores the SVG path instead of embedding the drawing. Details are failing item 3.

## Verification performed

From `C:\Users\cliff\.cursor\The_Closer_Project`:

- Directory listing of `build/` and `build/journal/`, and of `release/`.
- Read-only counts of chapter and signature files, frontmatter IDs, HTML anchors, opener and hero references, motif hashes, internal links, the `scavenger` string, and journal-rule spans.
- Zip inspection of the workbook DOCX, the companion DOCX, and the EPUB, including the EPUB local-file header for `mimetype`.
- PDF header, MediaBox, and page-object counts, plus pdfminer text and layout-object samples for the pages in the table above.
- `git ls-files journal/private` and `git check-ignore -v journal/private/`.
- `planning/STATUS.json` state tally and `planning/BUILD_NOTES.md`.

`journal/private/` was not listed and was not read.
