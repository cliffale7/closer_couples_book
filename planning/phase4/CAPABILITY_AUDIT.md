# Phase 4 capability audit

Date: 15 October 2026. Branch: `phase4/real-illustrations`.

`CURSOR_REAL_ILLUSTRATION_MASTER_WORK_ORDER.md` is not in the book project, the Android project, or the usual document folders. This audit follows the owner's written brief.

## What can actually make a plate

The image tool produces a finished painted JPEG. It does not write SVG paths, icons, or Python shapes. Allowed frames are 1:1, 4:3, 3:4, 16:9, and 9:16. Delivered sizes from the sample run:

| Plate | Frame | Pixels | File |
| --- | --- | --- | --- |
| Cover, rejected costume | 3:4 | 864×1152 | review copy only |
| Cover, accepted | 3:4 | 864×1152 | `assets/covers/cover-front.jpg` |
| Chapter 001 | 16:9 | 1280×720 | `assets/chapters/001/illustration.jpg` |
| Part 1 opener | 16:9 | 1280×720 | `assets/parts/01-opener.jpg` |

A 1280-pixel chapter plate at 5.4 inches wide is about 237 pixels per inch. A 864-pixel cover at 4.4 inches wide is about 196 pixels per inch. Both are real paintings a reader can recognize. Neither is a 300-dpi full-bleed press master. That limit stays in the review notes. It is not a reason to go back to line art.

Output is JPEG, not layered source art. There is no vector redraw and no type inside the picture. Book titles stay in the page layout.

## What must not be used as a plate

`scripts/render_motifs.py` now refuses to run. It only emits the rejected Night Library SVG drawings. Existing SVG files stay on disk so an unpainted slot is not a blank page, and so a painting can be compared with the slot it replaces. A page uses a `.jpg` when that file is present.

## Sample verdicts

Independent review is in `planning/phase4/REVIEW_BATCH_00.md`. The style lock is in `planning/phase4/STYLE.md`.

Approved and placed: front cover, back cover, title image, part openers 01–06, and chapters 001–072. Chapter 007’s first picture was rejected because the path did not split. The second picture is the one in the book.

Rejected: the Victorian cover, and the first chapter 007 path.

## Inventory

108 chapter plates, 13 part openers, 6 signature heroes, front cover, back cover, and title image. Eighty-one are approved. Forty-nine are still the rejected SVG drawings and are not finished art. Counts live in `planning/phase4/ART_INVENTORY.json`.
