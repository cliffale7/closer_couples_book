# Final closeout board

Branch: `phase3/book-completion`. This board is the current machine record. It is not owner approval.

| Gate | State | Evidence | Open |
| --- | --- | --- | --- |
| G01 Scope | PASS | App bundle test lists 001–108 and S01–S06 once. | None. |
| G02 Retention | PASS | No chapter cut in the commits below. | None. |
| G03 Time discovery | PASS | `scripts/test_phase3_discovery.py`. 337 variants. 0 parser notes. Evening lines are explicit long-day with no invented minutes. | Rebuild the printed index into the workbook. |
| G04 Signature parity | FAIL | Companion builder queues S01–S06 pages. Unit test checks the blocks. | Companion PDF/DOCX not rebuilt. |
| G05 Journal prompts | PASS for source | 114 journal fences. Signature prompts included in the builder. | Rendered companion still old. |
| G06 Repeat pack | PASS for files | Existing repeat-pack PDF/DOCX. 0.38 in line height in HTML. | Physical measure not done. |
| G07 Memoir privacy | PASS | `review/phase3/PRIVACY_REGRESSION.md`. Four synthetic tests. | Not identity verification. Not encrypted. |
| G08 Distinct experiences | FAIL | Prior clusters 001/005/081, 041/107, 039/046, 006/102 left distinct. Part 10: 080 rewritten. | Remaining clusters are in progress with the developmental editor. |
| G09 Copy and research | FAIL | No new full proof. | After chapter edits. |
| G10 Art | FAIL | Audit stands. Drawing corrections are in progress with the art director. | 13 assets, contact sheets, owner approval. |
| G11 Game materials | FAIL | S04 spent-room rule is in the signature and the last card packet. | Regenerate cards after final text. |
| G12 All formats | FAIL | Workbook, companion, and release zip are older than HEAD. | Full rebuild after content locks. |
| G13 Layout scan | FAIL | Previous raster is not this phase. | Raster the new PDF and say what was only scanned. |
| G14 Accessibility | FAIL | Not rechecked. | After rebuild. |
| G15 Field use | FAIL | Desk matrix and field scripts exist. Human sessions AWAITING_OWNER_REAL_USE. | Owner playtest. |
| G16 Single status | FAIL | Boards still need one reconciliation after the rebuild. | Final pass. |
| G17 Android handoff | PASS for tests | Six bundle tests. Registry committed. Release zip not yet refreshed. | Final zip with the real source commit. On-device import not tested here. |
| G18 Branch and privacy | PASS | Work is on `phase3/book-completion`. Private notes were not committed. | Do not merge to `main`. |
| G19 Unabridged | PASS | 7×10 master. No retail cut. | None. |
| G20 Owner approval | AWAITING_OWNER | Art, prose, and a real playtest are not signed. | Owner. |

Commits on this branch after `488e404`:

- `75851f0` private memoir field filter, evening duration labels, signature pages in the companion builder.
- `2fff025` stable prompt ids and bundle comparison.

`main` stays the first-draft baseline. This branch is not merged.
