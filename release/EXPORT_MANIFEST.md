# Export manifest

15 October 2026. Rebuilt on `phase4/real-illustrations` after the first eighteen lamp-lit paintings were placed: the front cover, the part 1 opener, and chapters 001–016. The other plates are still the rejected line drawings. These files are a draft for owner review. They are not a retail edition. `journal/private/` is not in this folder.

The 14 October manifest described a 1,452-page workbook. This rebuild replaces it. That earlier file is not the current book.

| File | Bytes | SHA-256 | Check |
| --- | ---: | --- | --- |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.pdf` | 15803091 | `bf6389a008524aa173b22a18dbc930401b7bef6e3a85694b74e761d34d5a169d` | 1472 pages; MediaBox 504 by 720 pt (7 by 10 in) |
| `The_Closer_Project_Illustrated_Workbook_v1_draft.docx` | 7992356 | `29af0a0dbc4973f2db2470a5f27ff4ee64cbe055e0aeeb15390e54b3cc848e55` | Opens; accepted plates embedded as JPEG, remaining slots as PNG |
| `The_Closer_Project_Reader_v1_draft.epub` | 7025299 | `33a10fa72273cc23059205cbcdb0da33de8ffaf45956bd42f48aac0c0b98b3d0` | `python scripts/validate.py` passed |
| `Our_Story_Companion_Journal_v1_draft.pdf` | 1134903 | `55512c5575853a861eca6e85f059d79dea8ad5f96ecff81b7b89c2c523931af8` | 294 pages; US Letter; S01–S06 sections present |
| `Our_Story_Companion_Journal_v1_draft.docx` | 100251 | `b35be11d5d823278280549fba79575962cbd214aa7e34cd68e06b03f3fc1c41b` | Blank prompts |
| `Printable_Cards_and_Worksheets_v1_draft.pdf` | 835355 | `90380fee1f6a291dca90851e04f678e6a876d19a987e2977691dcd4053d41202` | 49 pages; US Letter |
| `Printable_Cards_and_Worksheets_v1_draft.docx` | 50212 | `0d65988aaa43ba4dbb782a0b05f9ba22f60289238a7cf8c6329d17f6876bfe48` | Editable card text, including the S04 spent-room rule |
| `Our_Story_Repeatable_Session_Pack_v1.pdf` | 92158 | `ab059ef4dbba18a1b2d426e3dcc60c99011e0563fe7df3f9edb2fb1ff88a99cb` | 17 pages; US Letter |
| `Our_Story_Repeatable_Session_Pack_v1.docx` | 38509 | `9f249498ea39828a6694dd59993848931a766d0f20b3230a8911764f390ac1a0` | Editable blank packet |
| `OWNER_ART_REVIEW.pdf` | 532758 | `007cd15a084dd31ed5aaed97edb50f2661d65010e33d443111bcff1d463993af` | 22 letter pages; contact sheets; not an approval |

`python scripts/validate.py` passed on this workbook: 108 chapters, seven time shelves, signature links, EPUB nav and image alt text, no private journal path.

## Limits

- The workbook is 1,472 pages at 7 by 10 inches. No chapter fell under 1,200 words.
- Accepted paintings print at 5.4 inches wide. Their source files are about 1280 by 720 pixels, near 237 pixels per inch at that width. The cover file is 864 by 1152.
- Remaining chapter and part pictures are still the rejected SVG line drawings.
- DOCX embeds the accepted JPEGs directly and PNG rasters of the SVG slots.
- Chrome reprints the PDF on each run, so the PDF bytes are not stable across machines.
- Owner art approval, owner prose approval, and a real playtest are still open.
- The Android zip is `release/app_content/The_Closer_Project_Content_v1-draft.zip`, 654836 bytes, SHA-256 `3737f9c9d33214aaa3cd241a65cc4cefb9a21fa98e01eb34e1c195cc9c1deaa3`. Its manifest names source commit `b69f95bd37bc1e11842205fbf116343d3b581b3b`. `CHANGES.json` compares it with the previous public zip: no activities added or removed, 13 drawing files changed. On-device import was not tested.
