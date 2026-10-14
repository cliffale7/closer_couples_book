#!/usr/bin/env python3
"""Choose one chapter after the filters, for Surprise Us.

The paper version lives in frontmatter/06-surprise-us.md.

Usage, from the repository root:

    python scripts/surprise_us.py
    python scripts/surprise_us.py --time-band 20-45 --energy low
    python scripts/surprise_us.py --help

With no filters, one chapter is chosen from the full set. This is the
no-argument demo. Filters are applied before the choice. If nothing
matches, the script says so and does not drop a filter unless --relax
is present.

Reads chapter frontmatter only. Does not read journal/private/.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import yaml

import build_all

# The paper version lives in frontmatter/06-surprise-us.md.
FILTER_ORDER = ("time_band", "energy", "emotional_intensity", "format", "mood")
FRONTMATTER_LINE_CAP = 200


def configure_stdio() -> None:
    build_all.configure_stdio()


def normalize(value: object) -> str:
    return str(value).strip().casefold().replace("–", "-").replace("—", "-")


def unique_values(values: list[str]) -> list[str]:
    found: list[str] = []
    for value in values:
        text = normalize(value)
        if text and text not in found:
            found.append(text)
    return found


def string_list(value) -> list[str]:
    if value is None:
        return []
    items = value if isinstance(value, (list, tuple)) else [value]
    found = []
    for item in items:
        text = str(item).strip()
        if text:
            found.append(text)
    return found


def read_frontmatter(path: Path) -> dict:
    """Stop at the closing marker so the chapter body is not read."""
    build_all.assert_readable(path)
    lines: list[str] = []
    markers = 0
    with path.open(encoding="utf-8-sig") as handle:
        for _ in range(FRONTMATTER_LINE_CAP):
            line = handle.readline()
            if line == "":
                break
            if line.strip() == "---":
                markers += 1
                if markers == 2:
                    break
                continue
            if markers == 1:
                lines.append(line)
        else:
            raise SystemExit(
                f"{build_all.rel_posix(path)}: frontmatter did not close within {FRONTMATTER_LINE_CAP} lines."
            )
    if markers < 2:
        raise SystemExit(f"{build_all.rel_posix(path)}: YAML frontmatter is missing its closing ---.")
    raw = "".join(lines)
    try:
        loaded = yaml.safe_load(raw) if raw.strip() else {}
    except yaml.YAMLError as exc:
        raise SystemExit(f"{build_all.rel_posix(path)}: YAML frontmatter could not be parsed: {exc}") from exc
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise SystemExit(f"{build_all.rel_posix(path)}: YAML frontmatter must be a mapping.")
    return loaded


def load_chapters() -> list[dict]:
    folder = build_all.ROOT / "chapters"
    if not folder.is_dir():
        return []
    chapters = []
    paths = sorted(
        path for path in folder.glob("**/*.md") if path.is_file() and path.name.lower() != "readme.md"
    )
    for path in paths:
        meta = read_frontmatter(path)
        meta["_sort_id"] = int(str(meta.get("id")).strip()) if str(meta.get("id", "")).strip().isdigit() else 10**6
        chapters.append(meta)
    chapters.sort(key=lambda meta: (meta["_sort_id"], str(meta.get("title") or "").casefold()))
    return chapters


def field_values(meta: dict, name: str) -> set[str]:
    if name == "format":
        source = meta.get("formats", meta.get("format"))
    elif name == "mood":
        source = meta.get("moods", meta.get("mood"))
    else:
        source = meta.get(name)
    return {normalize(item) for item in string_list(source) if normalize(item)}


def matches(meta: dict, filters: dict[str, set[str]]) -> bool:
    for name, wanted in filters.items():
        if not wanted:
            continue
        if not field_values(meta, name).intersection(wanted):
            return False
    return True


def print_filters(filters: dict[str, set[str]]) -> None:
    for name in FILTER_ORDER:
        if filters[name]:
            print(f"{name}: " + ", ".join(sorted(filters[name])))


def print_match(meta: dict, dropped: list[str]) -> None:
    raw = str(meta.get("id", "")).strip()
    shown = raw.zfill(3) if raw.isdigit() else raw
    title = str(meta.get("title") or "").strip()
    print(f"{shown}  {title}".rstrip())
    if raw.isdigit():
        print(f"anchor: chapter-{int(raw):03d}")
    elif raw:
        print(f"id: {raw}")
    for name in ("time_band", "energy", "emotional_intensity"):
        print(f"{name}: {meta.get(name, '')}")
    print("format: " + ", ".join(string_list(meta.get("formats", meta.get("format")))))
    print("mood: " + ", ".join(string_list(meta.get("moods", meta.get("mood")))))
    if dropped:
        print("Relaxed by dropping: " + ", ".join(dropped))


def parser() -> argparse.ArgumentParser:
    tool = argparse.ArgumentParser(
        description=(
            "Choose one chapter after filters. "
            "The paper version lives in frontmatter/06-surprise-us.md."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "With no filters, one chapter is chosen from the full set.\n"
            "Repeat a filter to allow more than one value. Values within one filter\n"
            "are combined. Different filters all have to match.\n"
            "If nothing matches, the filters stay as given unless you pass --relax.\n\n"
            "Examples:\n"
            "  python scripts/surprise_us.py\n"
            "  python scripts/surprise_us.py --time-band 20-45 --energy low --mood discover\n"
        ),
    )
    tool.add_argument("--time-band", action="append", default=[], dest="time_band", help="Exact time_band. Repeat to allow a pair.")
    tool.add_argument("--energy", action="append", default=[], help="Exact energy. Repeat to allow more than one.")
    tool.add_argument(
        "--emotional-intensity",
        action="append",
        default=[],
        dest="emotional_intensity",
        help="Exact emotional_intensity. Repeat to allow more than one.",
    )
    tool.add_argument("--format", action="append", default=[], help="Match a formats entry. Repeat to allow more than one.")
    tool.add_argument("--mood", action="append", default=[], help="Match a moods entry. Repeat to allow more than one.")
    tool.add_argument(
        "--relax",
        action="store_true",
        help="Only if nothing matches, drop filters from the end until a chapter matches.",
    )
    tool.add_argument("--seed", type=int, default=None, help="Optional choice seed. Omit it for a fresh draw.")
    return tool


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = parser().parse_args(argv)
    # Filters are applied before the choice. They are not relaxed unless --relax was passed.
    filters = {name: set(unique_values(getattr(args, name))) for name in FILTER_ORDER}
    chapters = load_chapters()
    eligible = [meta for meta in chapters if matches(meta, filters)]
    dropped: list[str] = []
    if not eligible and args.relax:
        narrowed = {name: set(values) for name, values in filters.items()}
        for name in reversed(FILTER_ORDER):
            if not narrowed[name]:
                continue
            narrowed[name] = set()
            dropped.append(name)
            eligible = [meta for meta in chapters if matches(meta, narrowed)]
            if eligible:
                break
    if not eligible:
        print("No chapter matches these filters.")
        print_filters(filters)
        if dropped:
            print("Dropped while relaxing: " + ", ".join(dropped))
            print("Filters were relaxed and still nothing matched.")
        else:
            print("Filters were not relaxed.")
        return 2
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    print_match(rng.choice(eligible), dropped)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        raise SystemExit(f"Surprise Us failed: {exc}") from exc
