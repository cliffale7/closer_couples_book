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


EXPLICIT_SPOILER_HEADINGS = {
    "103": {"Facilitator section: solution key"},
    "S03": {"Cover this until the sample case is finished"},
}
REGISTRY_SCHEMA = "closer-prompt-registry/1"
SEATS = {"partner_a", "partner_b", "shared", "revisit"}


def spoiler_mark(activity_id: str, heading: str) -> tuple[str, bool, str | None]:
    """Hidden sections carry an explicit flag. A heading keyword is only the fallback."""
    if heading in EXPLICIT_SPOILER_HEADINGS.get(activity_id, set()):
        return "hidden", True, "registry"
    if build_all.cover_heading(heading):
        return "hidden", True, "heading"
    return "player", False, None


def empty_registry() -> dict:
    return {"schema": REGISTRY_SCHEMA, "prompts": []}


def load_registry(path: Path | None) -> dict:
    if path is None or not path.is_file():
        return empty_registry()
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict) or loaded.get("schema") != REGISTRY_SCHEMA:
        raise SystemExit("Prompt registry schema is not closer-prompt-registry/1.")
    if not isinstance(loaded.get("prompts"), list):
        raise SystemExit("Prompt registry prompts must be a list.")
    return loaded


def save_registry(path: Path | None, registry: dict) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def raw_prompts(doc: build_all.SourceDoc) -> list[dict]:
    found = []
    activity_id = str(doc.meta.get("id"))
    for block in doc.blocks:
        if block[0] != "fence" or block[1] != "journal":
            continue
        seat = ""
        for line in block[2].splitlines():
            stripped = line.strip()
            if stripped.endswith(":") and not stripped.startswith("-"):
                seat = stripped[:-1]
                continue
            if stripped.startswith("- ") and seat in SEATS:
                found.append(
                    {
                        "activity_id": activity_id,
                        "seat": seat,
                        "text": stripped[2:].strip(),
                    }
                )
    return found


def _suffix(prompt_id: str, activity_id: str, seat: str) -> int:
    prefix = f"{activity_id}.{seat}."
    if not prompt_id.startswith(prefix):
        return 0
    tail = prompt_id[len(prefix):]
    return int(tail) if tail.isdigit() else 0


def bind_prompts(raw: list[dict], registry: dict) -> tuple[list[dict], list[dict], dict]:
    """Reuse an id when the activity, seat, and wording match. A new wording gets a new id."""
    stored = [dict(item) for item in registry.get("prompts", []) if isinstance(item, dict)]
    active = {
        (item.get("activity_id"), item.get("seat"), item.get("text")): item
        for item in stored
        if item.get("status") != "tombstone"
    }
    used: set[str] = set()
    highest: dict[tuple[str, str], int] = {}
    known_ids = {str(item.get("id")) for item in stored}
    for item in stored:
        key = (str(item.get("activity_id")), str(item.get("seat")))
        highest[key] = max(highest.get(key, 0), _suffix(str(item.get("id")), key[0], key[1]))
    bound = []
    for item in raw:
        key = (item["activity_id"], item["seat"], item["text"])
        existing = active.get(key)
        if existing and existing.get("id") not in used:
            prompt_id = str(existing["id"])
            version = int(existing.get("prompt_version") or 1)
        else:
            seat_key = (item["activity_id"], item["seat"])
            number = highest.get(seat_key, 0)
            while True:
                number += 1
                prompt_id = f"{item['activity_id']}.{item['seat']}.{number}"
                if prompt_id not in known_ids and prompt_id not in used:
                    break
            highest[seat_key] = number
            known_ids.add(prompt_id)
            version = 1
            stored.append(
                {
                    "id": prompt_id,
                    "activity_id": item["activity_id"],
                    "seat": item["seat"],
                    "text": item["text"],
                    "prompt_version": version,
                    "status": "active",
                }
            )
        used.add(prompt_id)
        bound.append(
            {
                "id": prompt_id,
                "prompt_version": version,
                "activity_id": item["activity_id"],
                "seat": item["seat"],
                "private": item["seat"] in {"partner_a", "partner_b"},
                "text": item["text"],
                "introduced_in": EDITION,
                "deprecated_in": None,
            }
        )
    tombstones = []
    for item in stored:
        if item.get("status") == "tombstone":
            continue
        if item.get("id") in used:
            item["status"] = "active"
            continue
        item["status"] = "tombstone"
        tombstones.append(
            {
                "id": item.get("id"),
                "activity_id": item.get("activity_id"),
                "seat": item.get("seat"),
                "reason": "wording_or_seat_no_longer_present",
            }
        )
    registry = {"schema": REGISTRY_SCHEMA, "prompts": stored}
    return bound, tombstones, registry


