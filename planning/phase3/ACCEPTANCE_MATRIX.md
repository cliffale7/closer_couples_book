# Phase 3 acceptance matrix

Updated during the first implementation pass on `phase3/book-completion`. A gate is not PASS because a plan exists. Owner art approval, owner prose approval, and a real couple playtest stay pending.

| Gate | State | Evidence |
| --- | --- | --- |
| G01 Complete scope | PASS | `scripts/test_phase3_app_bundle.py` lists IDs 001–108 and S01–S06 once. No chapter was removed. |
| G02 Full chapter content | PASS for retention | Existing chapter and signature prose is still on disk. This pass did not abridge it. |
| G03 Time discovery | PASS | `scripts/test_phase3_discovery.py`, including 001, 017, 043, 071, S01, S02, and the three evening lines (024 extended, 035 standard, S05 extended) classified long-day with no invented minutes. `planning/phase3/VARIANT_AUDIT.md` reports 337 variants and 0 parser notes. |
| G04 Signature parity | FAIL | `scripts/build_journal.py` now appends S01–S06 prompt pages from each signature journal fence. The companion PDF has not been rebuilt with those pages, and the workbook PDF is still the previous export. |
| G05 Journal prompts | PASS for source | Each of the 114 files has a journal fence. Equal blank lines are in the repeat pack. Signature prompts are also queued in the companion builder. |
| G06 Repeat pack | PASS for files | `release/Our_Story_Repeatable_Session_Pack_v1.pdf` and `.docx`. Line height in the HTML is 0.38in. A physical print measurement is not done. |
| G07 Memoir exporter | PASS | `scripts/test_phase3_memoir.py` (4 tests). Shared PDF and DOCX omit fictional private markers, unmarked captions, and private images. Partner A omits Partner B-only markers and media. Full-private requires both local authorization files and both flags, then includes the private images. Path escape and `release/` are refused. Existing exports are not overwritten. See `review/phase3/PRIVACY_REGRESSION.md`. |
| G08 Distinct experiences | PASS for the assigned clusters | `review/phase3/EDITORIAL_CLOSEOUT.md`. All 52 practical-middle hashes were recomputed against the chapter files and matched. No chapter was rewritten. This is a text inspection, not a couple playing the activities. |
| G09 Copy and research | FAIL | No new full-book proof or evidence pass has been signed in this phase. |
| G10 Art | FAIL | All 130 drawings were reviewed in `review/phase3/ART_AUDIT.md`: 117 keep, 10 improve, 3 replace (005, 024, 061). No SVG was edited. Contact sheets and owner approval are still open. |
| G11 Game materials | FAIL | Prior card packet still exists. It has not been regenerated against the Phase 3 text. |
| G12 All formats | FAIL | Workbook PDF, DOCX, EPUB, and companion have not been rebuilt since the index change. |
| G13 Layout scan | FAIL | The previous 1,452-page raster does not include this phase. |
| G14 Accessibility | FAIL | Not rechecked after the index change. |
| G15 Field use | FAIL | Desk matrix: `review/phase3/PLAYABILITY_MATRIX.csv` (114 rows). One S04 handoff was corrected in the signature text. Field scripts: `review/phase3/FIELD_TEST_SCRIPTS.md`, all marked AWAITING_OWNER_REAL_USE. No real playtest is claimed. |
| G16 Single status | FAIL | `PRODUCTION_BOARD.md` and `STATUS.json` still disagree. |
| G17 Android handoff | PASS for the exporter tests | `scripts/test_phase3_app_bundle.py` (6 tests): 001–108 and S01–S06, stable prompt ids, initial baseline versus a no-op second bundle, explicit 103 spoiler, `requires_app_update` only for cards or a covered key. `source/prompt_registry.json` holds the current wording. The zip in `release/app_content/` is still the older bundle until the final export. On-device import is NOT TESTED IN BOOK PROJECT. |
| G18 Branch and privacy | PASS for the branch checkpoint | Work is on `phase3/book-completion`. Private notes were not read or committed. |
| G19 Unabridged master | PASS | No chapter was cut, merged, or retargeted to a retail page limit. Trim remains 7×10 for the workbook. |
| G20 Owner approval | PENDING_OWNER | No owner has signed art, prose, or a playtest. |

`python -m unittest scripts.test_phase3_discovery scripts.test_phase3_memoir scripts.test_phase3_app_bundle` is the regression set for this pass.
