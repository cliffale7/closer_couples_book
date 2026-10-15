#!/usr/bin/env python3
"""Normalize chapter and signature durations into time shelves.

A duration is read from the YAML ``durations`` text. Minutes are not inferred
from a title. A span of calendar days is multi-day even when the sentence also
mentions a short closing conversation.

Shelf boundaries, one shelf each, upper bound inclusive except the long day:

- 5–10: 5 <= minutes <= 10
- 10–20: 10 < minutes <= 20
- 20–45: 20 < minutes <= 45
- 45–90: 45 < minutes <= 90
- 90–180: 90 < minutes <= 180 (through 3 hours)
- long-day: minutes > 180, or an evening/afternoon with no minute count, still one day
- multi-day: a numbered span of days

Ten minutes is Quick Connections only. Four hours and twelve hours are a long
day, not multi-day. Three hours stays a full experience.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

SHELF_ORDER = ["5-10", "10-20", "20-45", "45-90", "90-180", "long-day", "multi-day"]
SHELF_LABELS = {
    "5-10": "5–10 minutes — Quick Connections",
    "10-20": "10–20 minutes — Little Discoveries",
    "20-45": "20–45 minutes — Meaningful Sessions",
    "45-90": "45–90 minutes — Deep Dives",
    "90-180": "90 minutes–3 hours — Full Experiences",
    "long-day": "Long day — more than 3 hours, still one day",
    "multi-day": "Multi-day — The Long Game",
}
VARIANT_ORDER = ("short", "standard", "extended")
VARIANT_PRETTY = {"short": "Short", "standard": "Standard", "extended": "Extended", "primary": "Primary"}
DAY_WORDS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}
DAY_RE = re.compile(
    r"\b(\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten)\s+days?\b",
    re.IGNORECASE,
)
MINUTE_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|hrs?)\b", re.IGNORECASE)


@dataclass
class Variant:
    activity_id: str
    title: str
    kind: str
    anchor: str
    variant_id: str
    display_duration: str
    estimated_minutes: int | None
    time_category: str
    is_multi_day: bool
    is_calendar_day: bool
    link_anchor: str
    energy: str
    emotional_intensity: str
    formats: list[str]
    moods: list[str]
    touch: bool
    repeatable: bool
    issues: list[str] = field(default_factory=list)

    @property
    def shown_id(self) -> str:
        raw = self.activity_id.strip()
        return raw.zfill(3) if raw.isdigit() else raw

    @property
    def estimate_text(self) -> str:
        if self.estimated_minutes is None:
            return self.display_duration
        minutes = self.estimated_minutes
        if minutes >= 60 and minutes % 60 == 0:
            return f"~{minutes // 60} h"
        return f"~{minutes} min"

    @property
    def index_label(self) -> str:
        pretty = VARIANT_PRETTY.get(self.variant_id, self.variant_id)
        if self.variant_id == "primary":
            return f"{self.shown_id} — {self.title}"
        return f"{self.shown_id} — {self.title} ({pretty}, {self.estimate_text})"


def shelf_for_minutes(minutes: int) -> str:
    if minutes <= 10:
        return "5-10"
    if minutes <= 20:
        return "10-20"
    if minutes <= 45:
        return "20-45"
    if minutes <= 90:
        return "45-90"
    if minutes <= 180:
        return "90-180"
    return "long-day"


def _string_list(value) -> list[str]:
    if value is None:
        return []
    items = value if isinstance(value, (list, tuple)) else [value]
    found = []
    for item in items:
        text = str(item).strip()
        if text:
            found.append(text)
    return found


def parse_duration(text: str) -> dict:
    """Return minutes, shelf, flags, and issues. Does not invent a minute count."""
    raw = str(text).strip()
    folded = raw.casefold().replace("–", "-").replace("—", "-")
    folded = re.sub(r"^(about|around|roughly)\s+", "", folded)
    if DAY_RE.search(folded):
        return {
            "minutes": None,
            "shelf": "multi-day",
            "multi": True,
            "calendar": True,
            "issues": [],
        }
    match = MINUTE_RE.match(folded)
    if match:
        amount = float(match.group(1))
        unit = match.group(2).casefold()
        minutes = int(round(amount * 60)) if unit.startswith("h") else int(round(amount))
        return {
            "minutes": minutes,
            "shelf": shelf_for_minutes(minutes),
            "multi": False,
            "calendar": minutes > 180,
            "issues": [] if minutes >= 5 else ["below_named_minimum"],
        }
    if re.match(r"^(an|one)\s+hour\b", folded):
        return {"minutes": 60, "shelf": "45-90", "multi": False, "calendar": False, "issues": []}
    if re.match(r"^half an hour\b", folded):
        return {"minutes": 30, "shelf": "20-45", "multi": False, "calendar": False, "issues": []}
    if any(word in folded for word in ("evening", "afternoon", "all day")):
        return {
            "minutes": None,
            "shelf": "long-day",
            "multi": False,
            "calendar": True,
            "issues": ["explicit_long_day"],
        }
    return {
        "minutes": None,
        "shelf": "",
        "multi": False,
        "calendar": False,
        "issues": ["unparsed_duration"],
    }


def activity_anchor(meta: dict, kind: str) -> str:
    raw = str(meta.get("id") or "").strip()
    if kind == "signature" or re.fullmatch(r"S\d+", raw, re.IGNORECASE):
        return "signature-" + raw.lower()
    if raw.isdigit():
        return f"chapter-{int(raw):03d}"
    return "chapter-" + raw.lower()


def variants_from_meta(meta: dict, *, kind: str, anchor: str | None = None) -> list[Variant]:
    anchor = anchor or activity_anchor(meta, kind)
    raw_id = str(meta.get("id") or "").strip()
    title = str(meta.get("title") or "").strip()
    energy = str(meta.get("energy") or "").strip()
    intensity = str(meta.get("emotional_intensity") or "").strip()
    formats = _string_list(meta.get("formats", meta.get("format")))
    moods = _string_list(meta.get("moods", meta.get("mood")))
    touch = meta.get("touch") is True
    repeatable = meta.get("repeatable") is True
    durations = meta.get("durations") if isinstance(meta.get("durations"), dict) else {}
    found: list[Variant] = []
    shared_issues: list[str] = []
    if meta.get("durations") is not None and not isinstance(meta.get("durations"), dict):
        shared_issues.append("durations_not_a_mapping")

    for name in VARIANT_ORDER:
        flag = meta.get(f"has_{name}")
        text = durations.get(name)
        text = str(text).strip() if text is not None else ""
        if flag is False:
            if text:
                shared_issues.append(f"{name}_present_while_disabled")
            continue
        if flag is True and not text:
            shared_issues.append(f"missing_{name}")
            continue
        if not text:
            continue
        parsed = parse_duration(text)
        if not parsed["shelf"]:
            shared_issues.extend(f"{name}:{item}" for item in parsed["issues"])
            continue
        found.append(
            Variant(
                activity_id=raw_id,
                title=title,
                kind=kind,
                anchor=anchor,
                variant_id=name,
                display_duration=text,
                estimated_minutes=parsed["minutes"],
                time_category=parsed["shelf"],
                is_multi_day=parsed["multi"],
                is_calendar_day=parsed["calendar"] or parsed["multi"],
                link_anchor=f"{anchor}-three-ways-to-play",
                energy=energy,
                emotional_intensity=intensity,
                formats=formats,
                moods=moods,
                touch=touch,
                repeatable=repeatable,
                issues=list(parsed["issues"]),
            )
        )

    if found:
        if shared_issues and found[0].issues is not None:
            found[0].issues.extend(shared_issues)
        return found

    band = str(meta.get("time_band") or "").strip()
    if band in SHELF_LABELS:
        found.append(
            Variant(
                activity_id=raw_id,
                title=title,
                kind=kind,
                anchor=anchor,
                variant_id="primary",
                display_duration=band,
                estimated_minutes=None,
                time_category=band,
                is_multi_day=band == "multi-day",
                is_calendar_day=band in {"long-day", "multi-day"},
                link_anchor=anchor,
                energy=energy,
                emotional_intensity=intensity,
                formats=formats,
                moods=moods,
                touch=touch,
                repeatable=repeatable,
                issues=shared_issues + ["duration_text_missing_used_time_band"],
            )
        )
        return found
    if shared_issues or band:
        # Keep a non-indexed record so the audit can name the gap.
        found.append(
            Variant(
                activity_id=raw_id,
                title=title,
                kind=kind,
                anchor=anchor,
                variant_id="primary",
                display_duration=band,
                estimated_minutes=None,
                time_category="",
                is_multi_day=False,
                is_calendar_day=False,
                link_anchor=anchor,
                energy=energy,
                emotional_intensity=intensity,
                formats=formats,
                moods=moods,
                touch=touch,
                repeatable=repeatable,
                issues=shared_issues + (["unparsed_time_band"] if band else ["no_duration"]),
            )
        )
    return found


def read_frontmatter(path: Path) -> dict:
    lines: list[str] = []
    markers = 0
    with path.open(encoding="utf-8-sig") as handle:
        for _ in range(200):
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
    if markers < 2:
        raise SystemExit(f"{path}: YAML frontmatter did not close.")
    loaded = yaml.safe_load("".join(lines)) or {}
    if not isinstance(loaded, dict):
        raise SystemExit(f"{path}: YAML frontmatter must be a mapping.")
    return loaded


def iter_activity_paths(root: Path | None = None) -> list[tuple[str, Path]]:
    root = root or ROOT
    found: list[tuple[str, Path]] = []
    chapters = root / "chapters"
    if chapters.is_dir():
        for path in sorted(chapters.glob("**/*.md")):
            if path.is_file() and path.name.lower() != "readme.md":
                found.append(("chapter", path))
    signatures = root / "signature"
    if signatures.is_dir():
        for path in sorted(signatures.glob("*.md")):
            if path.is_file() and path.name.lower() != "readme.md":
                found.append(("signature", path))
    return found


def load_variants(root: Path | None = None) -> list[Variant]:
    rows: list[Variant] = []
    for kind, path in iter_activity_paths(root):
        meta = read_frontmatter(path)
        rows.extend(variants_from_meta(meta, kind=kind))
    return rows


def write_audit(path: Path, rows: list[Variant]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    indexed = [row for row in rows if row.time_category]
    lines = [
        "# Variant time audit",
        "",
        "Generated by `scripts/catalog_variants.py`. Minutes come from the duration sentence, not the title.",
        "",
        "Boundary rule: a stated minute count belongs to exactly one shelf. The upper bound of each shelf through 3 hours is inclusive, so 10 minutes is only Quick Connections, 20 is only Little Discoveries, 45 is only Meaningful Sessions, 90 is only Deep Dives, and 180 is only Full Experiences. A single day longer than 3 hours is Long day. A numbered span of days is Multi-day, including a version whose sentence also names a short closing talk.",
        "",
        "An evening, afternoon, or all-day line with no minute count is Long day. The audit does not invent a minute total for that line.",
        "",
        f"Indexed variants: {len(indexed)}",
        f"Rows with parser notes: {sum(1 for row in rows if any(item != 'explicit_long_day' for item in row.issues))}",
        "",
        "| ID | Variant | Shelf | Minutes | Duration text | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        labels = {"explicit_long_day": "explicit long-day; minutes not invented"}
        notes = ", ".join(labels.get(item, item) for item in row.issues)
        minutes = "" if row.estimated_minutes is None else str(row.estimated_minutes)
        duration = row.display_duration.replace("|", "/")
        lines.append(
            f"| {row.shown_id} | {row.variant_id} | {row.time_category or '—'} | {minutes} | {duration} | {notes} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit variant time shelves.")
    parser.add_argument("--report", type=Path, default=ROOT / "planning" / "phase3" / "VARIANT_AUDIT.md")
    args = parser.parse_args(argv)
    rows = load_variants()
    write_audit(args.report, rows)
    print(f"variants: {len(rows)}")
    print(f"report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
