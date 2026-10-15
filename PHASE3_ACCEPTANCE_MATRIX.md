# Phase 3 acceptance matrix — mandatory gate evidence

Do not mark a gate PASS just because the writer/engineer says so. Put this checklist in `planning/phase3/ACCEPTANCE_MATRIX.md`, attach test logs and file paths, and re-open gates invalidated by subsequent edits. Use `PASS`, `FAIL`, `PENDING_OWNER`, or `NOT_VERIFIABLE`; leave a timestamp/commit for each observation.

| Gate | Must be shown, not asserted | Owner role |
|---|---|---|
| G01 Complete scope | IDs 001–108 precisely once; S01–S06; 13 parts; titles/premises checked against original catalog | Catalog, QA |
| G02 Full chapter content | Every chapter/signature contains complete actual mechanics, versions, why, variations, examples, afterward, distinct journal prompts and references | Editors, QA |
| G03 Time discovery | Variant-aware time index, valid exact durations, 001/017/071/S01 edge tests, actual random selection with matching versions | Catalog, QA |
| G04 Signature parity | S01–S06 in all relevant discovery indexes, bespoke companion prompts, repeatable pages and necessary cards | Signature, Journal, QA |
| G05 Personal/shared journaling | Equal partner pages, private by default, shared and revisit sections under each ID; printed fields and privacy semantics verified | Journal, QA |
| G06 Reusable physical packs | PDF+DOCX individual session cover, Partner A/B, shared, revisit, chronology, photo/memento, annual and continuation pages actually exported | Journal, Publication |
| G07 Local memoir compiler | CLI command builds three privacy-mode PDFs/DOCX from fictional entries, multiple dates/IDs/attempts, excludes private pages; no network, no Git leakage | Private Export, QA |
| G08 Distinct experiences | All mandatory contrast clusters reviewed, meaningful mechanical differences evidenced in actual text and game materials | Developmental, Play |
| G09 Copy/proof/research | All sources inspected, no placeholders/incorrect citations; all text edited and independent evidence-review signed | Evidence, Copy, QA |
| G10 Art quality | All 129 major image files + 2 covers reviewed; readable contact sheets produced, improvement list and owner choices documented | Art, Publication |
| G11 Game materials | Card counts, point totals, start/end/passing/spoilers/branches tested; printer-friendly packet | Play, QA |
| G12 Format generation | Full PDF, editable illustrated DOCX, EPUB, companion PDF/DOCX, cards PDF/DOCX, repeat pack PDF/DOCX, complete manifest/hashes | Publication, QA |
| G13 Layout | All current PDF pages rasterized; automated margin check on all; visual representative samples + flagged pages inspected separately; no clipped critical content | Publication, QA |
| G14 Accessibility | EPUB and headings/alt/nav verified, screen-reader manual check or explicit pending, readable printable rules | Accessibility, QA |
| G15 Field use | 114 desk-playability records, 13 human test scripts; real human completion logged only when it happens | Field, QA |
| G16 Project truth | Status JSON/board/archive/current status coherent and pointed to from README | Integration, QA |
| G17 Android handoff | Schema manifest, per-ID data/assets/prompt stable IDs, content hashes, deltas/migrations, compatibility tests | App Handoff, QA |
| G18 Privacy & backup | No personal data touched; public releases sanitized; safe branch, commits and owner-authorized remote backup | Privacy, Integration |
| G19 Unrestricted master size | No cut/merge/split, no Amazon edition, unchanged 7×10 main trim, improved margins and writable areas | Integration, QA |
| G20 Owner approval honesty | Art/writing/playtest/actual-paper review approval still PENDING unless owner explicitly signs off | Integration, QA |

## Required regression cases

- `001`: short 10-minute choice available when choosing quick activities; standard 30-minute remains in appropriate shelf; both link to same canonical ID without duplicate chapters.
- `017`: 8-minute short eye-gaze variant selectable with gaze/touch consent treated correctly and not falsely labeled as a proven four-minute love effect.
- `071`: four-hour and twelve-hour *single-day* experiences are visible under truthful long-day filters; do not misclassify as multi-day.
- `032`, `048`, `099`: multi-day choices retain date-range recording in journal and revisits; selecting a quick prompt cannot accidentally start their full multi-day mode.
- `S01`: 45-minute short and 2-hour standard variants included, with separate signature journal IDs/prompts.
- `S03`: opening player instructions and answer key cannot appear on the same print sheet; hidden material not leaked to cards or accessible default screen. 
- `043`: guess/reveal system has enough actual questions and a fair example.
- `103`: logic grid solvable with published packets, shared hours card public at setup, facilitator key kept separate from play.
- `104`: event cards and fictional sample response align, and the charter mechanics can be played start to finish.
- `106`: optional zero-point categories, exactly 100 points per person, valid consent around proposed outcomes, printed two-sheet allocation works.
- Privacy fixture: A private entry is absent from shared mode and other partner mode; old attempt retained after new prompt revision.
- Negative security: any attempt to export into `release/` fails; symlink/path traversal out of journal scope fails; logs never echo text; `git status --ignored` verifies isolation.
- App sync: no-op import, changed copy, changed image, retired prompt, changed variant, schema mismatch, stable old response IDs.

## Stop/go rule

ALL technical/editorial gates G01–G19 must pass before asking owner for a final editorial/art/physical proof review, apart from any explicitly external limitations that cannot be completed in the available environment. A formal `OWNER_APPROVED` or `PUBLICATION_READY` state is **not** permitted while actual owner/human playtesting signatures remain unsigned. An owner-review-ready state may be reported accurately.
