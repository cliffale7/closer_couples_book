# Production decisions

Locked 14 October 2026 by the executive producer. Change only by editing this file.

1. **Title.** Working title remains The Closer Project for files, covers, and identity.
2. **Inventory.** All 108 source experiences and 13 parts stay. Signature sessions use S01–S06 and do not renumber the catalog.
3. **Toolchain.** Pandoc and Typst are not installed. Canonical source is Markdown plus YAML. DOCX via `python-docx`. EPUB via a deterministic ZIP/XHTML builder. PDF via HTML/CSS printed by the installed Edge or Chrome headless browser. No redistributed font files; use Georgia, Palatino Linotype, and Calibri, which ship with Windows.
4. **Art.** One system: midnight, parchment, copper, dusk teal, burgundy. Original SVG and programmatic illustration. No stock icons relabeled 108 times. No scavenger-hunt imagery.
5. **Research.** Chapter prose may cite only IDs in `research/CITATION_WHITELIST.md`, or a source added later with URL, access date, and evidence-reviewer sign-off. Games with no study stay classified as tradition or original design.
6. **Memoir.** Prompts are specific and blank. Fictional examples are labeled fictional. Real couple notes go only in `journal/private/`, which Git ignores.
7. **Signatures.** S01 The Long Table; S02 The Night With the Lights Low; S03 The Case of the Missing Tuesday; S04 The Branching Evening; S05 The Capsule We Open Later; S06 The Long Toast. S03 is a parlor mystery and is unrelated to any scavenger hunt.
8. **Sample proof.** The publication pipeline may render `build/fixtures/` for typesetting only. Fixture text is not a chapter and must not be copied into `release/` as if it were entry 001.
9. **Art files.** Night Library, written in `assets/styles/DESIGN_SYSTEM.md`. Chapter motifs stay `assets/chapters/NNN/motif.svg`. Part openers are `assets/parts/01-opener.svg` through `13-opener.svg` (`viewBox` 540×440), drawn from `assets/styles/PART_OPENERS.md`. Signature heroes are `assets/signatures/S01-hero.svg` through `S06-hero.svg` (`viewBox` 540×360), drawn from `assets/styles/SIGNATURE_ART.md`. Do not use `part-01.svg` or `S01.svg`.
10. **Time shelves.** Indexes and Surprise Us use each duration sentence, not only `time_band`. Through 3 hours, the upper bound of a shelf is inclusive and the next shelf starts one minute later. More than 3 hours on a single day is `long-day`. A numbered span of days is `multi-day`, including a version that also mentions a short closing conversation. Chapter 071 is a long day. S05's sitting is 45–90 minutes; opening the capsule later is a revisit, not a second-day task.
