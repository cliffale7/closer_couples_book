# THE CLOSER PROJECT — PHASE 3: FIRST-EDITION COMPLETION & PUBLICATION READINESS
## Binding master work order for Cursor and its delegated specialist agents

**Project:** The Closer Project — existing illustrated relationship workbook + *Our Story* memoir companion  
**Canonical repository:** `https://github.com/cliffale7/closer_couples_book`  
**Inspected baseline:** `main` at `1c53ccdb95db144a9fa55a2960bc2bcc3cfd6971` (14 October 2026); **verify current HEAD before making changes**.  
**Phase:** post–first-draft editorial, usability, production and memoir completion.  
**Source of truth:** existing `source/experience_catalog.json`, original source DOCX files, chapters/ and signature/ Markdown + YAML frontmatter, book production contract, and this work order.  
**Required result:** an exceptionally complete, trustworthy, useful, visually coherent, *single master edition* of the full book, backed by reproducible exports and objective QA evidence. Owner approval and genuine human playtest are the only gates that may remain externally pending after all technical/editorial work is completed.

> **SIZE POLICY — NON-NEGOTIABLE:** Do not reduce, condense, abridge, split into print volumes, or reformat merely to meet Amazon/KDP or binding restrictions. Do not target a smaller page count, cheaper print price, or platform limit. The existing 7 × 10-inch master workbook may be **as large as it needs to be**, and pages may increase to improve space, illustrations, readability or actual journaling usability. Retain the complete reader EPUB, editable DOCX, companion journal and worksheets. **Do not create a special Amazon edition, alternate shortened reader or split-volume edition during this phase.** Those are separate future projects requiring owner authorization.

> **IN-PLACE POLICY:** This is a continuation of an existing substantial finished *draft*, not permission to restart or replace the content, abandon the art system, change IDs, or discard accomplished work. There are 108 numbered experiences in 13 parts, plus six signatures `S01`–`S06`, an illustrated workbook, distinct artwork, established research dossiers, a separate journal and printable assets. Preserve and improve them.

> **PRIVACY POLICY:** Never commit, upload, summarize, scan, inspect, or test against real personal entries from `journal/private/` without separate explicit authorization from the owners. Use synthetic fixtures kept outside public release paths. The actual public book must remain completely blank of personal stories and data.

---

## 0. The assignment and success standard

The original project is not a list of icebreakers. It is a large, sophisticated, fun, sometimes sensual, sometimes emotionally demanding collection of experiences for mature, curious partners who already enjoy one another and want to keep discovering each other. It must balance intimacy, knowledge, trust, laughter, affection, unusual games, serious philosophy, novelty, romance and genuine personal growth. It is not a broken-relationship repair manual, a clinical treatment, a productivity tracker, or a compatibility examination. It must also become a **durable recorded memoir of the couple's life together** through date-stamped, private and shared pages, repeat experiences, comparisons over years, photos/keepsake references, milestones and annual memories.

Your output must be a full, tested edition, not a plan for one. Implement every correction below in the canonical source, then regenerate every affected release format. Keep every numbered experience and signature session. No placeholders, partial samples, half-built scaffolding, or 'it should work' claims. A failing or unverified item is a named open item, never silently ticked as done.

**Prior audit findings to close:** (1) variant-aware time discovery; (2) complete `S01`–`S06` signature index and journal parity; (3) a genuinely reusable repeat-session writing packet; (4) a functioning, private, local, owner-populated memoir export; (5) distinct mechanics in similar chapters; (6) more lively editorial variety without losing rigor; (7) real playable rules and genuine user field-testing where possible; (8) meaningful illustration/layout curation and owner visual proof; (9) one accurate, current production status instead of contradictory boards; (10) a stable structured Android-app sync handoff. Also bring accessibility, bibliography, cross-format QA, book/journal linking, game materials and release evidence as close as reasonably possible to total readiness.

The **only prior recommendation intentionally excluded** is reducing size or preparing split/print-platform-specific editions.

---

## 1. Start with a forensic baseline and immutable snapshot