def has_cards(doc: build_all.SourceDoc) -> bool:
    return any(block[0] == "fence" and block[1] == "cards" for block in doc.blocks)


def mechanics_for(doc: build_all.SourceDoc, sections: list[dict]) -> dict:
    cards = has_cards(doc)
    hidden = any(section.get("spoiler") for section in sections)
    if cards:
        kind = "cards"
        note = "Card text is in the cards fence. This bundle does not play the cards."
    elif hidden:
        kind = "hidden_key"
        note = "A covered section stays hidden until the reader reveals it. This bundle does not build the puzzle UI."
    else:
        kind = "narrative"
        note = "The instructions are prose. No separate interactive runtime is in this bundle."
    return {"kind": kind, "cards_fence": cards, "structured": cards, "note": note}


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
            visibility, spoiler, source = spoiler_mark(str(doc.meta.get("id")), title)
            current = {
                "key": heading_key(title),
                "heading": title,
                "level": block[1],
                "visibility": visibility,
                "spoiler": spoiler,
                "reveal": "covered_until_play" if spoiler else None,
                "spoiler_source": source,
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
    sections = sections_for(doc)
    mechanics = mechanics_for(doc, sections)
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
        "sections": sections,
        "mechanics": mechanics,
        "prompt_ids": [item["id"] for item in prompts],
        "artwork": [{"id": motif, "alt": f"Motif for {doc.title}"}] if motif else [],
        "requires_app_update": mechanics["kind"] != "narrative",
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
    signatures = ROOT / "assets" / "signatures"
    if signatures.is_dir():
        paths.extend(sorted(signatures.glob("S*-hero.svg")))
    covers = ROOT / "assets" / "covers"
    if covers.is_dir():
        paths.extend(sorted(covers.glob("*.svg")))
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


def changes_from_payloads(previous: dict | None, current: dict, tombstones: list[dict]) -> dict:
    """Compare two public bundles. A missing previous bundle is an initial baseline."""
    if previous is None:
        return {
            "schema_version": SCHEMA,
            "baseline": "initial",
            "from_bundle": None,
            "note": "Initial baseline. This is not an incremental update.",
            "added_activity_ids": [item["id"] for item in current["activities"]],
            "removed_activity_ids": [],
            "changed_activity_ids": [],
            "added_prompt_ids": [item["id"] for item in current["prompts"]],
            "removed_prompt_ids": [],
            "changed_prompt_ids": [],
            "added_assets": sorted(current["assets"]),
            "removed_assets": [],
            "changed_assets": [],
            "tombstones": tombstones,
            "prompt_policy": (
                "A prompt id stays with the activity, seat, and wording. "
                "Inserting or reordering a question does not renumber older ids. "
                "A wording that disappears is tombstoned. Stored answers are not rewritten."
            ),
        }
    old_activities = {item["id"]: item.get("content_hash") for item in previous["activities"]}
    new_activities = {item["id"]: item.get("content_hash") for item in current["activities"]}
    old_prompts = {item["id"]: item.get("text") for item in previous["prompts"]}
    new_prompts = {item["id"]: item.get("text") for item in current["prompts"]}
    old_assets = previous["assets"]
    new_assets = current["assets"]
    return {
        "schema_version": SCHEMA,
        "baseline": "update",
        "from_bundle": previous.get("name"),
        "note": "Compared with the previous public bundle. Unchanged ids are omitted.",
        "added_activity_ids": sorted(set(new_activities) - set(old_activities)),
        "removed_activity_ids": sorted(set(old_activities) - set(new_activities)),
        "changed_activity_ids": sorted(
            key for key in set(old_activities) & set(new_activities) if old_activities[key] != new_activities[key]
        ),
        "added_prompt_ids": sorted(set(new_prompts) - set(old_prompts)),
        "removed_prompt_ids": sorted(set(old_prompts) - set(new_prompts)),
        "changed_prompt_ids": sorted(
            key for key in set(old_prompts) & set(new_prompts) if old_prompts[key] != new_prompts[key]
        ),
        "added_assets": sorted(set(new_assets) - set(old_assets)),
        "removed_assets": sorted(set(old_assets) - set(new_assets)),
        "changed_assets": sorted(
            key for key in set(old_assets) & set(new_assets) if old_assets[key] != new_assets[key]
        ),
        "tombstones": tombstones,
        "prompt_policy": (
            "A prompt id stays with the activity, seat, and wording. "
            "Inserting or reordering a question does not renumber older ids. "
            "A wording that disappears is tombstoned. Stored answers are not rewritten."
        ),
    }


def payloads_from_zip(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        activities = json.loads(archive.read("activities.json"))
        prompts = json.loads(archive.read("prompts.json"))
        assets = {
            name: sha256_bytes(archive.read(name))
            for name in archive.namelist()
            if name.startswith("assets/")
        }
    return {"name": path.name, "activities": activities, "prompts": prompts, "assets": assets}


def build_bundle(
    dest_dir: Path,
    source_commit: str,
    previous_zip: Path | None = None,
    registry_path: Path | None = None,
) -> Path:
    docs, _parts = build_all.load_sources(False)
    registry = load_registry(registry_path)
    raw = []
    selected = []
    for doc in docs:
        if doc.kind not in {"chapter", "signature"}:
            continue
        selected.append(doc)
        raw.extend(raw_prompts(doc))
    prompts, tombstones, registry = bind_prompts(raw, registry)
    save_registry(registry_path, registry)
    by_activity: dict[str, list[dict]] = {}
    for prompt in prompts:
        by_activity.setdefault(prompt["activity_id"], []).append(prompt)
    activities = [activity_object(doc, by_activity.get(str(doc.meta.get("id")), [])) for doc in selected]
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
    asset_hashes = {}
    for rel, data in asset_entries(docs):
        name = f"assets/{rel}"
        files[name] = data
        asset_hashes[name] = sha256_bytes(data)
    current_payload = {
        "name": None,
        "activities": activities,
        "prompts": prompts,
        "assets": asset_hashes,
    }
    previous_payload = payloads_from_zip(previous_zip) if previous_zip else None
    changes = changes_from_payloads(previous_payload, current_payload, tombstones)
    files["CHANGES.json"] = json.dumps(changes, ensure_ascii=False, indent=2).encode("utf-8")
    handoff = """# App update handoff

1. Use the newest `The_Closer_Project_Content_*.zip` whose manifest names the source commit you intend to import.
2. Compare `manifest.json` file hashes with the bundle already in the app. `CHANGES.json` is the same comparison when a previous zip was supplied. An `initial` baseline is the first bundle, not a later diff.
3. Import changed activities, prompts, and assets. Do not rewrite stored journal answers. Tombstoned prompt ids stay in the registry so old answers keep their question.
4. If `requires_app_update` is true, the activity has cards or a covered key. Ship app code before treating that activity as playable in the app. Prose remains in the bundle either way.
5. A schema other than `closer-content/1` should be refused, leaving the previous bundle and every journal entry in place.
6. This package contains public book text only. On-device import is not tested in the book project.
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
        "on_device_import": "NOT TESTED IN BOOK PROJECT",
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
    parser.add_argument("--previous-bundle", type=Path, default=None)
    parser.add_argument("--registry", type=Path, default=ROOT / "source" / "prompt_registry.json")
    args = parser.parse_args(argv)
    if build_all.is_private_path(args.dest):
        raise SystemExit("Refusing to write the public bundle into journal/private.")
    path = build_bundle(args.dest, args.source_commit, args.previous_bundle, args.registry)
    print(f"bundle: {path}")
    print(f"bytes: {path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
