# Export manifest

15 October 2026. Rebuilt on `phase4/real-illustrations` after all 130 lamp-lit paintings were placed: both covers, the title image, all 13 part openers, all 108 chapters, and signature heroes S01–S06. These files are a draft for owner review. They are not a retail edition. `journal/private/` is not in this folder.

The 14 October manifest described a 1,452-page workbook. This rebuild replaces it. That earlier file is not the current book.

| File | Bytes | SHA-256 | Check |
| --- | ---: | --- | --- |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` | 57450761 | `69c43046d7b914e9a41de24d0d293c080ee06766e9e2b68726f2ba33918782a8` | 1506 pages; MediaBox 504 by 720 pt (7 by 10 in) |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.docx` | 47588895 | `b9b090117684df8a7c594fc0a20d9b835d6855253c340ac4621f5e4eb281f002` | Opens; accepted plates embedded as JPEG |
| `The_Closer_Project_Reader_v1_draft.epub` | 47408137 | `5e4024c2d735dbcefe49875672383ad2f342501fe1b2c4f27780f71cf64aff54` | `python scripts/validate.py` passed |
| `Our_Story_Companion_Journal_v1_draft.pdf` | 1134903 | `55512c5575853a861eca6e85f059d79dea8ad5f96ecff81b7b89c2c523931af8` | 294 pages; US Letter; S01–S06 sections present |
| `Our_Story_Companion_Journal_v1_draft.docx` | 100251 | `b35be11d5d823278280549fba79575962cbd214aa7e34cd68e06b03f3fc1c41b` | Blank prompts |
| `Printable_Cards_and_Worksheets_v1_draft.pdf` | 835355 | `90380fee1f6a291dca90851e04f678e6a876d19a987e2977691dcd4053d41202` | 49 pages; US Letter |
| `Printable_Cards_and_Worksheets_v1_draft.docx` | 50212 | `0d65988aaa43ba4dbb782a0b05f9ba22f60289238a7cf8c6329d17f6876bfe48` | Editable card text, including the S04 spent-room rule |
| `Our_Story_Repeatable_Session_Pack_v1.pdf` | 92158 | `ab059ef4dbba18a1b2d426e3dcc60c99011e0563fe7df3f9edb2fb1ff88a99cb` | 17 pages; US Letter |
| `Our_Story_Repeatable_Session_Pack_v1.docx` | 38509 | `9f249498ea39828a6694dd59993848931a766d0f20b3230a8911764f390ac1a0` | Editable blank packet |
| `OWNER_ART_REVIEW.pdf` | 48337869 | `5a304ca9fc60486e51659c9ac2124017183fa9cfcd2fae5b186987e14d866fa6` | 22 letter pages; the 130 accepted paintings; not an approval |

`python scripts/validate.py` passed on this workbook: 108 chapters, seven time shelves, signature links, EPUB nav and image alt text, no private journal path.

## Limits

- The workbook is 1,506 pages at 7 by 10 inches. The page after the cover is the title still life. No chapter fell under 1,200 words.
- Accepted paintings print at 5.4 inches wide. Their source files are about 1280 by 720 pixels, near 237 pixels per inch at that width. The cover file is 864 by 1152.
- DOCX embeds the accepted JPEGs directly.
- Chrome reprints the PDF on each run, so the PDF bytes are not stable across machines.
- Owner art approval, owner prose approval, and a real playtest are still open.
- The Android zip is `release/app_content/The_Closer_Project_Content_v1-draft.zip`, 47196423 bytes, SHA-256 `10701f61e7331a0029f4ff0604504d689a0f32752509264fb378a2da41925a0d`. Its manifest names source commit `36f923ad22cd506cb5b51e0b2d59d098d0a3ea05`. `CHANGES.json` compares it with the previous public zip: no activities added or removed, 114 activities changed because their artwork path changed, 130 paintings added, and 130 line drawings removed. On-device import was not tested.
