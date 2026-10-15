# Independent check of this rebuild

15 October 2026. Commands were run from the repository root after the art corrections were already committed.

| Command | Result |
| --- | --- |
| `python scripts/build_all.py` | Exit 0. HTML, DOCX, EPUB, and PDF written. |
| `python scripts/build_journal.py` | Exit 0. Companion PDF 1,134,903 bytes. HTML contains one heading each for S01–S06. |
| `python scripts/build_cards.py` | Exit 0. 104 still contributes 12 event cards. S01 still contributes 12 questions. |
| `python scripts/build_repeat_pack.py` | Exit 0. PDF 92,158 bytes. |
| `python scripts/build_art_review.py` | Exit 0. 22-page contact PDF. |
| `python scripts/validate.py` | PASS. 108 chapters. PDF 1,464 pages, 7 by 10 in. |
| `python scripts/raster_pages.py` | 1,464/1,464. Two margin flags, both opened. |

Index HTML contains all seven time shelves. Chapter 001 is in the 5–10 minute shelf. Chapter 071 is not. S01 links to `signature-s01-three-ways-to-play`.

EPUB: 129 images, 0 missing alt attributes.

Citations in the two phase-3 prose edits were re-read against the standing limits: 080 still ties G2004 to well-being beyond the event and refuses a divorce percentage from B1992. S04 still limits A2000 to short-term experienced quality. No new citation was added in this rebuild. The earlier proofread logs were not redone chapter by chapter.

Private journal files were not opened. Release copies were made from `build/` after the commands above. Checksums are in `release/EXPORT_MANIFEST.md`.

Not claimed: a screen reader, a printed ruler, a couple's playtest, or owner approval.
