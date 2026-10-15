# -*- coding: utf-8 -*-
"""Write the Phase 4 plate inventory. Does not draw anything."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART_MAP = ROOT / "assets" / "ART_MAP.json"
OUT = ROOT / "planning" / "phase4" / "ART_INVENTORY.json"

APPROVED = {
    "cover-front": "assets/covers/cover-front.jpg",
    "part-01": "assets/parts/01-opener.jpg",
    "001": "assets/chapters/001/illustration.jpg",
    "002": "assets/chapters/002/illustration.jpg",
    "003": "assets/chapters/003/illustration.jpg",
    "004": "assets/chapters/004/illustration.jpg",
    "005": "assets/chapters/005/illustration.jpg",
    "006": "assets/chapters/006/illustration.jpg",
    "007": "assets/chapters/007/illustration.jpg",
    "008": "assets/chapters/008/illustration.jpg",
    "009": "assets/chapters/009/illustration.jpg",
    "010": "assets/chapters/010/illustration.jpg",
    "011": "assets/chapters/011/illustration.jpg",
    "012": "assets/chapters/012/illustration.jpg",
    "013": "assets/chapters/013/illustration.jpg",
    "014": "assets/chapters/014/illustration.jpg",
    "015": "assets/chapters/015/illustration.jpg",
    "016": "assets/chapters/016/illustration.jpg",
}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    body = text.split("---", 2)[1]
    found: dict[str, str] = {}
    for line in body.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        found[key.strip()] = value.strip().strip('"')
    return found


def main() -> None:
    art = json.loads(ART_MAP.read_text(encoding="utf-8"))
    part_titles: dict[int, str] = {}
    for path in (ROOT / "chapters").rglob("*.md"):
        meta = frontmatter(path)
        if meta.get("part", "").isdigit() and meta.get("part_title"):
            part_titles[int(meta["part"])] = meta["part_title"]
    slots = []

    def add(slot_id: str, kind: str, title: str, scene: str, fallback: str) -> None:
        live = APPROVED.get(slot_id, fallback)
        slots.append(
            {
                "id": slot_id,
                "kind": kind,
                "title": title,
                "scene_seed": scene,
                "live_path": live,
                "status": "approved" if slot_id in APPROVED else "rejected_svg",
            }
        )

    add(
        "cover-front",
        "cover",
        "Front cover",
        "Two contemporary adults at a lamp-lit table at night",
        "assets/covers/cover-front.svg",
    )
    add(
        "cover-back",
        "cover",
        "Back cover",
        "The same table after the conversation, lamp still lit, chairs pushed back",
        "assets/covers/cover-back.svg",
    )
    add(
        "title-page",
        "cover",
        "Title image",
        "A copper lamp, two cups, and an open blank book, with no lettering",
        "assets/covers/title-page.svg",
    )
    for number in range(1, 14):
        add(
            f"part-{number:02d}",
            "part",
            part_titles.get(number, f"Part {number}"),
            "A threshold scene for this part, painted, with no type",
            f"assets/parts/{number:02d}-opener.svg",
        )
    for chapter in art["chapters"]:
        add(
            chapter["id"],
            "chapter",
            chapter["title"],
            chapter["motif"],
            chapter["svg"],
        )
    for path in sorted((ROOT / "signature").glob("S*.md")):
        meta = frontmatter(path)
        slot_id = meta.get("id") or path.name[:3]
        add(
            slot_id,
            "signature",
            meta.get("title", path.stem),
            meta.get("deck", "Signature hero scene"),
            f"assets/signatures/{slot_id}-hero.svg",
        )
    counts: dict[str, int] = {}
    for slot in slots:
        counts[slot["status"]] = counts.get(slot["status"], 0) + 1
    payload = {"style": "lamp-lit table", "counts": counts, "slots": slots}
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(counts, "slots", len(slots))


if __name__ == "__main__":
    main()