1. Read: `CURSOR_MASTER_WORK_ORDER.md`, `AGENTS.md`, `styles/CHAPTER_CONTRACT.md`, `styles/HOUSE_STYLE.md`, `assets/styles/DESIGN_SYSTEM.md`, `planning/DECISIONS.md`, `planning/STATUS.json`, `review/developmental/MANUSCRIPT_NOTES.md`, `review/QA_AFTER_COPYEDIT.md`, `review/QA_KEY_AND_RASTER.md`, `review/PAGE_RASTER.md`, `release/EXPORT_MANIFEST.md`, `journal/COMPANION_STRUCTURE.md`, `journal/PROMPT_BANK.md`, `print/CARDS_AND_WORKSHEETS.md`, `research/CITATION_WHITELIST.md`, plus the original source catalog. Read the complete *current* tree and history; earlier QA documents are historical snapshots, not necessarily current failures.
2. Record HEAD, branch, clean/dirty working tree, tracked changes, current release hashes, original source-file checksums, chapter/signature counts and complete list of existing generated exports. Never overwrite uncommitted owner edits. Create a dedicated `phase3/book-completion` branch from the verified state (or equivalent safe worktree). Preserve a known-good backup tag/commit and a build manifest. If branch creation isn't available, stop destructive steps, preserve backups, continue only on a safe copy, and report the limitation.
3. Run the existing commands and record stdout/stderr and exit status: `python scripts/audit_sources.py`, `python scripts/build_all.py`, `python scripts/build_journal.py`, `python scripts/build_cards.py`, `python scripts/validate.py`, and any relevant lint/test scripts. If a command is unavailable in the current repo, discover the actual command; do not invent a passing result.
4. Create `planning/phase3/BASELINE.md` with objectively observed issues vs historical issues already fixed. Include hash comparison between `build/` and `release/`. Create a correction tracker `planning/phase3/ACCEPTANCE_MATRIX.md` copied/adapted from the supplied contract, assigning owner, current evidence, state, and final verification path for every item.
5. Read all 108 complete chapters, six signatures, existing cards and journal prompts, the illustrations or rendered proofs, and relevant research briefs through assigned specialists. Inspect project output and its actual files, not only agent summaries. No author self-certifies their own final draft.
6. Keep outputs on disk under the canonical repository. Work on distinct files/worktrees when parallel. Coordinator resolves all merges, re-runs validators after integration, and maintains durable checkpoints at least after each major phase.

**Baseline known from previous audit, not a substitute for fresh verification:** 108 copyedited chapters, 6 copyedited signatures, 13 parts, approximately 245,091 total reported chapter/signature words, 108 chapter motifs, 13 opener drawings, 6 hero artworks, 262-page companion journal, 49-page card/worksheet packet, and a 1,452-page 7 × 10-inch PDF. These are reference numbers; report new numbers after each real build.

---

## 2. Agent orchestra: mandatory delegation and editorial independence

Create or use the specialized subagent profiles supplied in `.cursor/agents/phase3-*.md`. If Cursor's installed agent API changes, use the current supported delegation mechanism. Do not fake parallelism in a single chat; if no subagent capability is available, work in sequential named passes with explicit input/output contracts. **Minimum distinct functional roles:**

- **P3 Executive Producer / Integration Lead:** owns roadmap, branch, task assignment, cross-team handoffs, requirements, final package and honesty of completion claims. Only integrator writes canonical release manifests and tags.
- **P3 Catalog & Navigation Engineer:** audits metadata and implements time-variant-aware book indexes, random selector, signature discovery and exact example/test coverage.
- **P3 Signature Experience Editor:** writes/repairs session-level metadata, bespoke prompts, full signature navigation, session-specific worksheets and intricate long-form experiences.
- **P3 Memoir Experience Architect:** the emotional/storytelling model for both individual and shared journaling, reusable repeat packs and chronology.
- **P3 Private Data & Export Engineer:** creates truly usable local memoir importer/exporter, secure file handling and tests using only fictional fixtures.
- **P3 Developmental Editor:** reads the full collection for overlap, emotional progression, distinct first moves and reader enjoyment; specifies text changes.
- **P3 Play Mechanics Designer:** audits each game, turn sequence, point allocation, hidden information, cards, puzzles, bypasses and repeatability; dry-runs all 114 experiences where appropriate.
- **P3 Relationship Research & Evidence Reviewer:** validates scientific claims in actual papers/source records, stays within evidence limits, distinguishes creative design from research, corrects citations.
- **P3 Intimacy & Consent Editor:** evaluates vulnerable/romantic/sensual exercises for mutual choice, privacy and graceful opt-out, without flattening mature tone.
- **P3 Literary Voice & Copy Editor:** makes the manuscript delightful, adult, warm, specific, humorous where warranted, not formulaic or repetitive; protects substantial prose.
- **P3 Art Director & Illustrator:** inspects page proofs, checks every asset, develops a coherent improvement proposal and fixes weak/problematic art after editorial design sign-off where required.
- **P3 Page Design & Publication Engineer:** produces full 7 × 10 workbook PDF and DOCX, complete EPUB, journal and worksheets; indexes, anchors, print fields and layouts; no page ceiling.
- **P3 Accessibility & Multiformat Auditor:** independently inspects heading structure, navigation, contrast, alt text, font legibility, EPUB keyboard/screen reader, printable rules and exported fields.
- **P3 Structured Book-to-App Export Engineer:** designs/implements stable versioned content packages, changesets, manifest/version migration rules and cross-project handoff.
- **P3 Real-Use QA & Field-Test Coordinator:** creates task-based scripts and test logs for actual readers/players; conducts simulated rule tests but does not falsely report a human couple playtest.
- **P3 Independent Final Auditor:** finds failures, checks evidence rather than assertions, attempts to break exports, does not approve work authored by its own role.

**Role constraints:** No agent invents findings, citations, real memories, survey respondents, approved artwork, completed human tests, or device behavior. Research agents hand off cited constraints and 'what not to claim'; writers deliver revised canonical content and a change log; engineers deliver reproducible code and real generated output; QA delivers command logs and inspected proof evidence. Every workstream names its files and acceptance criteria. The Coordinator may run many independent batches concurrently, but never assign two writers to edit the same source file simultaneously. All automation operates in the foreground while invoked; preserve checkpoints for the next session if interrupted.

