# QA after copyedit

**Date:** 14 October 2026  
**Edition under test:** the copyedit rebuild in `build/` and `release/`, not the earlier 1,141-page export recorded in `review/FINAL_QA_REPORT.md`  
**Verdict:** not a release. `python scripts/validate.py` passed, and that pass does not close this audit.

2 checklist items fail. Nothing in this pass was corrected. Chapter files, signature files, research, styles, and build scripts were not edited. `journal/private/` was not opened.

## Failing checklist

- [ ] **Chapter 103’s solution key shares sheets with player text.** In `build/workbook.html`, `<h3 id="chapter-103-facilitator-section-solution-key">` has no `page-break` class. Workbook PDF page 1240 ends “How to customize,” then prints “Facilitator section: solution key” and solution step 1 (“S3 allows question-at-6 with Harbor-at-8, or question-at-8 with Harbor-at-10”). Page 1241 continues through “The remaining hour, 10, is the walk,” prints the solved grid, and then starts “Three ways to play” (`id="chapter-103-three-ways-to-play"`). The chapter text on that same spread says to start the key on a new sheet and leave it face down. **Fix:** give the facilitator heading and the following “Three ways to play” heading the same `page-break` class already used on the S03 cover heading, rebuild the workbook PDF, and copy that PDF into `release/`. Leave the solution out of the card packet.

- [ ] **A full print-size raster of all 1,451 workbook pages was not reviewed.** `build/raster/` holds 129 PNGs: 108 at 440×280, 13 at 540×440, 6 at 540×360, and 2 at 522×738. Those are the motif, opener, hero, and cover renders. They are not page rasters. `build/raster-test.png` is 8,481 bytes. This audit rendered 13 workbook pages at 144 dpi (1008×1440, which is 7×10 in) and opened the pages listed below. That sample cannot clear clipping, overflow, running heads, or handwriting rules on the pages that were not opened. **Fix:** rasterize every workbook page at print size, review each image, and record the page numbers that change.

## Retests that cleared

### 1. Consent repairs are in the chapter text

- `chapters/part-05/034-the-yes-no-maybe-game.md` has `touch: false`. The close, the short game, the standard game, the replay house rule, Vale’s example line, and the partner A prompt keep “easy and soon” in the same breath as “you still ask” and “nothing else is scheduled.” The spoken line is “Easy and soon, we still ask, and nothing else is scheduled.”
- `chapters/part-05/035-the-art-of-anticipation.md` has `touch: true`. The landing says “A yes to the written outline is not a yes to touch when the landing starts” and “Sex still needs a present yes when you reach it. A yes to a kiss is not that yes.” The example asks, “Yellow still ends it. Is the kissing we wrote still a yes?”
- `chapters/part-05/036-the-sensory-date.md` says “Each hosted station stays behind a fresh offer from the host for that station.” The sample offer ends “Do you want this station?” The same question is in the worked example for taste and for texture.
- `signature/S02-the-night-with-the-lights-low.md` station 3 says “Temperature needs its own yes before it starts” and “Fabric needs its own yes before the cloth moves.”

### 2. The copyedit logs name edits that are in the files

`review/copyedit/openings.md` and `review/copyedit/sensual-consent.md` are on disk. Every quoted `Now:` sentence in `openings.md` occurs in the file that bullet names. Checked openings in 005, 009, 028, 046, 057, 073, and S01 place the new sentence ahead of any retained older wording. `planning/STATUS.json` still has `"state": "drafted"` on all 114 tracked entries. That field was not treated as evidence the prose was untouched. The logged repairs are present, so this item clears. The edition is still unfinished because of the two failures above.

### 3. Workbook DOCX drawings are embedded PNGs

`build/The_Closer_Project_Illustrated_Workbook_v1_draft.docx` and the release copy are byte-identical, 1,925,407 bytes. Each zip has 129 files under `word/media/`, all PNG, none empty, 1,063,949 bytes of media. `word/document.xml` contains 129 `w:drawing` elements and 129 `a:blip` elements. `word/media/image1.png` is the front-cover art. Live SVG inside the DOCX is not required, and the document does not contain the path `01-opener.svg`.

### 4. Cover art is on the title and the colophon

`build/workbook.html` line 457 places `assets/covers/cover-front.svg` in `<header class="title-page" id="title-page">`. The colophon, `id="colophon"`, places `assets/covers/cover-back.svg`. Workbook PDF page 1 shows that front cover above the type title. Page 1448 shows the back cover above the build note.

### 5. The seven release files match the manifest

`release/EXPORT_MANIFEST.md` lists seven files. All seven are present, and each size matches the manifest to the byte:

| File | Bytes |
| --- | ---: |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` | 9,109,709 |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.docx` | 1,925,407 |
| `The_Closer_Project_Reader_v1_draft.epub` | 859,759 |
| `Our_Story_Companion_Journal_v1_draft.pdf` | 1,057,551 |
| `Our_Story_Companion_Journal_v1_draft.docx` | 95,928 |
| `Printable_Cards_and_Worksheets_v1_draft.pdf` | 833,654 |
| `Printable_Cards_and_Worksheets_v1_draft.docx` | 50,172 |

The workbook PDF is `%PDF-`, 1,451 pages, and every MediaBox is 504×720 pt. The companion PDF is 262 pages at 612×792 pt. The card PDF is 49 pages at 612×792 pt. The manifest says this folder is a validated draft and does not call the edition finished. Build and release copies of the workbook PDF, DOCX, and EPUB, and of the companion PDF and DOCX, share SHA-256 hashes.

### 6. The card packet is present and keeps the solved lines out

