#!/usr/bin/env python3
"""Choose one activity version after the filters, for Surprise Us.

The paper version lives in frontmatter/06-surprise-us.md.

A draw is a variant, not merely the chapter's default length. Touch and the
depth ceiling are never dropped, including when --relax is present.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import catalog_variants  # noqa: E402

RELAXABLE = ("time_band", "energy", "format", "mood")
DEPTH_ORDER = ("light", "personal", "deep", "intense")


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


def normalize(value: object) -> str:
    return str(value).strip().casefold().replace("–", "-").replace("—", "-")


def unique_values(values: list[str]) -> list[str]:
    found: list[str] = []
    for value in values:
        text = normalize(value)
        if text and text not in found:
            found.append(text)
    return found


def depth_allowed(value: str, ceiling: str) -> bool:
    if not ceiling:
        return True
    if value not in DEPTH_ORDER or ceiling not in DEPTH_ORDER:
        return False
    return DEPTH_ORDER.index(value) <= DEPTH_ORDER.index(ceiling)


def eligible(rows: list[catalog_variants.Variant], filters: dict[str, set[str]]) -> list[catalog_variants.Variant]:
    chosen = []
    ceilings = filters.get("depth_ceiling") or set()
    ceiling = next(iter(ceilings), "")
    for row in rows:
        if not row.time_category:
            continue
        wanted_time = filters.get("time_band") or set()
        if wanted_time and row.time_category not in wanted_time:
            continue
        wanted_energy = filters.get("energy") or set()
        if wanted_energy and normalize(row.energy) not in wanted_energy:
            continue
        wanted_format = filters.get("format") or set()
        if wanted_format and not wanted_format.intersection(normalize(item) for item in row.formats):
            continue
        wanted_mood = filters.get("mood") or set()
        if wanted_mood and not wanted_mood.intersection(normalize(item) for item in row.moods):
            continue
        if not depth_allowed(row.emotional_intensity, ceiling):
            continue
        touch = filters.get("touch") or set()
        if "no" in touch and row.touch:
            continue
        chosen.append(row)
    return chosen


def print_filters(filters: dict[str, set[str]]) -> None:
    for name in ("time_band", "energy", "depth_ceiling", "touch", "format", "mood"):
        if filters.get(name):
            print(f"{name}: " + ", ".join(sorted(filters[name])))


def print_match(row: catalog_variants.Variant, dropped: list[str]) -> None:
    print(f"{row.shown_id}  {row.title}".rstrip())
    print(f"variant: {row.variant_id}")
    if row.estimated_minutes is None:
        print(f"estimate: {row.display_duration}")
    else:
        print(f"estimate: {row.estimated_minutes} minutes")
    print(f"shelf: {row.time_category}")
    print(f"anchor: {row.link_anchor}")
    print(f"energy: {row.energy}")
    print(f"emotional_intensity: {row.emotional_intensity}")
    print(f"touch: {'true' if row.touch else 'false'}")
    print("format: " + ", ".join(row.formats))
    print("mood: " + ", ".join(row.moods))
    if dropped:
        print("Relaxed by dropping: " + ", ".join(dropped))


def parser() -> argparse.ArgumentParser:
    tool = argparse.ArgumentParser(
        description="Choose one activity version after filters. Touch and depth are never relaxed.",
    )
    tool.add_argument("--time-band", action="append", default=[], dest="time_band")
    tool.add_argument("--energy", action="append", default=[])
    tool.add_argument("--depth-ceiling", default="", choices=["", *DEPTH_ORDER])
    tool.add_argument("--touch", default="", choices=["", "yes", "no"])
    tool.add_argument("--format", action="append", default=[])
    tool.add_argument("--mood", action="append", default=[])
    tool.add_argument(
        "--relax",
        action="store_true",
        help="Drop time, energy, format, or mood from the end until something matches. Never drops touch or depth.",
    )
    tool.add_argument("--seed", type=int, default=None)
    return tool


def filters_from_args(args) -> dict[str, set[str]]:
    filters = {
        "time_band": set(unique_values(args.time_band)),
        "energy": set(unique_values(args.energy)),
        "format": set(unique_values(args.format)),
        "mood": set(unique_values(args.mood)),
        "depth_ceiling": {args.depth_ceiling} if args.depth_ceiling else set(),
        "touch": {args.touch} if args.touch else set(),
    }
    return filters


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = parser().parse_args(argv)
    filters = filters_from_args(args)
    rows = catalog_variants.load_variants()
    chosen = eligible(rows, filters)
    dropped: list[str] = []
    if not chosen and args.relax:
        narrowed = {name: set(values) for name, values in filters.items()}
        for name in reversed(RELAXABLE):
            if not narrowed.get(name):
                continue
            narrowed[name] = set()
            dropped.append(name)
            chosen = eligible(rows, narrowed)
            if chosen:
                break
    if not chosen:
        print("No activity matches these filters.")
        print_filters(filters)
        if dropped:
            print("Dropped while relaxing: " + ", ".join(dropped))
            print("Filters were relaxed and still nothing matched.")
        else:
            print("Filters were not relaxed.")
        return 2
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    print_match(rng.choice(chosen), dropped)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:
        raise SystemExit(f"Surprise Us failed: {exc}") from exc