Suggested stages: parallel baseline research + catalog analysis + design review; dependent author/editor passes; parallel independent engineering for journal/export and book indexes using disjoint files; final integrated build; separate QA review. Reassign failed work to its owner, then retest with another agent. Do not stop after showing a dashboard of agent plans.

---

## 3. Critical repair A: time-aware discovery that actually works

**Problem:** `scripts/build_all.py` currently groups chapters by a single `time_band` even when their short/standard/extended variants span more shelves. `scripts/surprise_us.py` likewise searches the single primary shelf. Quick 10-minute sessions can be invisible. Signature sessions are omitted from several generated indexes.

**Required architecture:**

1. Normalize duration options for *every* chapter and signature: `variant_id` (`short`, `standard`, `extended`, and any bespoke modes), `display_duration`, `estimated_min_minutes` and `estimated_max_minutes` or explicit `time_category`, `is_calendar_day` / `is_multi_day`, and availability. Use existing YAML fields as input; preserve their human language and the reader's page text. Add metadata as needed, but **do not derive durations from the title or guess an unsupported minute count**.
2. A single experience can appear in *multiple* time shelves; display the applicable version on the index line, e.g. `001 — The Stranger Across From Me (Short, ~10 min)` in Quick Connections, and `001 … (Standard, ~30 min)` under Meaningful Sessions. Link to the correct chapter and, ideally, the variant's subsection/anchor. Do not duplicate whole chapter text or generate bogus extra IDs.
3. Retain the original time shelves: **5–10**, **10–20**, **20–45**, **45–90**, **90–180 minutes**, and **Multi-day/Ongoing**. Add a truthful **Long Day / 3+ hours, single-day** shelf or explicit separate filter so 4-hour and 12-hour experiences do not get mislabeled 'multi-day'. Boundary handling must be documented and consistent (e.g., ten minutes belongs to both adjacent display shelves if the design intentionally supports overlap, otherwise exactly one based on an agreed inclusive/exclusive rule). Different durations do not imply emotional intensity or energy.
4. *Surprise Us* first applies mutually agreed time, energy, emotional-depth ceiling, activity format/mood, and touch preferences. Add variant-aware candidate selection and signature eligibility. Return **activity ID, variant, time estimate, reasons/tags, and safe link/anchor**, not merely a chapter whose *default* session is too long. Preserve the 'no results' outcome; do not silently relax constraints. Optional opt-in relaxation only after explicit selection, and never automatically relax consent/touch/depth ceilings.
5. Ensure `S01`–`S06` appear in their appropriate time, alphabetic/name, mood, energy, depth, type, and revisit indexes. Make the separate signature section identifiable rather than renumbering it as 109–114.
6. Generate the **indexes dynamically** from one canonical normalized catalog consumed by PDF, DOCX, EPUB and any optional offline random tool. Avoid hand-maintaining lists that silently drift.
7. Add automated cases at least for: `001 short ~10`, `017 short ~8`, `043 short ~20`, `071 short ~4 h and standard ~12 h`, `S01 short ~45 and standard ~120`, actual multi-day `032/048/099` as supported, missing extended variant, strict low energy, strict touch=no, no matches. Include report listing *every* variant categorized and invalid/unparsable fields requiring manual editorial correction.
8. Add a readable 'Only have 5 / 10 / 20 / 45 / 90 minutes?' front-of-book quick decision guide, and similar 'We have the afternoon' and 'We have all evening' shortcuts. The six (plus long-day) shelves must be visible from the contents/navigation; PDF/EPUB links must actually resolve.

**Done means:** a genuine ≤10-minute variant of a longer chapter is discoverable in a 10-minute browse, the random selector can choose it, signatures are represented, long single-day plans are not mislabeled multi-day, and every listed variant maps to instructions that exist.

---

## 4. Critical repair B: the six signatures must be first-class experiences

1. Preserve the complete S01–S06 texts, titles, dates/IDs and their distinctive mechanics: `S01 The Long Table`, `S02 The Night With the Lights Low`, `S03 The Case of the Missing Tuesday`, `S04 The Branching Evening`, `S05 The Capsule We Open Later`, `S06 The Long Toast`.
2. Include signatures in every relevant index, all linked, and provide signature-specific time/depth/energy/type/mood/affection/touch metadata following the same validation rules as chapters.
3. Give **each** signature a substantive, uniquely written `Our Story` flow and companion-journal section containing: dated session and version; **separate equal-length Partner A and Partner B** prompts appropriate to the actual mechanics; **Shared Narrative**; **Revisit / Then vs Now**; optional keepsake; explicit continuation pages; at least the same handwriting baseline/minimum as ordinary chapters. Don't reproduce the same generic journal prompt six times.
4. Supply signature-specific printable play components if any require them: card layouts, sealed prompts, answer concealment, branching trees, mystery facilitator key on separate pages, time capsule envelopes/labels, toast cards and staging instructions. Verify that players cannot accidentally see mystery solutions when playing.
5. Cross-reference signatures from the journal companion and printable packet with stable S IDs; add reusable blank signature revisit sheets, with date and attempt fields.
6. Test all signature instructions on paper using two distinct participants/role simulations. For S03 and S04, trace every branch and confirm game-state/answer correctness; do not substitute algorithmic solubility for actual human comprehension.

