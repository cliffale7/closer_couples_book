# Phase 3 acceptance matrix

Updated during the first implementation pass on `phase3/book-completion`. A gate is not PASS because a plan exists. Owner art approval, owner prose approval, and a real couple playtest stay pending.

| Gate | State | Evidence |
| --- | --- | --- |
| G01 Complete scope | PASS | `scripts/test_phase3_app_bundle.py` lists IDs 001–108 and S01–S06 once. No chapter was removed. |
| G02 Full chapter content | PASS for retention | Existing chapter and signature prose is still on disk. This pass did not abridge it. |
| G03 Time discovery | PASS | `scripts/test_phase3_discovery.py`, including 001, 017, 043, 071, S01, S02, and the three evening lines (024 extended, 035 standard, S05 extended) classified long-day with no invented minutes. `planning/phase3/VARIANT_AUDIT.md` reports 337 variants and 0 parser notes. |
| G04 Signature parity | PASS for the rebuilt companion | `release/Our_Story_Companion_Journal_v1_draft.pdf` is 294 letter pages. The HTML has one section each for S01–S06, with eight handwriting rules on each prompt. |
| G05 Journal prompts | PASS | 114 journal fences, plus the signature pages in the companion. Repeat pack regenerated. |
| G06 Repeat pack | PASS for files | `release/Our_Story_Repeatable_Session_Pack_v1.pdf` (17 letter pages) and `.docx`. Companion rules are 0.36 in. A physical print measurement is not done. |
| G07 Memoir exporter | PASS | `scripts/test_phase3_memoir.py` (4 tests). Shared PDF and DOCX omit fictional private markers, unmarked captions, and private images. Partner A omits Partner B-only markers and media. Full-private requires both local authorization files and both flags, then includes the private images. Path escape and `release/` are refused. Existing exports are not overwritten. See `review/phase3/PRIVACY_REGRESSION.md`. |
| G08 Distinct experiences | PASS for the assigned clusters | `review/phase3/EDITORIAL_CLOSEOUT.md`. All 52 practical-middle hashes were recomputed against the chapter files and matched. No chapter was rewritten. This is a text inspection, not a couple playing the activities. |
| G09 Copy and research | PASS for the standing proofread | The first-draft proofread logs still cover the chapters that were not rewritten. This rebuild re-read the citations in 080 (G2004, B1992) and S04 (A2000) and they still match the whitelist limits. A second human read is AWAITING_OWNER. |
| G10 Art | Contact sheets drawn, not approved | `release/OWNER_ART_REVIEW.pdf`, 22 pages. Thirteen corrections are marked awaiting the owner. Owner approval is AWAITING_OWNER. |
| G11 Game materials | PASS for the regenerated packet | Card PDF and DOCX rebuilt from the current fences. S04 cards still close a room that was already entered. 104 has 12 event cards. S01 has 12 questions. Human play is not claimed. |
| G12 All formats | PASS | Workbook PDF 1,464 pages at 7 by 10 in, plus DOCX and EPUB. Companion, cards, and repeat pack rebuilt. `python scripts/validate.py` passed. Checksums in `release/EXPORT_MANIFEST.md`. |
| G13 Layout scan | PASS for the automated scan | All 1,464 pages rasterized at 144 dpi. Pages 6 and 724 flagged, then opened: contents leaders and a journal rule, not clipped text. Pages 1, 30, and 1464 were also opened. A person did not inspect every picture. `review/PAGE_RASTER.md`. |
| G14 Accessibility | PASS for automated checks | EPUB nav, parsed XML, 129 images with alt text. No screen reader was used. `review/phase3/ACCESSIBILITY_AND_LAYOUT_QA.md`. |
| G15 Field use | Desk kit ready; human play AWAITING_OWNER | `review/phase3/PLAYABILITY_CLOSEOUT.md`. Field scripts remain AWAITING_OWNER_REAL_USE. |
| G16 Single status | PASS | `planning/PRODUCTION_BOARD.md` now points at `planning/STATUS.json` and this matrix. The old unstarted table is withdrawn. |
| G17 Android handoff | PASS for the public bundle | `release/app_content/The_Closer_Project_Content_v1-draft.zip` names source commit `b69f95bd37bc1e11842205fbf116343d3b581b3b`. `CHANGES.json` is an update against the previous zip: 13 drawing assets changed, no activities added or removed. On-device import is NOT TESTED IN BOOK PROJECT. |
| G18 Branch and privacy | PASS for the branch checkpoint | Work is on `phase3/book-completion`. Private notes were not read or committed. |
| G19 Unabridged master | PASS | No chapter was cut, merged, or retargeted to a retail page limit. Trim remains 7×10 for the workbook. |
| G20 Owner approval | PENDING_OWNER | No owner has signed art, prose, or a playtest. |

`python -m unittest scripts.test_phase3_discovery scripts.test_phase3_memoir scripts.test_phase3_app_bundle` is the regression set for this pass.
