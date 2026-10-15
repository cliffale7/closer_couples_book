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

Commands, from the book folder:

```text
python scripts/export_private_memoir.py --private-root journal/private --mode shared
python scripts/export_private_memoir.py --private-root journal/private --mode partner-a
python scripts/export_private_memoir.py --private-root journal/private --mode partner-b
python scripts/export_private_memoir.py --private-root journal/private --mode full-private --authorize-partner-a --authorize-partner-b
```

The shared file contains only pages marked shared. Partner A's file contains Partner A's pages plus shared pages, and Partner B's pages only when B marked them shared. The full private file is written only when both people are named in the command. Files land in `journal/private/exports/`.

A later book revision does not rewrite these files. Each session can store the prompt id and the wording that was on the page when you answered.

The tool refuses to write into `release/` or `build/`, and it refuses a file path that leaves the private root. It prints counts and paths, not the text you wrote. The files themselves are ordinary documents on this computer. They are not encrypted.