**Done means:** a reader finding a signature by mood or time can conduct it using real included materials and record an equivalent-quality full memoir of that experience.

---

## 5. Critical repair C: a *usable* repeatable memoir, not merely templates

**Intent:** Years from now, readers can open the book and see not only which activities they did but what each person thought, how they changed, and the memories they chose to save. This must work for a first sitting, a twentieth revisit, a two-day experiment, or a special occasion.

### A. Expand and publish repeatable blank pages

- Produce a **self-contained, print-ready + editable** `Our_Story_Repeatable_Session_Pack_v1.pdf` and `.docx` (or more descriptive filename), with an unlimited-copy blank session cover, individually private equal Partner A and B pages, shared session, revisit/then-now, chronology index, milestone, photo/keepsake caption, annual reflection, and optional add-on pages for special activities.
- Include ID (001–108, S01–S06 or custom milestone), title, date, time, place, attempt number, chosen variant, session status, initials, optional private/shared flags, notes, photo/memento pointers. Make information findable both chronologically and by activity; include a short guide for physically filing repeat visits.
- Prompts should reflect the activity, not force the same 'how did you feel?' on every page. For generic printable repeat sheets, allow readers to copy activity-specific questions or follow an included prompt reference. Preserve personal narrative space instead of reducing the memoir to checkboxes, numeric ratings or compatibility scores.
- Printed writing lines must be genuine, legible and sufficiently spaced. Carry forward 0.32-inch minimum baseline separation and 8+ lines under a full narrative prompt; generate continuation sheets instead of shrinking or crowding pages. Provide a generous inner gutter and tangible examples using clearly fictional characters or blank fields.
- Do not manufacture private answers. Two personal pages belong to equal partners, and a shared page contains only mutually chosen shared writing. A missing response, altered prompt, skipped activity or early stop counts as a legitimate record.

### B. Implement an actual private, offline, user-populated memoir export

- Add documented **local-only** tooling (`scripts/export_private_memoir.py` + test suites, or equivalently named real entrypoint) that accepts actual user-entered sessions using a stable supported format (Markdown/JSON/YAML and documented import semantics). Prefer compatibility with `journal/COMPANION_STRUCTURE.md`'s `our-story-session/1` schema; version/change the schema explicitly if needed.
- Offer at minimum: (i) **shared-only keepsake** containing only owner-approved shared records; (ii) one named participant's own pages plus eligible shared pages; (iii) optional combined full private copy only when each person's inclusion is explicitly authorized. Preserve all attempts; sort chronologically, group by activity if selected; link index, date and ID; include optional milestone and memento captions, and handle missing files gracefully. Avoid silently combining Partner A/B private answers.
- Render actual, readable **private DOCX and PDF**, with a clear versioned export filename, embedded permitted local memento images when requested, and a contents/chronology. Support blank/missing optional fields, duplicate-date sessions, multiple variants, session histories and future ID additions. Do not fabricate text, overwrite originals or pull in public sample stories as if they happened.
- **Strict privacy:** `journal/private/` and all private exports stay ignored by Git. No network calls from export logic, no telemetry, no web fonts, no third-party API/TTS/uploads, no reliance on cloud conversion. Validate every path to prevent writing to tracked source/release or importing files outside authorized private scope; reject symlinks escaping it; use temp files and atomic writes; do not print private text in command logs. Explicitly reject packaging into `release/`. Document threat limitations of raw local files without advertising nonexistent encryption.
- Use **fictional synthetic test data only**, stored in a disposable test fixture, to prove the three export modes, isolation, order, cross-links, repeats, then-now, blank sessions, missing media, image attachment, special S IDs, and no leakage to public book/commit. Private tests must run without accessing real owner journals.
- Align the IDs and revision semantics with the Android handoff in §10. Exports must never rewrite old answers merely because a question is updated in the canonical book.

**Done means:** given four fictional sessions and two fictional partners with distinct privacy settings, the tool actually outputs the correct readable private documents and excludes private pages from the shared document, while the public release remains blank.

---

## 6. Critical repair D: distinct mechanics and a varied literary experience

### Developmental contrast pass

Read the developmental notes, reread all flagged pairs and nearby chapters in sequence, and produce a structured **contrast matrix**: premise; unique first move; actual steps; emotional/social payoff; differences from neighbors; overlap risk; concrete revision required; resulting proof. Never delete/merge/renumber an existing ID without explicit owner direction. Revise the experience itself when necessary—not merely the teaser.

Minimum mandatory comparisons:

