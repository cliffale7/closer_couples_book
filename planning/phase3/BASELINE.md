# Phase 3 baseline

Recorded at the start of `phase3/book-completion`, from `main` at `1c53ccdb95db144a9fa55a2960bc2bcc3cfd6971`.

The committed draft already had 108 chapters, six signatures, a 1,452-page 7×10 workbook, a 262-page companion, and a 49-page card packet. Those release files are unchanged by the first Phase 3 code pass. Historical QA reports remain historical.

## Observed at the start of this pass

- Indexes and Surprise Us used one `time_band` per chapter. A 10-minute version of 001 was not a separate hit. Signatures were omitted from the generated indexes.
- 071 was labeled `multi-day` even though both versions are a single day (4 hours and 12 hours).
- S05 was labeled `multi-day` even though the sitting is a 20-minute, 90-minute, or one-evening sealing. Opening later is a revisit.
- S02 durations are written as "about 30 minutes" and were not parsed until the prefix was allowed.
- Signature journal fences exist in the signature files. The companion builder still draws prompts from the 001–108 bank.
- No local memoir exporter existed. No standalone repeat-session packet existed. No versioned app-content zip existed.
- `planning/PRODUCTION_BOARD.md` and `planning/STATUS.json` do not describe the same state. They were not rewritten in this pass.
- `journal/private/` is gitignored. It was not opened.

## Not a failure of the first draft

The proofread workbook, citation limits, spoiler page breaks, and private-path guard were already in the baseline commit. This phase does not treat those closed items as open.
