# Export manifest

15 October 2026. Rebuilt from `phase3/book-completion` after the memoir filter, the signature companion pages, the time indexes, and the thirteen corrected drawings. These files are a draft for owner review. They are not a retail edition. `journal/private/` is not in this folder.

The 14 October manifest described a 1,452-page workbook. This rebuild replaces it. That earlier file is not the current book.

| File | Bytes | SHA-256 | Check |
| --- | ---: | --- | --- |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` | 9459916 | `5fb146b056e1c8104ca87a512e59b3a58b26bc12f36cf975fa53c451f9254a8f` | 1464 pages; MediaBox 504 by 720 pt (7 by 10 in) |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.docx` | 1953000 | `d7d5fd9bf433eb2e6d2f3a3ddcc7c0d6c274315fb94d3f336edf6e3783e9d805` | Opens; drawings embedded as PNG |
| `The_Closer_Project_Reader_v1_draft.epub` | 865014 | `e9fd0203e8171861b222628c7dec01f989e4c7eabd6bb49a701250a5ddd5bab1` | `python scripts/validate.py` passed |
| `Our_Story_Companion_Journal_v1_draft.pdf` | 1134903 | `aedb7d4e014adf375740c38540e4ec132cb96431fe0c980fb9c825d089181e9e` | 294 pages; US Letter; S01–S06 sections present |
| `Our_Story_Companion_Journal_v1_draft.docx` | 100251 | `b35be11d5d823278280549fba79575962cbd214aa7e34cd68e06b03f3fc1c41b` | Blank prompts |
| `Printable_Cards_and_Worksheets_v1_draft.pdf` | 835355 | `7f4ebf10f7add0de7a82d06c180f5379cfee9bd0747d3202e4bda89b8b47ead9` | 49 pages; US Letter |
| `Printable_Cards_and_Worksheets_v1_draft.docx` | 50212 | `60dca177666dd871de432c4b8bd8b27f11e829c459b70fe6803b90b7bee3a3c4` | Editable card text, including the S04 spent-room rule |
| `Our_Story_Repeatable_Session_Pack_v1.pdf` | 92158 | `48af93523aa60d216043fba372c5b5a0f6cf37e10ce568bf707657b66cd59ae9` | 17 pages; US Letter |
| `Our_Story_Repeatable_Session_Pack_v1.docx` | 38509 | `f93482f940f8bd238e2ba6428475c6cb3c355f979d1a087d35b65ee2d1867051` | Editable blank packet |
| `OWNER_ART_REVIEW.pdf` | 532758 | `007cd15a084dd31ed5aaed97edb50f2661d65010e33d443111bcff1d463993af` | 22 letter pages; contact sheets; not an approval |

`python scripts/validate.py` passed on this workbook: 108 chapters, seven time shelves, signature links, EPUB nav and image alt text, no private journal path.

## Limits

- Every workbook page was rasterized at 144 dpi. Two pages were flagged for margin ink and then opened. The ink is a contents leader and a journal rule, not clipped text. A person did not look at all 1,464 pictures. See `review/PAGE_RASTER.md`.
- DOCX pictures are PNG rasters of the SVG drawings.
- Chrome reprints the PDF on each run, so the PDF bytes are not stable across machines.
- Owner art approval, owner prose approval, and a real playtest are still open.
- The Android zip, when present, is a public content bundle. On-device import was not tested here.