- `001/005/081`: stranger roleplay vs novel-question design vs secret question box.
- `041/107`: two-truths guessing vs story with one meaningful smuggled detail.
- `039/046`: romantic re-meeting vs collaborative alternate-universe caper.
- `006/102`: life museum vs never-said museum with two exhibit labels.
- `025/028/057/029`: observed love gestures vs personal operating manual vs bad-day instructions vs reassurance menu.
- `026/074/078/105/030`: appreciation rounds, unnoticed moments, unspoken thanks, compliment decoding, receiving practice.
- `010/052/087/097`: fear under fear, belief under belief, recursive questions, emotional archaeology.
- `009/020/013/016`: vulnerability confession, listening mechanics, chosen disclosure, dropping defensive performance.
- `017/018/019`: mutual gaze, gesture-only communication, shared breathing.
- `032/048/099`: devotion, missions, invisible postcards.
- `043/101`: current/older assumptions vs reasoning from the other person's mind.
- `089/104`: relationship charter vs imagined civilization stressed by events.
- `055/093/050/091`: personal lifetime goals vs joint absurd bucket list vs meaning-in-life scenes vs more of the present.
- `027/076/033`: first strong feelings vs changed portrait vs attraction interview.
- `031/090/098/S05`: future love letter, future memory, centenarian interview, time capsule.
- Whole Part 10 `073`–`080`: make eight distinct memoir tools rather than eight variants of 'tell our story.'

For each cluster, give each exercise **clearly differentiated rules, materials, example and final artifact**. If two are still functionally identical, redesign one while retaining its original central premise; the revised game must remain playable.

### Voice and editorial diversity

The manuscript should feel like a good book written for adults with intelligence, humor, curiosity, affection and a little mischief—not 114 repeated therapy worksheets. Keep essential information discoverable, but vary presentation appropriately: a mystery chapter can feel like a case file; a playful couples quiz can read like game-night instructions; a letter exercise can begin with an evocative invitation; a deep disclosure activity can be quieter and more literary; a sensory date should guide space and choices clearly. Keep stable **machine-readable semantic section IDs** so the app/book tooling doesn't break, even when print-facing section labels or narrative rhythm vary.

- Remove repeated boilerplate metaphors (familiarity/clerk/files/coffee) where they appear mechanically. Vary setting, stakes, rhythm, humor, sentence shape, question architecture and examples. The fictional pair Rowan and Vale can remain where useful, but avoid using the same fictional pair in all chapters; use alternative clearly labeled fictional arrangements, mini-dialogues, direct second-person instruction, or no example characters when the mechanics speak for themselves. **Do not insert real anecdotes about Clifford and Erica without a specific supplied source and permission.**
- Maintain depth; do not slash word counts to create style variety. The existing manuscript is extensive on purpose. Rewrite only to clarify, enrich, or differentiate. A complex game may grow longer, and a romantic/introspective chapter may retain generous prose.
- Ensure each exercise tells readers **why, how, what could go wrong, how to adapt, how to close, and what to remember**; reduce repetitive advice where it distracts but never remove essential consent/choice requirements.
- Run rigorous line/copy/proof passes on **all 108 chapters, six signatures, 13 part introductions, front matter, indexes, game sheets and both memoir editions**. Proofreader must resolve actual typos, mechanical ambiguities, point inconsistencies, mismatched card counts and source notes, not simply mark documents 'copyedited'. Keep per-file change logs, independent review signoff, and word-count impact report.
- Validate claims with primary research or rigorous secondary verification. Clearly label custom inventions as original formulations without claiming absolute global novelty. Recheck source title/author/year/DOI/interpretation and limits. No bogus percentages or causal claims. Where relevant distinguish empirical research, practitioner framework, adaptation and pure game design.
- Maintain mutual consent, autonomy, the right to skip/pass, privacy of written answers and open-minded mature sensuality. Avoid treating a written 'yes' or game score as standing consent to any physical act. Do not turn the book into a repetitive warning pamphlet; write clear human prose.

**Done means:** readers can tell closely related activities apart from the first page and actual rules, the different sections have their own personality, no missing instructions remain, and full editorial/proof records support the final texts.

---

## 7. Critical repair E: graphics, visual quality and format usability

The established *Night Library* design system (midnight/parchment/copper/teal/burgundy, line-art motifs) is coherent and worth protecting; **do not arbitrarily replace it with glossy stock-photo romance graphics or a new color palette**. But 'every SVG file exists' is not the same as 'the book looks finished.'

