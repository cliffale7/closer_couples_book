# Phase 3 acceptance matrix

Updated during the first implementation pass on `phase3/book-completion`. A gate is not PASS because a plan exists. Owner art approval, owner prose approval, and a real couple playtest stay pending.

| Gate | State | Evidence |
| --- | --- | --- |
| G01 Complete scope | PASS | `scripts/test_phase3_app_bundle.py` lists IDs 001–108 and S01–S06 once. No chapter was removed. |
| G02 Full chapter content | PASS for retention | Existing chapter and signature prose is still on disk. This pass did not abridge it. |
| G03 Time discovery | PASS | `scripts/test_phase3_discovery.py`. Shelves documented in `planning/DECISIONS.md` item 10 and `planning/phase3/VARIANT_AUDIT.md`. |
| G04 Signature parity | FAIL | Signature versions are in the index code and the app bundle. The printed companion has not yet been rebuilt with signature sections, and the workbook PDF is still the previous export. |
| G05 Journal prompts | PASS for source | Each of the 114 files has a journal fence. Equal blank lines are in the repeat pack. |
| G06 Repeat pack | PASS for files | `release/Our_Story_Repeatable_Session_Pack_v1.pdf` and `.docx`. Line height in the HTML is 0.38in. A physical print measurement is not done. |
| G07 Memoir exporter | PASS | `scripts/test_phase3_memoir.py` builds shared, partner, and full-private PDF/DOCX from fictional temp sessions and refuses `release/` plus a path escape. |
| G08 Distinct experiences | FAIL | Contrast revisions are not finished. |
| G09 Copy and research | FAIL | No new full-book proof or evidence pass has been signed in this phase. |
| G10 Art | FAIL | No new contact sheets. Night Library files were not replaced. |
| G11 Game materials | FAIL | Prior card packet still exists. It has not been regenerated against the Phase 3 text. |
| G12 All formats | FAIL | Workbook PDF, DOCX, EPUB, and companion have not been rebuilt since the index change. |
| G13 Layout scan | FAIL | The previous 1,452-page raster does not include this phase. |
| G14 Accessibility | FAIL | Not rechecked after the index change. |
| G15 Field use | FAIL | Desk matrix and the 13 human scripts are not logged as played. Real use is not claimed. |
| G16 Single status | FAIL | `PRODUCTION_BOARD.md` and `STATUS.json` still disagree. |
| G17 Android handoff | PASS for the public bundle | `release/app_content/The_Closer_Project_Content_v1-draft.zip` and `scripts/test_phase3_app_bundle.py`. An installed app was not imported; that belongs to the Android project. |
| G18 Branch and privacy | PASS for the branch checkpoint | Work is on `phase3/book-completion`. Private notes were not read or committed. |
| G19 Unabridged master | PASS | No chapter was cut, merged, or retargeted to a retail page limit. Trim remains 7×10 for the workbook. |
| G20 Owner approval | PENDING_OWNER | No owner has signed art, prose, or a playtest. |

`python -m unittest scripts.test_phase3_discovery scripts.test_phase3_memoir scripts.test_phase3_app_bundle` is the regression set for this pass.
