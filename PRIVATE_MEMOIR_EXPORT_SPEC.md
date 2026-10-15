# Our Story — completed private memoir workflow contract

**Goal:** An offline, local, real working workflow that transforms readers' own notes into a *personal book of their relationship* without ever injecting private material into public Git/release or implying either partner must share their private entries.

## Data model

Prefer documented `our-story-session/1` compatibility, then version if additional fields are necessary. Each session has stable `session_id` (UUID or stable generated local ID), `activity_id` (001–108, S01–S06, milestone or annual), `content_revision`, `attempt`, local date/time, variant, optional place, selected partners, completion/paused/declined state, private-partner markdown, shared markdown, ordered prompt-answer records with stable prompt IDs, optional personal keepsake filenames, and share flags. The model is not a productivity score.

Keep structured metadata and the text bodies separate, with local filenames within private scope. Store a historical snapshot of prompt wording/question ID used at time of answer when useful, so future rewrites don't falsify the old answer. All years and attempts remain intact. If the owner redoes #001 in ten years, nothing gets overwritten.

## Exports

- `shared` — only shared entries and explicitly marked individual excerpts; never read other content into the generated output.
- `partner-a` / `partner-b` — that participant's private record + shared entries + specifically authorized excerpts from the other person (default none).
- `full-private` — only after each participant's explicit inclusion permission; stored locally for their authorized personal archive, never public.

Outputs: actually generated, editable DOCX and readable PDF, with date and ID navigation, title page, chronology, individual activity groupings or chronological ordering as requested, text correctly attributed, meaningful image captions, multiple visits and annual recap. For a confidential export, append `_PRIVATE_MEMOIR_` to the filename, place only under approved gitignored `journal/private/exports/`, and never send to an external conversion service. Public blank companion remains independent.

## Negative tests

- Shared export does not contain arbitrary private marker strings from fixture entries.
- One participant's export does not contain the other's private marker string.
- `full-private` requires explicit approvals recorded at export invocation.
- A disallowed path to `release/`, `build/`, repo root, symlink escape or `../` traversal is rejected.
- Real notes are never needed for tests; mock ones use names like `Participant A` and `Participant B` with conspicuous **FICTIONAL** markers.
- Error and success logs show file paths/counts, not private paragraphs.
- Public release and git status do not pick up any fixture/private export content; nonprivate test fixture stays safely separated.
- Overwrites, collisions, corrupt metadata, missing image or missing prompt are handled without silent data loss.

## Owner usability

Provide simple instructions: 'Make a dated journal entry', 'Make a shared entry', 'Make a revisit', 'Attach a keepsake', 'Export the shared keepsake', 'Export my own pages', 'Keep both histories across a book update'. Demonstrate **exact real CLI commands and resulting output paths** using fictional fixture data; don't only document design architecture.