1. Build a **visual approval kit** with actual rendered page screenshots/contact sheets: front and back covers, complete contents, all 13 part openers, 24+ representative chapter openings including each distinct part and all complex game/romance/letter/puzzle types, all 6 signature openings, writing spreads, index samples, special cards, research/endmatter, and corresponding DOCX/EPUB reading views. Provide high enough resolution to judge legibility and composition, not a microscopic montage. Label IDs and PDF page numbers.
2. Art director reviews *all* 108 motif files, 13 part openers, 6 hero pieces, and covers for actual relevance, professional finish, visual variety, line weights, adequate contrast, consistent print scale, meaningful alt text, rights/originality and rendering quality. Create `review/phase3/ART_AUDIT.md` with `keep`, `improve`, `replace` decisions. Make technical fixes immediately; for major creative direction changes, show a limited proposal and retain the current style until owner approval. Do not block all other work while approval is pending.
3. Repair awkward layouts: visual hierarchy, section differentiation, folios, heads, orphan/widow control, pages accidentally dominated by emptiness, unintentionally split game rules, keys exposed beside player instructions, crowded journal fields, art scale inconsistencies, low-contrast instructional type, and awkward blank pages. **Do not reduce size or writable space to shrink page count.** Correct margins/inside gutter as actually needed for readability on-screen and on printed pages; keep 7 × 10 workbook and generous letter-sized journal.
4. Preserve/edit vector SVG source files in repo. High-resolution PNG for DOCX is permitted and already supported; regenerate with actual correct sizes and consistent interpolation rather than embedding raw SVG paths as text. PDF/EPUB must contain real art, not filenames. Inspect at normal reading zoom and at full print trim.
5. Page-raster all current PDF pages at print-appropriate resolution; run automated blank/clipping/margin/text bounding-box checks, then actual targeted visual inspection covering beginning/end, every part/signature, all high-risk layouts and all automated flags. **Do not assert that a human visually read 1,452 pages if only automation scanned them.** Record automated coverage and manually inspected page ranges separately; archive review images or an actionable manifest.
6. Build and validate an accessible EPUB (navigation, semantic headings, correct order, image descriptions, no critical color-only signals, resizable text and reflow; keyboard and screen reader exercise where possible). Validate table-of-contents links in PDF and EPUB. Validate DOCX all embedded art, actual editable paragraphs/tables and reasonable compatibility, not just zip integrity.
7. Implement or validate print/handwriting materials. Any game that requires pieces must have them in the packet with consistent rules, player instructions separated from solution keys, usable cut dimensions and robust color/grayscale legibility. Puzzle answer keys begin on clearly separate pages and are marked to keep covered.
8. Keep the expansive full workbook and generous journal materials. If book grows from 1,452 to 1,650 pages, that is not a failure. Correctness and pleasure of use beat arbitrary trim.

**Done means:** an owner-reviewable visual kit, no material rendering/legibility problems in inspected/rastered evidence, correct complete art in all editions, consistent graphic identity, and accurate transparent QA records.

---

## 8. Critical repair F: independent practical game/playability verification

A test that verifies chapter headings is not a test that an actual couple can play the activity. Build `review/phase3/PLAYABILITY_MATRIX.csv` covering all 108 + S01–S06, classifying each type (conversation, roleplay, writing, physical presence, sensory, cooperative puzzle, card game, multi-day, signature). For every experience inspect: objective, setup, materials, clear start, turn order, question source, consent/pause, role swap, end condition, short/standard/extended variants, replay logic, journaling handoff and estimated time.

- **Automated or synthetic desk tests:** Walk every game mechanism to completion using fictional answers and test edge cases—empty pile, disagreement, ties, a pass, early stop, repeated game, impossible grid, missing printed card, conflicting instructions. For 043 trace concealed-answer and scoring/marks. For 103 actually solve the published starter independently from the player packets; run spoiler separation checks. For 104 exhaust event-card counts and charter response logic. For 106 prove allocations total 100, zeros work, and negotiated result isn't mistaken for obligation. For S01–S06 trace every branch, cue, time allocation and printable.
- **Representative hands-on field test kit:** Prepare one-page executable scripts for 001, 017, 034, 043, 071, 097, 103, 104, 106, 108, S01, S03 and S04. Include time estimate, exact materials, what to observe, 'where did you get stuck?', 'what did you remember?', and improvement notes. Some sessions are long and need a date/time window; don't claim they were completed if no human test occurred.
- **Actual human test** is a separate, explicit gate: seek feedback from the owner and a consenting second participant when available. No simulated actors may be described as real players. Do not solicit intimate responses into public Git, analytics or bug reports; gather *usability feedback*, not real answers. Provide fillable/offline feedback forms or blank printouts, with an option to report only whether a session was easy/fun/confusing. Owner can choose which activities to try before approval.
- Revise rules and printed materials using the findings; rerun synthetic tests and log improvements. A genuinely unavoidable pending human test must be documented as `AWAITING_OWNER_REAL_USE`, not misreported as passed. The book can reach an **owner-review-ready release candidate** without falsifying human evidence.

---

## 9. Critical repair G: single authoritative production state

Old repo state artifacts contradict each other: `planning/PRODUCTION_BOARD.md` has 'unstarted', while `planning/STATUS.json` reports every chapter/signature `copyedited`; dated QA refers to earlier PDF sizes. Preserve old reports in a historical archive or label them explicitly **superseded**. Replace the owner-facing status with one true current report:

- `planning/CURRENT_RELEASE_STATUS.md`: branch/HEAD, version, export build timestamp, canonical source checksums, counts and word estimates, exact output names, sizes, hashes, PDF page sizes/counts, images, QA suites run, editor states, last fully checked item, open gates, outstanding owner approvals, and **what changes if a future book revision is imported into the app**.
- `planning/phase3/CHAPTER_PROGRESS.csv` or schema-backed JSON with 001–108 and S01–S06, concrete status `research_verified`, `developmentally_edited`, `line_edited`, `mechanically_validated`, `illustrated`, `journal_ready`, `exported`, `QA_passed`, and `owner_approved` with supporting evidence paths; no mass-updating all entries to passed without checks.
- `release/EXPORT_MANIFEST.md` must match *this build* byte-for-byte, listing all releases including new repeat session packet, and distinguishing SVG vs PNG images. Provide deterministic source hashes where feasible. Do not claim Chrome's PDF bytes are bit-reproducible if they are not; input source provenance and matched build/release hashes matter.
- Update or archive `planning/PRODUCTION_BOARD.md` so it no longer says things that are plainly outdated. Preserve prior dated QA reports as audit history, add a current independent `review/phase3/FINAL_READINESS_REPORT.md`, and link to authoritative status from `README.md` and `release/HOW_TO_BEGIN.md`.
- Required readiness vocabulary: `DRAFT`, `TECHNICALLY_VALIDATED`, `EDITORIALLY_REVIEWED`, `READY_FOR_OWNER_REVIEW`, `OWNER_APPROVED`, `PUBLICATION_READY`. No owner/real-use approval is inferred from file sizes or automatic tests.

