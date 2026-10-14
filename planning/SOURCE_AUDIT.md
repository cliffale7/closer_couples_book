# Source audit — 14 October 2026

Status: **PASS.** Originals were opened as Office Open XML, not trusted from the convenience extracts alone.

## Checksums

Both files match `source/SOURCE_CHECKSUMS.txt`.

| File | SHA-256 |
| --- | --- |
| `source/The_Closer_Project_Working_Manuscript_v0.1.docx` | `48f6d32c94e3b0bac1e6e3df3007203ffae30104dcc03015aa8f2b15de6b821e` |
| `source/The_Closer_Project_Concept_and_Feedback_Invitation.docx` | `8bebf324b4a945a7440a00b5fd4ca714dece7e555a4e3f6c5894381c3758724a` |

Originals stay unmodified in `source/`.

## Inventory

- Working manuscript body: 108 numbered entries, IDs 001–108, no gaps and no duplicates.
- Titles and premises match `source/experience_catalog.json` after apostrophe and dash normalization. Machine comparison is in `planning/source_audit.json`.
- Thirteen parts and ID ranges match the work order.
- The manuscript convenience extract also contains 001–108 in order.
- `planning/ORIGINAL_IDEAS_EXPANDED.md` covers 097–108 only.
- The manuscript contains one table: a provisional time index with illustrative IDs. Those IDs are examples, not exclusive time-band assignments. Final durations come from written mechanics.
- Editorial metadata inside the manuscript is `TBD` on purpose. That scaffolding is not publishable chapter copy.
- Concept document confirms the audience (mature, curious adults; not a crisis manual) and voluntary participation.

## Conflict log

| Topic | Sources | Resolution |
| --- | --- | --- |
| Whether to cut or merge activities | Concept feedback questions invite suggestions to remove or combine. The manuscript and work order require the full inventory. | Keep all 108. Duplicated mechanisms may be flagged in editorial notes only. |
| Duration metadata | Manuscript marks duration TBD and gives illustrative time-index examples. | Writers assign real short/standard/extended estimates from the mechanics. |
| Eye contact and “36 questions” | Not specified as science in the source premises. | See `research/CITATION_WHITELIST.md`. Do not claim four minutes of eye contact induces love. Do not copy the Aron question set verbatim. |

Regenerate this audit with `python scripts/audit_sources.py`.
