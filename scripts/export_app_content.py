#!/usr/bin/env python3
"""Write the public, versioned book bundle the Android project can import.

The bundle is editorial content only. It does not read journal/private/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_all  # noqa: E402
import catalog_variants  # noqa: E402

SCHEMA = "closer-content/1"
EDITION = "v1-draft"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def heading_key(text: str) -> str:
    return build_all.slugify(text)


def section_visibility(heading: str) -> str:
    folded = heading.casefold()
    if "facilitator" in folded or folded.startswith("cover this"):
        return "hidden"
    return "player"


def journal_prompts(doc: build_all.SourceDoc) -> list[dict]:
    prompts = []
    for block in doc.blocks:
        if block[0] != "fence" or block[1] != "journal":
            continue
        seat = ""
        counts: dict[str, int] = {}
        for line in block[2].splitlines():
            stripped = line.strip()
            if stripped.endswith(":") and not stripped.startswith("-"):
                seat = stripped[:-1]
                continue
            if stripped.startswith("- ") and seat in {"partner_a", "partner_b", "shared", "revisit"}:
                counts[seat] = counts.get(seat, 0) + 1
                prompt_id = f"{doc.meta.get('id')}.{seat}.{counts[seat]}"
                text = stripped[2:].strip()
                prompts.append(
                    {
                        "id": prompt_id,
                        "prompt_version": 1,
                        "activity_id": str(doc.meta.get("id")),
                        "seat": seat,
                        "private": seat in {"partner_a", "partner_b"},
                        "text": text,
                        "introduced_in": EDITION,
                        "deprecated_in": None,
                    }
                )
    return prompts


def sections_for(doc: build_all.SourceDoc) -> list[dict]:
    sections = []
    current: dict | None = None
    chunks: list[str] = []

    def flush() -> None:
        nonlocal current, chunks
        if current is None:
            chunks = []
            return
        current["markdown"] = "\n\n".join(chunk for chunk in chunks if chunk.strip())
        sections.append(current)
        current = None
        chunks = []

    for block in build_all.body_blocks(doc):
        if block[0] == "heading":
            flush()
            title = block[2]
            current = {
                "key": heading_key(title),
                "heading": title,
                "level": block[1],
                "visibility": section_visibility(title),
            }
        elif block[0] == "para":
            chunks.append(block[1])
        elif block[0] == "fence" and block[1] == "cards":
            chunks.append("```cards\n" + block[2] + "\n```")
        elif block[0] == "fence" and block[1] != "journal":
            chunks.append(block[2])
    flush()
    return sections


def variants_for(doc: build_all.SourceDoc) -> list[dict]:
    rows = []
    for variant in catalog_variants.variants_from_meta(doc.meta, kind=doc.kind, anchor=doc.anchor):
        if not variant.time_category:
            continue
        rows.append(
            {
                "variant_id": variant.variant_id,
                "display_duration": variant.display_duration,
                "estimated_minutes": variant.estimated_minutes,
                "time_category": variant.time_category,
                "is_multi_day": variant.is_multi_day,
                "link_anchor": variant.link_anchor,
            }
        )
    return rows


def activity_object(doc: build_all.SourceDoc, prompts: list[dict]) -> dict:
    meta = doc.meta
    motif = str(meta.get("motif") or "")
    payload = {
        "schema_version": SCHEMA,
        "id": str(meta.get("id")),
        "kind": doc.kind,
        "title": doc.title,
        "slug": str(meta.get("slug") or ""),
        "part": meta.get("part"),
        "part_title": meta.get("part_title"),
        "classification": meta.get("classification"),
        "anchor": doc.anchor,
        "deck": meta.get("deck") or "",
        "energy": meta.get("energy"),
        "emotional_intensity": meta.get("emotional_intensity"),
        "formats": catalog_variants._string_list(meta.get("formats", meta.get("format"))),
        "moods": catalog_variants._string_list(meta.get("moods", meta.get("mood"))),
        "touch": meta.get("touch") is True,
        "affection": meta.get("affection") is True,
        "repeatable": meta.get("repeatable") is True,
        "materials": catalog_variants._string_list(meta.get("materials")),
        "cross_links": [str(item) for item in (meta.get("cross_links") or [])],
        "variants": variants_for(doc),
        "sections": sections_for(doc),
        "prompt_ids": [item["id"] for item in prompts],
        "artwork": [{"id": motif, "alt": f"Motif for {doc.title}"}] if motif else [],
        "requires_app_update": False,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    payload["content_hash"] = sha256_text(encoded)
    return payload


def asset_entries(docs: list[build_all.SourceDoc]) -> list[tuple[str, bytes]]:
    paths = []
    for doc in docs:
        motif = str(doc.meta.get("motif") or "")
        if motif:
            paths.append(ROOT / motif)
    for number in range(1, 14):
        paths.append(ROOT / f"assets/parts/{number:02d}-opener.svg")
    found = []
    seen = set()
    for path in paths:
        if not path.is_file():
            continue
        rel = path.resolve().relative_to(ROOT.resolve()).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        found.append((rel, path.read_bytes()))
    return found


def build_bundle(dest_dir: Path, source_commit: str) -> Path:
    docs, _parts = build_all.load_sources(False)
    activities = []
    prompts = []
    for doc in docs:
        if doc.kind not in {"chapter", "signature"}:
            continue
        activity_prompts = journal_prompts(doc)
        prompts.extend(activity_prompts)
        activities.append(activity_object(doc, activity_prompts))
    activities.sort(key=lambda item: (item["kind"] != "chapter", item["id"]))
    parts = []
    current = None
    for item in activities:
        if item["kind"] != "chapter":
            continue
        part = item.get("part")
        if current is None or current["part"] != part:
            current = {"part": part, "title": item.get("part_title"), "activity_ids": []}
            parts.append(current)
        current["activity_ids"].append(item["id"])
    files: dict[str, bytes] = {}
    files["activities.json"] = json.dumps(activities, ensure_ascii=False, indent=2).encode("utf-8")
    files["prompts.json"] = json.dumps(prompts, ensure_ascii=False, indent=2).encode("utf-8")
    files["parts.json"] = json.dumps(parts, ensure_ascii=False, indent=2).encode("utf-8")
    files["signatures.json"] = json.dumps(
        [item for item in activities if item["kind"] == "signature"],
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8")
    for rel, data in asset_entries(docs):
        files[f"assets/{rel}"] = data
    changes = {
        "schema_version": SCHEMA,
        "from_bundle": None,
        "added_activity_ids": [item["id"] for item in activities],
        "removed_activity_ids": [],
        "changed_activity_ids": [],
        "tombstones": [],
        "prompt_policy": "A prompt id stays with answers already written. A wording change keeps the id and records the old text_at_answer on the session. A new id is issued only when the question's meaning changes.",
    }
    files["CHANGES.json"] = json.dumps(changes, ensure_ascii=False, indent=2).encode("utf-8")
    handoff = """# App update handoff