---

## 10. Critical repair H: reliable content handoff to the Android companion

The current Android project consumes book content, and should not need to reconstruct semantics from a rendered PDF every time. Build a **separately generated, versioned structured export** without replacing the human-readable DOCX/PDF/EPUB:

- Output e.g. `release/app_content/The_Closer_Project_Content_<edition>.zip` with schema-versioned `manifest.json`, `activities.json` (or per-ID files), `parts.json`, `signatures.json`, asset files/maps, `journal_prompts.json`, citation/attribution references and migration/change report. Preserve stable activity IDs 001–108 and S01–S06, variant IDs, chronological/journal prompt IDs, link destinations, image hashes, revision identifiers and optional interactive affordances (question decks, grids, timers, choices, concealed answers). **Do not drop details that the digital version needs to render a complete session.**
- Each activity requires a persistent ID, semantic section keys, fully rendered display content as structured rich text/HTML/Markdown, variant metadata, discoverability fields, related activities, artwork alt text and content hash. Prompts need stable IDs independent of display wording; changed prompt text must not rewrite old user answers. Each serialized object has a schema/revision version.
- Produce a **machine-readable diff** between prior and current bundle: added/removed/changed sections, artwork, assets, activity metadata, variants and journal prompts. Deleted or renamed content must have explicit redirect/tombstone mapping for historical records and import validation. The book never silently destroys app data or assumes existing app data can be overwritten.
- The versioned bundle contains **public editorial content only**, never private journals, real names, any couple's histories, or device-specific secrets. Separate editorial sync from app binary deploy; changes requiring new UI mechanics should be flagged as code updates rather than silently omitted.
- Write sample importer notes and compatibility tests: unchanged IDs preserve existing dated visits, old journal text and photos; renamed chapter links resolve; changed artwork refreshes without touching memory; old schema either migrates or fails safely with a clear message and unchanged app storage.
- Provide `release/app_content/APP_UPDATE_HANDOFF.md` with one simple repeatable instruction for Cursor in the Android repo: identify latest verified bundle, compare manifest, import changed content/assets, implement UI mechanics only when needed, validate, produce updated app, and preserve memoir history. **Do not directly change the Android repo or reinstall anything as part of this book completion phase.**

---

## 11. Reader experience and finishing details

Do a dedicated walkthrough as readers, not just engineers. Cover: starting tonight in 5 minutes, choosing a deep experience, using no/touch boundaries, understanding time variants, preparing game pieces, using 'Surprise Us', recording two private pages and one shared, repeating after months, finding old entries by ID/date, doing a signature, writing a long letter, storing a memento, printing more pages, filling the editable DOCX, assembling a local private keepsake, and handing a new edition to Android. The book should explain all of these actions in friendly, precise adult language.

Check these deliverables rather than assuming their current form is complete: half-title, title, introductory manifesto, philosophy, how-to, navigation, privacy/choice, 13 intros, 108 complete activities, 6 full signatures, special game mechanics, relevant printable packets, 108+6 individual journal prompts, repeat pack, chronology, annual recap, closing essay, comprehensive references, searchable indexes, art sources and meaningful alt text, EPUB metadata, colophon, release manifest, app-content bundle, QA and owner review kit. Keep sample character names explicitly fictional and no unattributed borrowed text.

**Accessibility and physical usability:** If screen readers are not available on the current machine, do static semantic checks and mark screen-reader use unverified pending owner/tool access. Do not claim a full accessibility pass based solely on good color contrast. If actual printouts are unavailable, provide print-proof instructions with known measurement targets and clearly distinguish digital proof from real printed proof. No external print-platform restrictions apply.

---

## 12. The build/test/release pipeline and concrete acceptance gates

### Proposed workflow (run to completion, checkpoint after each)

