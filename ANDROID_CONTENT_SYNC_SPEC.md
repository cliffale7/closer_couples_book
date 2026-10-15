# Book-to-Android versioned export contract

The book repository is editorial source of truth. This task builds the **public content export**, not a new Android application. The existing app must keep its local journals separately.

## Must be in each release bundle

- `manifest.json`: `schema_version`, `book_edition`, `build_timestamp`, `source_commit`, `release_id`, per-file SHA-256, list of 108 IDs + six signature IDs, asset hashes, provenance and compatibility notes.
- `parts.json`: thirteen parts, titles, order, chapter IDs, introductions, opener art refs.
- `activities/*.json` or `activities.json`: immutable ID, current title and slug, classified research vs original, section texts/semantic keys, variant durations in minutes and labels, actual eligible time shelves, energy/mood/intensity/format/touch metadata, materials, session steps, diagrams and asset refs, prompt references, cross-links, revision and content hashes.
- `signatures/*.json`: same core contract for S01–S06, with full session structures and any handout/hidden facilitator separation.
- `prompts/*.json`: stable prompt IDs (not question text hashes), prompt version, activity ID, intended partner seat/shared/revisit/private status, text, optional alternative prompts and introduced/deprecated version IDs.
- `assets/`: original artwork or sanitized compatible rendered variants with stable ID, MIME type, dimensions and alt text; no remote dependency needed for offline use.
- `interactive/`: explicit schema for card sets, player-visible/hidden content, score rules, story branches, timers or puzzle constraints where applicable. Note when an experience is narrative-only, rather than promising nonexisting mechanics.
- `REFERENCES.md`, `CHANGES.json`, `APP_UPDATE_HANDOFF.md`.

## Revision behaviors to verify

1. No-op bundle import touches no app journal entries.
2. Changed prose updates reader content, not journal answer text.
3. Changed prompt preserves old prompt ID for existing answers with old wording snapshot; new prompt ID only when meaning materially changes, migration mapping explicit.
4. Removed/renamed activity retains tombstone/alias for prior histories; stable IDs if possible.
5. Changed illustration refreshes asset but does not touch visit/photos.
6. Changed mechanics requiring new app code are labeled `requires_app_update`, never silently rendered as a broken narrative.
7. New bundle schema incompatible with installed app fails safely, leaving the old good bundle and all journals usable.
8. Manifest comparison and content hashes identify exact changed chapters/files.
9. No private notes, sample couple-specific stories, personally identifying data or owner-only graphics accidentally included.

## Desired owner's repeat workflow

Drop approved updated book release/content ZIP into Android project's designated inbox (to be defined there); ask Cursor to run the app-import update work order. That project's agents compare manifests, migrate content/assets/interactive UI as necessary, validate offline session/journaling behavior, produce update and preserve all historical records. **Book project supplies ready-to-ingest public data; Android project handles installed app state.**
