"""Lock the source inventory: checksums, DOCX text, catalog, and part ranges."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}

EXPECTED = {
    "The_Closer_Project_Concept_and_Feedback_Invitation.docx":
        "8bebf324b4a945a7440a00b5fd4ca714dece7e555a4e3f6c5894381c3758724a",
    "The_Closer_Project_Working_Manuscript_v0.1.docx":
        "48f6d32c94e3b0bac1e6e3df3007203ffae30104dcc03015aa8f2b15de6b821e",
}

PART_RANGES = {
    1: (1, 8, "The Art of Really Knowing Someone"),
    2: (9, 16, "Vulnerability and the Courage to Be Seen"),
    3: (17, 24, "The Science and Experience of Closeness"),
    4: (25, 32, "Love, Affection, and Feeling Chosen"),
    5: (33, 40, "Desire, Attraction, and Sensual Intimacy"),
    6: (41, 48, "Playfulness, Laughter, and a Little Mischief"),
    7: (49, 56, "The Inner World: Dreams, Meaning, and Identity"),
    8: (57, 64, "Trust, Communication, and Emotional Safety"),
    9: (65, 72, "Shared Adventures and New Experiences"),
    10: (73, 80, "The Past, the Present, and the Story of Us"),
    11: (81, 88, "Radical Curiosity and the Surprising Stuff"),
    12: (89, 96, "Building a Closer Future Together"),
    13: (97, 108, "The Inventor’s Workshop: Original Proposals"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def docx_blocks(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    blocks = []
    body = root.find("w:body", NS)
    for child in list(body):
        tag = child.tag.split("}")[-1]
        if tag == "p":
            texts = [t.text or "" for t in child.iter(f"{{{W_NS}}}t")]
            style = child.find("w:pPr/w:pStyle", NS)
            style_val = style.get(f"{{{W_NS}}}val") if style is not None else ""
            blocks.append({"kind": "p", "style": style_val, "text": "".join(texts).strip()})
        elif tag == "tbl":
            rows = []
            for tr in child.iter(f"{{{W_NS}}}tr"):
                cells = []
                for tc in tr.findall("w:tc", NS):
                    bits = [t.text or "" for t in tc.iter(f"{{{W_NS}}}t")]
                    cells.append("".join(bits).strip())
                rows.append(cells)
            blocks.append({"kind": "table", "style": "", "text": " | ".join(" || ".join(r) for r in rows)})
    return blocks


def normalize(s: str) -> str:
    return (
        s.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .strip()
    )


def main() -> None:
    issues: list[str] = []
    checksums = {}
    for name, expected in EXPECTED.items():
        path = SOURCE / name
        if not path.is_file():
            issues.append(f"MISSING {name}")
            continue
        digest = sha256(path)
        checksums[name] = digest
        if digest != expected:
            issues.append(f"CHECKSUM MISMATCH {name}: got {digest}")

    catalog = json.loads((SOURCE / "experience_catalog.json").read_text(encoding="utf-8"))
    items = catalog["experiences"]
    parts = catalog["parts"]
    if len(items) != 108:
        issues.append(f"catalog count {len(items)}")
    ids = [c["id"] for c in items]
    if ids != list(range(1, 109)):
        issues.append("catalog IDs are not 1..108 in order")
    if len(parts) != 13:
        issues.append(f"part count {len(parts)}")

    for part in parts:
        lo, hi, title = PART_RANGES[part["part_number"]]
        if part["ids"] != list(range(lo, hi + 1)):
            issues.append(f"part {part['part_number']} id range mismatch")
        if normalize(part["part_title"]) != normalize(title):
            issues.append(f"part title mismatch {part['part_number']}: {part['part_title']!r}")

    manuscript = SOURCE / "The_Closer_Project_Working_Manuscript_v0.1.docx"
    blocks = docx_blocks(manuscript)
    paragraphs = [b["text"] for b in blocks if b["text"]]
    (ROOT / "planning").mkdir(exist_ok=True)
    (ROOT / "planning" / "manuscript_blocks.json").write_text(
        json.dumps(blocks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    entry_re = re.compile(r"^(\d{3})\.\s+(.+)$")
    found: dict[int, str] = {}
    for text in paragraphs:
        m = entry_re.match(text)
        if m:
            found[int(m.group(1))] = m.group(2).strip()

    if set(found) != set(range(1, 109)):
        missing = sorted(set(range(1, 109)) - set(found))
        extra = sorted(set(found) - set(range(1, 109)))
        issues.append(f"DOCX entry IDs missing={missing} extra={extra} count={len(found)}")

    premises = {}
    # Premise is the next non-empty paragraph after a title that is not an expansion brief.
    # Walk blocks in order.
    current_id = None
    for text in paragraphs:
        m = entry_re.match(text)
        if m:
            current_id = int(m.group(1))
            premises[current_id] = None
            continue
        if current_id and premises.get(current_id) is None:
            if text.lower().startswith("expansion brief") or text.lower().startswith("editorial metadata"):
                continue
            if text.startswith("Part ") or text.startswith("##"):
                continue
            premises[current_id] = text

    title_mismatches = []
    premise_mismatches = []
    for item in items:
        doc_title = found.get(item["id"])
        if doc_title is None:
            continue
        if normalize(doc_title) != normalize(item["title"]):
            title_mismatches.append(
                {"id": item["id"], "docx": doc_title, "catalog": item["title"]}
            )
        doc_premise = premises.get(item["id"]) or ""
        if normalize(doc_premise) != normalize(item["source_premise"]):
            premise_mismatches.append(
                {
                    "id": item["id"],
                    "docx": doc_premise,
                    "catalog": item["source_premise"],
                }
            )

    concept_path = SOURCE / "The_Closer_Project_Concept_and_Feedback_Invitation.docx"
    concept_blocks = docx_blocks(concept_path)
    concept_text = "\n".join(b["text"] for b in concept_blocks if b["text"])
    philosophy_markers = [
        "not designed only for couples in crisis",
        "rotating library",
        "Participation is voluntary",
        "separate established research",
    ]
    missing_markers = [m for m in philosophy_markers if m.lower() not in concept_text.lower()]
    if missing_markers:
        issues.append(f"concept markers missing: {missing_markers}")

    extract = (SOURCE / "Working_Manuscript_Fulltext_Extract.md").read_text(encoding="utf-8")
    extract_ids = [int(m) for m in re.findall(r"^### (\d{3})\. ", extract, flags=re.M)]
    if extract_ids != list(range(1, 109)):
        issues.append(f"markdown extract IDs differ: count={len(extract_ids)} unique={len(set(extract_ids))}")

    expanded = (ROOT / "planning" / "ORIGINAL_IDEAS_EXPANDED.md").read_text(encoding="utf-8")
    expanded_ids = [int(m) for m in re.findall(r"^## (\d{3})\. ", expanded, flags=re.M)]
    if expanded_ids != list(range(97, 109)):
        issues.append(f"expanded ideas IDs {expanded_ids}")

    report = {
        "checksums_match_source_file": all(
            checksums.get(n) == e for n, e in EXPECTED.items()
        ),
        "checksums": checksums,
        "docx_paragraphs": len(paragraphs),
        "docx_tables": sum(1 for b in blocks if b["kind"] == "table"),
        "entries_found_in_docx": len(found),
        "title_mismatches": title_mismatches,
        "premise_mismatches": premise_mismatches,
        "issues": issues,
        "pass": not issues and not title_mismatches and not premise_mismatches,
    }
    out = ROOT / "planning" / "source_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("pass", "entries_found_in_docx", "docx_tables", "issues")}, indent=2))
    print(f"title_mismatches={len(title_mismatches)} premise_mismatches={len(premise_mismatches)}")
    if title_mismatches[:5]:
        print("TITLE SAMPLE", title_mismatches[:3])
    if premise_mismatches[:3]:
        print("PREMISE SAMPLE", json.dumps(premise_mismatches[:2], ensure_ascii=False)[:2000])


if __name__ == "__main__":
    main()
