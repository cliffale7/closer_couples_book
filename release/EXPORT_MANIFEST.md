# Export manifest

14 October 2026. These files are a validated draft. They are the public blank edition. `journal/private/` is not in this folder.

| File | Bytes | Check |
| --- | ---: | --- |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` | 9111548 | `%PDF-`; 1452 pages; MediaBox 504 by 720 pt (7 by 10 in) |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.docx` | 1925420 | Opens; part-opener check passed because drawings are embedded |
| `The_Closer_Project_Reader_v1_draft.epub` | 859617 | `python scripts/validate.py` passed, including mimetype stored first |
| `Our_Story_Companion_Journal_v1_draft.pdf` | 1057976 | 262 pages; US Letter |
| `Our_Story_Companion_Journal_v1_draft.docx` | 95955 | Blank prompts; no builder architecture in the HTML source |
| `Printable_Cards_and_Worksheets_v1_draft.pdf` | 833863 | 49 pages; US Letter; dashed cut borders |
| `Printable_Cards_and_Worksheets_v1_draft.docx` | 50181 | Editable card text |

`python scripts/validate.py` passed on the workbook after the copyedit rebuild. A separate word count, with fenced blocks removed, found no chapter under 1,200 words. Card generation required 12 event cards for 104 and 12 questions for S01.

## What changed since the earlier QA report

The earlier report is `review/FINAL_QA_REPORT.md`. It scored a previous export. This folder is a later build.

- Cover art is placed on the workbook title and colophon. The DOCX embeds PNG screenshots of the SVG art. HTML, EPUB, and PDF still use the SVG files.
- Thirteen part introductions are in the book.
- In-book journal prompts use eight handwriting rules. The session line stays at two.
- The companion no longer prints builder notes, prompt-bank fences, or a private-folder path.
- Proofread logs for all 108 chapters, the six signatures, the front matter, and the journal pages are in `review/proofread/`. This export was rebuilt after that pass. `planning/STATUS.json` marks those entries copyedited.
- The fictional Tuesday solution starts after the heading "Cover this until the sample case is finished," which is marked to begin a new page.
- Chapter 103's facilitator key starts on its own sheet. "Three ways to play" starts on the next sheet, so the solved grid does not share a page with the play text.
- The card packet prints hours 6, 8, and 10 on the shared card before the sealed packets. It does not reprint the covered answer section or the solved Tuesday sample.

## Limits still open

- Every workbook page of this 1,452-page PDF was rasterized at 144 dpi. The review is `review/PAGE_RASTER.md`. Two pages put a one-pixel rule on the footer boundary. No text was cut off, and no page from that scan needs a layout change.
- DOCX pictures are rasters, not live SVG.
- Chrome reprints the PDF on each run, so PDF bytes are not stable.
- Chapter states in `planning/STATUS.json` say `copyedited`. A second human read is still the right check before anyone treats a sentence as final.
- Near-duplicate chapters were flagged and kept.
- Activity 100's printable piece is a log with the chapter's own columns. The book does not define a separate weather-card deck.
- This manifest does not call the edition finished.
