# -*- coding: utf-8 -*-
"""Copy accepted batch-01 paintings and point those chapters at them."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(r"C:\Users\cliff\.cursor\projects\c-Users-cliff-cursor-The-Closer-Project-Android-Cursor-Package\assets")
ACCEPTED = ["002", "003", "004", "005", "006", "007", "008"]
SOURCES = {"007": "ch-007b.jpg"}

for number in ACCEPTED:
    src = SRC / SOURCES.get(number, f"ch-{number}.jpg")
    dest = ROOT / "assets" / "chapters" / number / "illustration.jpg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    review = ROOT / "assets" / "illustrations" / "phase4" / "review" / f"{number}-accepted.jpg"
    review.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, review)
    print("copied", number, dest.stat().st_size)

for path in (ROOT / "chapters").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        continue
    head, rest = text.split("---", 2)[1:]
    for number in ACCEPTED:
        if f'id: "{number}"' not in head:
            continue
        old = f'assets/chapters/{number}/motif.svg'
        new = f'assets/chapters/{number}/illustration.jpg'
        if old not in head:
            raise SystemExit(f"No motif path in {path}")
        path.write_text("---" + head.replace(old, new, 1) + "---" + rest, encoding="utf-8")
        print("pointed", path.name)
