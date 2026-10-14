# THE CLOSER PROJECT — Cursor Production Starter Package

This ZIP is a ready-to-open starting workspace for building a **complete, illustrated first draft** of the book and its companion shared-memoir journal. It is a work order + source files + machine-readable catalog + project-local agent team, **not the finished book**.

## Get going in Cursor

1. Unzip this archive into its own folder, e.g. `The_Closer_Project/`. Keep the hidden `.cursor/agents/` folder (some unzip programs hide dot-directories).
2. Open that folder in **Cursor** as the workspace/project.
3. Open Agent chat and attach/mention `@CURSOR_MASTER_WORK_ORDER.md` (or paste its entire contents) and say: `Execute this work order, using all supplied source documents and the project subagent team. Begin the source audit and delegate research/art/layout in parallel. Continue building the complete book, with persistent checkpoints.`
4. If Cursor offers a Projects/coordinator workflow on your plan, you can use it; otherwise standard Agent with project-local subagents works. Accept only needed install/tool permissions, and keep an eye on model usage when running many agents.
5. Judge progress from written files, chapter inventory, real compiled PDFs/DOCX/EPUB, journal exports, and the QA report—not a chat claim saying "done." The work is very large and may require multiple resumed agent sessions; the work order requires durable checkpoints.

## Package contents

- `CURSOR_MASTER_WORK_ORDER.md` — complete production brief and acceptance contract.
- `AGENTS.md` — persistent shared project instructions.
- `.cursor/agents/` — 12 focused Cursor subagents ready for use (current syntax uses YAML frontmatter).
- `source/*.docx` — immutable original working manuscript and project-feedback document.
- `source/experience_catalog.json` — machine-readable full inventory of 108 IDs/titles/parts/source descriptions.
- `planning/ORIGINAL_IDEAS_EXPANDED.md` — preserves special mechanics of activities 097–108.
- `scripts/validate_starter.py` — quick validation that the package has the right starting inventory.

## Important editorial distinctions

This project is unrelated to any scavenger hunt. All 108 original items are preserved; new centerpiece sessions get IDs outside 001–108. The book targets mature, fun, open-minded couples and blends the familiar, reinvented and original. It is NOT a book of research-backed clinical claims; sources must be checked and caveated where relevant. Never invent actual real-life journal responses. Private couple notes live outside public release builds and Git history.

## Starting validation

From the project folder, run `python scripts/validate_starter.py` to check the expected source inventory (the script uses Python standard library only).
