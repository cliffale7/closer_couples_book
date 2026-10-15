# Privacy regression

Date: 2026-10-14. Synthetic fixtures only. No real journal was opened.

Command: `python -m unittest scripts.test_phase3_memoir`

Result: 4 tests, OK.

## What the fixtures contain

One private root under a temporary directory. Five fictional sessions. Markers are obvious invented strings, not a couple's notes.

- Private prose for Partner A and Partner B, plus a shared paragraph.
- A historical prompt snapshot on a private Partner A seat (`OLD_PROMPT_WORDING`, `NEW_PROMPT_WORDING`).
- An unmarked keepsake (`toast.png`, caption `UNMARKED_CAPTION_ONLY`). No visibility key.
- One mixed session, S03, with a shared body, a shared prompt, a Partner B prompt, a legacy prompt with no seat, a title marked `partner_a`, a place marked `partner_b`, and a date marked shared.
- Four photos in that mixed session: Partner A, Partner B, shared, and `visibility: nope` (unknown).
- A signature session S01 whose private pages stay private.
- Dates 2020, 2021, 2022, 2023, and 2024, so a later sitting does not replace an earlier one.
- A path that points outside the private root.
- A second full-private run against files that already exist.

## What was checked

Shared, partner-a, and full-private each wrote a DOCX and a PDF. Tests read DOCX `word/document.xml`, counted `word/media` parts, read PDF text with pypdfium2, and counted PDF image objects. Export filenames were checked for the private-memoir mark and for the unmarked caption.

| Export | Private markers and media |
| --- | --- |
| shared | Shared prose, the shared prompt, the shared caption, and one image. No Partner A or Partner B prose, no unmarked caption, no private title or place, no legacy prompt, no unknown-visibility caption. One DOCX media part. One PDF image. |
| partner-a | Partner A prose and prompt, Partner A title and photo, shared prose and photo. No Partner B caption, place, or prompt. No unmarked caption. Two DOCX media parts. Two PDF images. |
| full-private | Refused with only one flag. Refused with both flags and no authorization files. After `authorizations/partner-a.yaml` and `partner-b.yaml` (schema `our-story-export-authorization/1`, `granted: true`, scope `full-private`) plus both flags, the private markers and at least five images were present. A second run refused to overwrite. |

`release/` as a private root is refused. A memento path outside the root is refused. The tool prints counts and paths. The tests do not print caption text to the console as a success log; the exporter's own log is mode, session counts, unmarked-keepsake count, and paths.

## Limits

The authorization files are local notes. The command flags are the operator's confirmation. This is not cryptographic consent and not an identity check. The PDF and DOCX are ordinary files. They are not encrypted. EXIF is not a separate stripper: the fixtures are new PNGs with no camera metadata, and a hidden image is omitted rather than rewritten. A corrupt image raises `SystemExit` with the exception class name only; that path is in the exporter and was not given its own fixture in this run.
