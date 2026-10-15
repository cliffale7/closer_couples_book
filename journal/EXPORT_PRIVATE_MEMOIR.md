# Export a private Our Story

This runs on your computer. It does not upload anything. It reads a folder of sessions and writes a PDF and a Word file whose names contain `PRIVATE_MEMOIR`. Those names are ignored by Git.

A session folder looks like this:

```text
journal/private/sessions/2026-04-03-001-attempt-1/
  session.yaml
  partner-a.md
  partner-b.md
  shared.md
  mementos.yaml
```

`session.yaml` uses schema `our-story-session/1`. Story text stays in the markdown files. Set `share.partner_a` and `share.partner_b` to `private` or `shared`. The shared page is included when `share.shared` is `shared`.

A field with no visibility is private. Put an explicit mark in `field_visibility` when a date, title, place, time, version, or status may appear in a shared export:

```yaml
field_visibility:
  date: shared
  title: partner_a
  place: partner_b
```

Each keepsake needs its own `visibility`: `shared`, `partner_a`, or `partner_b`. An old keepsake with no mark stays private. A shared paragraph in the same session does not make the photo shared. The export writes a count of unmarked keepsakes and does not list their captions.

Prompt lines need a seat. `001.partner_a.1` follows that seat. A prompt with no seat and no `visibility` stays out of the shared export and out of the other person's export. It is included only in the full private file.

Commands, from the book folder:

```text
python scripts/export_private_memoir.py --private-root journal/private --mode shared
python scripts/export_private_memoir.py --private-root journal/private --mode partner-a
python scripts/export_private_memoir.py --private-root journal/private --mode partner-b
python scripts/export_private_memoir.py --private-root journal/private --mode full-private --authorize-partner-a --authorize-partner-b
```

The shared file contains only pages, prompts, captions, and photos marked shared. Partner A's file contains Partner A's private pages, shared pages, and anything Partner B explicitly marked shared. It does not contain Partner B's unshared prose, prompts, titles, or photos. The full private file needs both of these local notes, plus both flags on the command:

```text
journal/private/authorizations/partner-a.yaml
journal/private/authorizations/partner-b.yaml
```

```yaml
schema: our-story-export-authorization/1
person: partner-a
scope: full-private
granted: true
date: 2026-10-14
```

Use `partner-b` in that person's file. The flags confirm that the person at the keyboard intends the export. They are not proof that both people agreed, and this tool does not verify identity. The files are ordinary documents on this computer. They are not encrypted.

Files land in `journal/private/exports/`. The tool will not overwrite an export that is already there. A later book revision does not rewrite these files. Each session can store the prompt id and the wording that was on the page when you answered.

The tool refuses to write into `release/` or `build/`, refuses a file path that leaves the private root, and refuses a duplicate session id. It prints counts and paths, not the text you wrote.
