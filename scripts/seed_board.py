"""Create the production board, status file, and art map from catalog plus seeds."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "planning" / "chapter_seeds.tsv"
catalog = json.loads((ROOT / "source" / "experience_catalog.json").read_text(encoding="utf-8"))
items = {e["id"]: e for e in catalog["experiences"]}

rows = []
for line in SEEDS.read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("id"):
        continue
    parts = line.split("|")
    if len(parts) != 5:
        raise SystemExit(f"Bad seed: {line}")
    rows.append(parts)

if [int(r[0]) for r in rows] != list(range(1, 109)):
    raise SystemExit("Seeds must be IDs 001-108 in order")

for folder in (
    "research/dossiers",
    "review/evidence",
    "review/developmental",
    "review/copyedit",
    "journal/templates",
    "journal/private",
    "assets/chapters",
    "assets/parts",
    "assets/covers",
    "assets/signatures",
    "assets/styles",
    "chapters",
    "signature",
    "frontmatter",
    "appendices",
    "build/fixtures",
    "release",
):
    (ROOT / folder).mkdir(parents=True, exist_ok=True)

private_note = ROOT / "journal" / "private" / "DO_NOT_COMMIT.txt"
if not private_note.exists():
    private_note.write_text(
        "Real couple notes stay in this folder. Git ignores it. Do not copy these notes into release exports.\n",
        encoding="utf-8",
    )

art = []
status_chapters = {}
for id_s, classification, sources, motif, near in rows:
    n = int(id_s)
    item = items[n]
    src = [s for s in sources.split(";") if s]
    near_ids = [s for s in near.split(";") if s]
    art.append(
        {
            "id": item["display_id"],
            "title": item["title"],
            "part": item["part_number"],
            "motif": motif,
            "svg": f"assets/chapters/{item['display_id']}/motif.svg",
            "alt": f"Line motif for {item['display_id']} {item['title']}: {motif}",
        }
    )
    status_chapters[item["display_id"]] = {
        "title": item["title"],
        "part": item["part_number"],
        "state": "unstarted",
        "classification_seed": classification,
        "source_hints": src,
        "near_duplicates": near_ids,
        "word_count": 0,
        "artifacts": [],
    }

(ROOT / "assets" / "ART_MAP.json").write_text(
    json.dumps({"system": "Night Library", "chapters": art}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

signatures = {
    "S01": "The Long Table",
    "S02": "The Night With the Lights Low",
    "S03": "The Case of the Missing Tuesday",
    "S04": "The Branching Evening",
    "S05": "The Capsule We Open Later",
    "S06": "The Long Toast",
}
status = {
    "project": "The Closer Project",
    "edition": "v1-draft",
    "updated": "2026-10-14",
    "phase": "1-research-art-layout",
    "source_audit": "pass",
    "chapters": status_chapters,
    "signatures": {k: {"title": v, "state": "unstarted"} for k, v in signatures.items()},
}
(ROOT / "planning" / "STATUS.json").write_text(
    json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8"
)

lines = [
    "# Production board",
    "",
    "Updated 14 October 2026. Phase 1: research, art, and layout are in progress. No chapter is drafted yet. Source audit passed.",
    "",
    "| ID | Title | State |",
    "| --- | --- | --- |",
]
for key, row in status_chapters.items():
    lines.append(f"| {key} | {row['title']} | {row['state']} |")
lines.append("")
lines.append("Signatures S01–S06 are unstarted.")
(ROOT / "planning" / "PRODUCTION_BOARD.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

hints_path = ROOT / "research" / "CHAPTER_HINTS.csv"
with hints_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "classification_seed", "whitelist_hints", "near_duplicates", "premise"])
    for id_s, classification, sources, motif, near in rows:
        item = items[int(id_s)]
        writer.writerow([
            item["display_id"],
            item["title"],
            classification,
            sources,
            near,
            item["source_premise"],
        ])
print(f"Seeded {len(rows)} chapters")