`print/CARDS_AND_WORKSHEETS.md` is the editable source. The release PDF is 49 US Letter pages, and the release DOCX opens as a zip. Chapter 104 prints twelve event cards in the procedure and again in the cards block; packet pages 14–15 print cards 1–12, from “The stores run low” through “The newcomer.” S01 prints twelve questions, Near 1–4, Middle 1–4, and Far 1–4, in the signature and on packet pages 16–17. Packet page 24 is the 103 shared card: “Hours are only 6, 8, and 10.” Packet page 25 is Packet North and page 26 is Packet South. Workbook PDF page 1236 prints that hours sentence under “What you both see before either packet is opened,” before the packet bodies. The packet PDF and the packet DOCX contain none of “The Tuesday is 10 March,” “The remaining hour, 10, is the walk,” `journal/private`, or `scavenger`.

### 7. Thirteen part introductions are in the book

`build/workbook.html` has 13 elements of class `part-intro` and 13 part openers. The thirteen paragraphs match `parts/INTRODUCTIONS.md` exactly. Workbook PDF page 13 prints the Part 1 opener, its drawing, and the first of those paragraphs.

### 8. The S03 sample solution starts after the cover heading

`build/workbook.html` has one occurrence of “The Tuesday is 10 March,” and it follows `<h3 id="signature-s03-cover-this-until-the-sample-case-is-finished" class="page-break">`. The inlined CSS gives `h3.page-break` `break-before: page` and `page-break-before: always`. Workbook PDF page 1357 ends on “Stop here if you are playing the sample.” Page 1358 begins “Cover this until the sample case is finished” and then gives “The Tuesday is 10 March.”

### 9. In-book writing rules are only counts 2 and 8

`build/workbook.html` has 1,305 `writing-lines` blocks: 114 with two spans and 1,191 with eight. Every two-span block is under the heading “Session.” Workbook PDF page 20 shows eight rules under each of two private prompts, with the last rule above the page number.

### 10. The companion no longer prints builder material

`build/journal/our-story.html` contains none of `companion architecture`, `lines_per_prompt`, `journal/private`, or `scavenger`. The companion PDF (262 pages) and the companion DOCX match that result. Companion PDF page 2 is “How to use these pages” and includes “No real memory is supplied here.”

## Checks that also held

- 108 chapter files, IDs `001`–`108`, no missing IDs and no duplicate IDs. Six signature files, `S01`–`S06`.
- Chapters `097`–`108` each have `classification: original-formulation`. The near-duplicate pairs named in `review/developmental/MANUSCRIPT_NOTES.md` are still separate files. None were merged.
- `build/workbook.html` has 1,499 internal `href="#..."` links and 0 broken targets. The string `scavenger` occurs 0 times in that HTML, in the workbook PDF, in the EPUB xhtml, in the card packet, and in the companion.
- `python scripts/validate.py` printed `PASS  validation`, including 108 chapter files, a readable DOCX, an EPUB whose mimetype is stored first, and a 1,451-page PDF whose trim is 7 by 10 inches.
- Private journal: `git check-ignore -v journal/private/` matches `.gitignore` line 2. `git ls-files journal/private` is empty. The workbook DOCX, companion DOCX, card DOCX, and EPUB have no zip part whose name contains `journal/private`. The workbook mentions that folder twice as a sentence: PDF page 1186 (local memento storage that this project does not upload) and PDF page 1448 (the folder is not read). `validate.py` refused to read `journal/private/unused.md`.

## Sample pages opened

Rendered at 144 dpi for the workbook (1008×1440) and 108 dpi for the letter sheets. Text was also extracted for these pages.

| Page | What is on it |
| --- | --- |
| Workbook 1 | Front cover drawing, then the type title “Illustrated workbook.” Margins hold the art. |
| Workbook 13 | Part 1 kicker, opener drawing, title, and the part introduction. |
| Workbook 20 | Two private prompts, eight handwriting rules under each. The last rule sits above the page number. |
| Workbook 1236 | Shared reference card. “Hours are only 6, 8, and 10.” comes before either packet is opened. |
| Workbook 1237 | Blank grid with Cedar, Harbor, and Lantern. Column heads wrap and remain readable. |
| Workbook 1240 | “How to customize,” then the facilitator key and solution step 1 on the same sheet. |
| Workbook 1241 | Solution steps 2–9, the solved grid, then “Three ways to play.” |
| Workbook 1357 | Notes, then “Stop here if you are playing the sample.” No solved Tuesday. |
| Workbook 1358 | “Cover this until the sample case is finished,” then “The Tuesday is 10 March.” |
| Workbook 1448 | Back cover, then the build note. |
| Workbook 1451 | End of the source list and “No referenced image was missing.” |
| Packet 14 | Chapter 104 cards 1–8, dashed cut borders, text inside the borders. |
| Packet 16 | S01 Near 1–4 and Middle 1–4. |
| Packet 24 | 103 shared card and blank grid, marked to leave face up. |
| Packet 25 | Packet North, four clues, no solution sentence. |
| Companion 2 | Couple-facing instructions. No builder heading and no template fence. |

## Verification performed

From `C:\Users\cliff\.cursor\The_Closer_Project`:

- `python scripts/validate.py`
- File sizes and SHA-256 comparisons for `build/` against `release/`
- Zip inspection of both workbook DOCXes, the card DOCX, the companion DOCX, and the EPUB
- HTML counts for part introductions, writing-line spans, the S03 heading, internal links, and `scavenger`
- PDF page counts and MediaBoxes, plus text search of the workbook, the 49-page packet, and the 262-page companion
- Print-size rasters of the sample pages in the table above
- `git check-ignore -v journal/private/` and `git ls-files journal/private`

`journal/private/` was not listed and was not read.
