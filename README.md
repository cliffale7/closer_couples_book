# The Closer Project

Illustrated workbook and digital reader. The canonical text is Markdown with YAML frontmatter. The original DOCX files in `source/` stay untouched.

The production brief is `CURSOR_MASTER_WORK_ORDER.md`. Orientation for the starter package is in `README_START_HERE.md`. What this draft pipeline does and does not do is in `planning/BUILD_NOTES.md`.

## Build

Install the Python packages, then build and validate:

```bash
python -m pip install -r requirements.txt
python scripts/build_all.py
python scripts/validate.py
```

`python scripts/build_all.py` reads `frontmatter/*.md`, plus `chapters/**/*.md` and `signature/**/*.md` when those files exist. A real chapter that is missing a required heading stops the build before it writes the editions.

To include the typesetting fixture:

```bash
python scripts/build_all.py --proof
```

`--proof` adds `build/fixtures/typesetting-proof.md`. That file is a fake sample titled **FIXTURE NOT A CHAPTER**. It is not catalog entry 001 and it is not one of the six signature sessions.

The build writes:

- `build/workbook.html`
- `build/The_Closer_Project_Illustrated_Workbook_v1_draft.docx`
- `build/The_Closer_Project_Illustrated_Workbook_v1_draft.pdf`
- `build/The_Closer_Project_Reader_v1_draft.epub`

The PDF is printed from the HTML by headless Chrome, then by Edge if Chrome is missing. Pandoc and Typst are not used. `journal/private/` is never read.

## Validate

`python scripts/validate.py` checks that the HTML, DOCX, PDF, and EPUB exist and are non-trivial, that the PDF trim is 7 by 10 inches, and that the EPUB unzip contains `mimetype`, `container.xml`, and nav. It also checks required headings on any real chapter files.