**Phase A — forensic baseline + safe branch:** verify status and source counts, snapshot hash, build existing outputs; publish baseline/acceptance tracker.  
**Phase B — parallel specialist audits:** catalog/index variants, signature/journal gaps, overlap/developmental notes, full artwork audit, research and mechanics; produce actionable prioritized findings.  
**Phase C — code/metadata repair:** variant-aware index and Surprise Us, include S IDs, correct long single-day classification, normalized machine-readable data, repeat-journal and local exporter with privacy tests.  
**Phase D — editorial pass:** revise overlapping activities, strengthen distinct mechanics, varied voice, line edit entire book and worksheets, sign off citation claims and consent; revise art/layout where needed.  
**Phase E — complete journal/signatures:** bespoke S prompts, companion sections, repeat pack, reliable chronology/milestones, private synthetic export.  
**Phase F — assets/layout/reader:** review all art, create sample proofs, adjust user-facing layout, build current full book/Journals/worksheets, regenerate index/link map and EPUB.  
**Phase G — functional tests + playability:** run all build/unit/schema/privacy tests, role-simulate all 114, solve puzzles independently, build human test kit, scan page rasters, validate key print samples and EPUB navigation.  
**Phase H — Android sync + final assembly:** versioned content manifest/diff package; regenerate/reconcile ALL outputs; independent reviewer retests from clean checkout; verify no real private content in public artifacts.  
**Phase I — candidate release:** produce current status/owner review bundle, hashes/page counts, marked blockers, Git checkpoint + approved remote backup, clear next actions for owner signoff.

### Acceptance gates — ALL must have recorded evidence

**G01** Exactly 108 existing chapter IDs and 6 independent signatures, no loss of original catalog, correct 13 parts.  
**G02** Every chapter/signature retains full mature prose, research limits, readable playable instructions, and usable short/standard/extended variants **where they exist**.  
**G03** Time shelves and Surprise Us use variant metadata; verified edge/boundary tests, signatures, long-day handling and strict filters.  
**G04** All 6 signatures are available across indexes, journals, materials and replays.  
**G05** Every 114 experience has specific private/shared/revisit prompts; both partner pages equal dignity/space.  
**G06** Standalone repeat-session printable/editable packet actually exists and is tested for handwriting usability.  
**G07** Offline private populated-memoir exporter actually runs with fictional fixtures and produces privacy-correct PDFs and DOCXes.  
**G08** Every overlap cluster has an effective distinct game/experience mechanism and logged before/after proof.  
**G09** Every chapter and front/back matter gets substantive editorial/proof pass; no mechanical inconsistencies, fabricated evidence, copied protected texts, or repeated bland boilerplate left unexamined.  
**G10** All existing original assets integrated; owner visual approval kit created; technical art QA and layout evidence present; major restyle requires owner approval.  
**G11** Printable rules, decks, grids, solution keys and worksheets are complete; no exposed spoilers in player packet.  
**G12** Every production format (full PDF, editable DOCX, EPUB, companion PDF/DOCX, printables, repeat pack) is generated, opens/validates, and matches manifest.  
**G13** Accurate full-page automated layout scan, independent representative visual sample and honest notes on unverified human print proof.  
**G14** Accessible structured navigation, links, alt text, contrast and reading/print checks; unsupported real assistive-tech test tracked, not falsely passed.  
**G15** Desk-test evidence for all 114; 13 representative two-person field test scripts; real human runs only marked passed after real participant feedback.  
**G16** Authoritative current status correct; stale board corrected; old QA reports clearly historical.  
**G17** Versioned app-content package and diff/migration tests, no private data; future book updates can be provided as one verified package.  
**G18** Git branch/checkpoint and sanitized public release, no real private data leakage; deliverable inventory and current hashes match.  
**G19** No size reduction, splitting, abridgment, format downscaling, or Amazon-specific edition.  
**G20** Owner sign-off items are explicitly presented and not falsely recorded as done.

### Definition of an acceptable final response from Cursor

Produce a concise, evidence-backed table with each G01–G20 gate (`PASS`, `FAIL`, `PENDING OWNER`, or `NOT VERIFIABLE IN THIS ENVIRONMENT`), links to tests/artifacts, exact export names and current path, counts, current source commit/hash, page count/word count, and what changed from the initial snapshot. Provide an easy-to-open `release/OWNER_REVIEW_START_HERE.md` with proof page gallery, a few suggested first activities and journal workflow. Include a readable list of any unresolved owner decisions and actual external blockers. No claim of absolute publication readiness until required signoffs happen. It is acceptable and expected to finish all engineering and editorial implementation, then mark owner art approval, owner prose approval and real couple playtest as awaiting real human input if they have not happened.

**No stopping at a work plan, a dozen sample chapters, a simulated book, or a successful HTML build.** Work through the whole current project, checkpoint as needed, and create a ready-for-owner-review master edition that is as close to final as tools and user-owned approvals permit.

---

## 13. Source and priority rules when this brief intersects older documentation

1. User-established scope and this Phase 3 brief override older suggestions to shorten/split for retail platforms. Keep all content.  
2. Preserve prior locked decisions unless they conflict with a verified usability defect or specific Phase 3 requirement; document decisions before intentional changes.  
3. The catalog ID/title/premise is stable; creative presentation can improve. The source document and actual published pages take precedence over stale production-board labels.  
4. Book privacy always wins over a convenience build; never copy actual partner notes into public repo/release.  
5. A scientifically credible but boring exercise is not done; a beautifully written but unplayable exercise is not done; an illustrated book with broken indexes or no usable memoir is not done. All dimensions matter.  
6. Owner approval is a real milestone, not something an AI editor grants itself.  
7. If constrained by limits, favor preserving complete work on disk, marking exact remaining gates and enabling safe resumption over announcing success prematurely.

**END OF BINDING WORK ORDER.**
