# Chapter contract

Every file is `chapters/part-XX/NNN-slug.md` using the catalog title exactly.

## Frontmatter

```yaml
---
id: "001"
title: "The Stranger Across From Me"
part: 1
part_title: "The Art of Really Knowing Someone"
slug: stranger-across-from-me
deck: "One sentence that makes two adults want to start."
classification: reimagined
primary_minutes: 35
time_band: "20-45"
durations:
  short: "10 minutes"
  standard: "35 minutes"
  extended: "70 minutes"
has_short: true
has_standard: true
has_extended: true
emotional_intensity: personal
energy: low
formats: [conversation, roleplay]
moods: [discover, laugh]
location: "indoors, seated"
materials: ["two chairs", "a timer"]
setup_effort: low
writing: true
affection: false
discussion: true
touch: false
repeatable: true
cross_links: ["005", "008", "016"]
motif: "assets/chapters/001/motif.svg"
---
```

Allowed `time_band`: `5-10`, `10-20`, `20-45`, `45-90`, `90-180`, `long-day`, `multi-day`. Use `long-day` for one calendar day longer than 3 hours. Use `multi-day` only when the activity itself spans more than one date. The Time index still lists every version from `durations`, so a short sitting can appear on an earlier shelf than `time_band`.

Allowed `emotional_intensity`: `light`, `personal`, `deep`, `intense`.

Allowed `energy`: `low`, `medium`, `high`.

Allowed `classification`: `established`, `reimagined`, `original-formulation`, `mixed`.

Entries 097–108 are `original-formulation`.

`cross_links` are real catalog IDs only.

## Required headings, in this order

1. `## The hook`
2. `## Why it might matter`
3. `## Before you begin`
4. `## The experience`
5. `## Three ways to play` (omit a length only if the frontmatter flag is false, and say why in this section)
6. `## Going deeper`
7. `## Variations and replay`
8. `## Examples`
9. `## Afterward`
10. `## Our Story`
11. `## Notes`

Body prose, excluding frontmatter and the journal block, should usually land between 1,200 and 2,200 words. Games and signatures may run longer. Do not pad.

## Our Story block

After the human-readable journal instructions, include:

```journal
session: date, time, place, version played, mood if wanted, intention, initials if wanted, done or paused
partner_a:
- prompt specific to this activity
- a second prompt
partner_b:
- prompt with equal dignity, not a copy that assumes the same role
- a second prompt
shared:
- What actually happened
- The line or moment worth keeping
- What we discovered
- What we might do next, if anything
revisit:
- Attempt, date, and what changed
- Then versus now
```

Private pages are optional to share. Say so once, in ordinary sentences.

## Voice

Write to both people. No therapy clichés, no broken-relationship framing, no gender roles, no scavenger hunt, no fabricated memories of a real couple. Label every sample exchange as fictional. Passing, pausing, and changing a prompt are ordinary options. A game result is not consent to touch or sex.

## Evidence

Cite whitelist IDs in `## Notes`, for example `See A1997.` If the whitelist does not support a sentence, do not write it as a research finding. Folk games can be described as folk games.
