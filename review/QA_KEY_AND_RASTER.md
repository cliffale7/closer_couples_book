# QA recheck: chapter 103 key and page raster

**Date:** 14 October 2026  
**Scope:** the two items that failed in `review/QA_AFTER_COPYEDIT.md`. Nothing else from that audit was reopened. Older QA reports were not edited.  
**Verdict:** both items hold. Fail count: 0. This is still not a finished release.  
**Report path:** `review/QA_KEY_AND_RASTER.md`

Chapter files, signature files, scripts, styles, and release files were not edited. `journal/private/` was not opened.

## Checklist

- [x] **Chapter 103’s facilitator key starts on its own sheet, and “Three ways to play” starts after that key.** `build/workbook.html` gives `class="page-break"` to both `chapter-103-facilitator-section-solution-key` and `chapter-103-three-ways-to-play`. The inlined CSS applies `break-before: page` and `page-break-before: always` to `h2.page-break` and `h3.page-break`. In `build/The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` (1,452 pages, every MediaBox 504×720 pt), page 1240 ends on “How to customize” and “Stopping is a result.” Page 1241 begins “Facilitator section: solution key,” prints the nine solution steps, including “The remaining hour, 10, is the walk,” and prints the solved grid. Page 1242 finishes the fictional practice pair and ends “End of the facilitator section.” Page 1243 begins “Three ways to play” and does not reprint the solved grid. Build and release workbook PDFs are both 9,110,973 bytes and share one SHA-256. The card packet still omits that solution sentence: it is absent from `print/CARDS_AND_WORKSHEETS.md`, from the extracted text of `release/Printable_Cards_and_Worksheets_v1_draft.pdf` (49 pages), and from the joined text of `release/Printable_Cards_and_Worksheets_v1_draft.docx`. The build copies of that PDF and DOCX are the same sizes, 833,654 and 50,172 bytes.

- [x] **The page raster reviews every page of the current PDF, and the opened pages do not clip text.** `review/PAGE_RASTER.md` records 1,452 pages, the page count of the current workbook PDF. `build/page-raster/` contains `page-0001.png` through `page-1452.png`, 1,452 files, no gaps, each 1008×1440 pixels. Pages 6, 724, 1241, 1242, and 1243 were opened. Text is not clipped on any of them. Pages 6 and 724 put a light rule at y=1336, running from about x=97 to x=909: the last contents rule on page 6, and the bottom rule of the journal box on page 724. The page number sits below that rule, inside the sheet. Side margins on the opened pages are white. On page 1241 the last line of the practice pair is whole, and the sentence continues at the top of page 1242. Page 1243 starts “Three ways to play” with its own top margin under the running head.

## Pages opened

| Page | What is on it | Text |
| --- | --- | --- |
| 6 | End of the contents, including Part 13, the signature sessions, and the indexes. | Not clipped. The last entry, “Time,” sits above a dotted rule and the page number. |
| 724 | End of a chapter and an Our Story box with handwriting rules. | Not clipped. The box closes above the page number. |
| 1241 | Facilitator key, steps 1–9, the solved grid, the bypass, and the start of the fictional practice pair. | Not clipped. The grid’s three rows are complete. |
| 1242 | The rest of the practice pair, then “End of the facilitator section.” | Not clipped. |
| 1243 | “Three ways to play,” then “Going deeper” and “Variations and replay.” | Not clipped. No solved grid on this sheet. |

A later “Three ways to play” on PDF page 1258 belongs to another chapter (principles and event cards). It is not the chapter 103 heading and it does not carry the solved grid.

## Why this is still not a release

These three limits are unchanged, and this pass does not close them:

- Workbook DOCX art is PNG. `build/The_Closer_Project_Illustrated_Workbook_v1_draft.docx` has 129 files under `word/media/`, all PNG. SVG paths appear only as written filenames in the document text.
- PDF bytes are not stable. `release/EXPORT_MANIFEST.md` records that Chrome reprints the PDF on each run. The build and release copies match each other today; a reprint is not guaranteed to match those bytes.
- `planning/STATUS.json` still has `"state": "drafted"` on all 108 chapters and all 6 signatures.

## Verification performed

From `C:\Users\cliff\.cursor\The_Closer_Project`:

- HTML class and CSS check for the two chapter 103 headings
- PDF page count, MediaBoxes, and text of pages 1238–1245 and 1258
- File size and SHA-256 of the build workbook PDF against the release copy
- Text search of the card-packet PDF, DOCX, and `print/CARDS_AND_WORKSHEETS.md` for “The remaining hour, 10, is the walk”
- Dimensions of all 1,452 rasters
- Opened `build/page-raster/page-0006.png`, `page-0724.png`, `page-1241.png`, `page-1242.png`, and `page-1243.png`
- `planning/STATUS.json` state count, and the workbook DOCX media extensions

`journal/private/` was not listed and was not read.