1. Use the newest `The_Closer_Project_Content_*.zip` whose manifest names the source commit you intend to import.
2. Compare `manifest.json` file hashes with the bundle already in the app.
3. Import changed activities, prompts, and assets. Do not rewrite stored journal answers.
4. If `requires_app_update` is true on an activity, ship an app change before relying on that activity's new interaction.
5. A schema other than `closer-content/1` should be refused, leaving the previous bundle and every journal entry in place.
6. This package contains public book text only.
"""
    files["APP_UPDATE_HANDOFF.md"] = handoff.encode("utf-8")
    manifest = {
        "schema_version": SCHEMA,
        "book_edition": EDITION,
        "source_commit": source_commit,
        "activity_ids": [item["id"] for item in activities if item["kind"] == "chapter"],
        "signature_ids": [item["id"] for item in activities if item["kind"] == "signature"],
        "files": {name: sha256_bytes(data) for name, data in sorted(files.items())},
        "privacy": "Public editorial content only. No private journal is included.",
    }
    files["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / f"The_Closer_Project_Content_{EDITION}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            archive.writestr(name, data)
    (dest_dir / "APP_UPDATE_HANDOFF.md").write_text(handoff, encoding="utf-8")
    return zip_path


def main(argv: list[str] | None = None) -> int:
    build_all.configure_stdio()
    parser = argparse.ArgumentParser(description="Build the public Android content bundle.")
    parser.add_argument("--dest", type=Path, default=ROOT / "release" / "app_content")
    parser.add_argument("--source-commit", default="uncommitted")
    args = parser.parse_args(argv)
    if build_all.is_private_path(args.dest):
        raise SystemExit("Refusing to write the public bundle into journal/private.")
    path = build_bundle(args.dest, args.source_commit)
    print(f"bundle: {path}")
    print(f"bytes: {path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
