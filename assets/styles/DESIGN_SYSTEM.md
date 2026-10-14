# Night Library — design system

**Identity.** The Closer Project is a night library you can write in: midnight bands, parchment pages, and copper line drawings of keys, doors, paths, and constellations.

This is the visual system for the illustrated literary workbook. Palette and chapter motif subjects are already locked in `assets/styles/PALETTE_LOCK.md` and `assets/ART_MAP.json`. Do not invent a second palette, and do not edit `assets/ART_MAP.json` to restyle a chapter. Part openers are briefed in `assets/styles/PART_OPENERS.md`. Signature heroes are briefed in `assets/styles/SIGNATURE_ART.md`.

The book is for intelligent, mature adults. The pictures are warm, specific, and printable. They are a keepsake workbook: line and flat color, real margins, pages a pen can use. Guardrails for every asset: original drawing only; no copyrighted characters; no scavenger-hunt maps, clue trails, or hidden prizes; no clinical diagram-as-personality; no romance-cover clinch, roses, or heart-lock.

## Palette

Hex values are canonical for screen, EPUB, and the Edge/Chrome print CSS. Contrast ratios below were measured against WCAG relative luminance.

| Token | Hex | Role |
| --- | --- | --- |
| midnight | `#1B2433` | Cover ground, part-opener headband, display panels |
| charcoal | `#2C3544` | Secondary panels, running heads, quiet labels |
| parchment | `#F6F1E7` | Page ground |
| ivory | `#FBF8F2` | Journal writing ground; text on midnight, teal, and burgundy |
| ink | `#241F1C` | Body text and primary line |
| copper | `#A85A32` | Motif accent, rules, index-tab color |
| gold | `#C6A15B` | Small stars and folio ornaments on dark grounds |
| teal | `#3E6464` | Secondary motif accent |
| burgundy | `#7C3A46` | Desire chapters and signature warmth |
| line | `#D9CFC0` | Journal rules only |
| pause | `#3E6464` | Pause ring, always with the word Pause |

Measured contrast (useful pairs):

| Pair | Ratio | Use |
| --- | --- | --- |
| Ink on parchment | 14.49:1 | Body text |
| Ink on ivory | 15.38:1 | Prompts over writing blocks |
| Midnight on parchment | 13.85:1 | Display type on the page |
| Charcoal on parchment | 10.97:1 | Labels, running heads, folios |
| Ivory on midnight | 14.71:1 | Cover and part-band type |
| Parchment on midnight | 13.85:1 | Long cover text |
| Ivory on charcoal | 11.65:1 | Type on secondary panels |
| Burgundy on parchment | 7.31:1 | Accent words at text size |
| Ivory on burgundy | 7.77:1 | Type on a burgundy field |
| Teal on parchment | 5.81:1 | Short labels 11 pt and larger |
| Ivory on teal | 6.17:1 | Type on a teal field |
| Gold on midnight | 6.42:1 | Short cover labels, not body |
| Ivory on copper | 4.75:1 | Tab numerals only, 12 pt bold and larger |
| Copper on parchment | 4.47:1 | Rules and motif strokes, not small type |
| Ink on copper | 3.24:1 | Do not set text this way |
| Gold on parchment | 2.16:1 | Ornament only; never type |
| Line on parchment | 1.37:1 | Non-information writing rules |

Copper is a drawing and rule color. Small copper type fails ordinary text contrast, so metadata, captions, and instructions stay ink or charcoal. Gold never carries a word on parchment. Journal rules are faint on purpose; they guide a pen and never encode a choice, a score, or a warning.

## Type

No font files are bundled or redistributed. The stacks are faces that ship with Windows. Handwritten texture, when a page needs a flourish, is a drawn SVG stroke. It is not a script font, and it never sets instructions.

| Role | Face | Size / leading | Color |
| --- | --- | --- | --- |
| Cover title | Palatino Linotype Bold | 40 pt / 44 pt | Ivory |
| Part title | Palatino Linotype | 26 pt / 30 pt | Ivory on the midnight band |
| Chapter title | Palatino Linotype | 22 pt / 26 pt | Ink |
| Section heading | Palatino Linotype | 14 pt / 18 pt | Ink |
| Body | Georgia | 11 pt / 15 pt | Ink |
| Journal prompt | Georgia | 11 pt / 15 pt | Ink |
| Running head, folio, tags, captions | Calibri | 9 pt / 12 pt | Charcoal |
| Part number on the band | Calibri | 11 pt / 14 pt | Gold |
| Index tab numeral | Calibri Bold | 12 pt | Ivory on copper |

CSS stacks for the publication engineer:

```css
--face-title: "Palatino Linotype", Palatino, "Book Antiqua", serif;
--face-body: Georgia, "Times New Roman", serif;
--face-label: Calibri, "Segoe UI", sans-serif;
```

Instructional text does not go below Georgia 10.5 pt or Calibri 9 pt. Folios may sit at Calibri 9 pt. Italic Georgia is for a short deck under a title, not for long passages. Bold is for a name the reader must find, used rarely.

The baseline grid is 15 pt, started at the top of the live area. Body and prompts sit on it. Titles may occupy two or three lines, then the next block snaps back to the grid.

## Page geometry

Interior trim is 7.00 in wide by 10.00 in tall, portrait.

| Edge | Measure |
| --- | --- |
| Head | 0.70 in |
| Foot | 0.70 in |
| Fore-edge (outer) | 0.70 in |
| Gutter (inner) | 0.90 in |

The three outer edges the reader sees are 0.70 in. The gutter is wider because the book is long. On a recto, the gutter is the left edge and the fore-edge is the right. On a verso, they swap. If the final page count needs a thicker binding, increase the gutter and keep the fore-edge at 0.70 in.

Live area: 5.40 in wide by 8.60 in tall.

Primary grid: six columns of 0.75 in with 0.18 in gutters. A twelve-column micro-grid is the same field split in half, for tags, journal columns, and captions. Body text uses the full live width. A chapter does not wrap prose beside the motif.

```css
@page {
  size: 7in 10in;
  margin-top: 0.70in;
  margin-bottom: 0.70in;
  margin-outside: 0.70in;
  margin-inside: 0.90in;
}
```

Bleed is 0.125 in, and only on the cover and on art that is designed to bleed (the part-opener headband). Text pages and journal pages do not bleed.

Running head, Calibri 9 pt charcoal: part title on the verso, chapter title on the recto, set 0.42 in from the trim so it sits inside the head margin. Folio at the foot, outer corner, same face and size, with a 0.5 pt copper rule 4 pt long beside it. The folio is a number; the copper mark is decoration.

## Motif language

Every drawing is an original line illustration: ink contour, a copper accent, and at most one second accent (teal, burgundy, or gold). Fills are flat parchment, ivory, or a single accent. No gradients, no photo collage, no stock icon redrawn and renamed.

The shared vocabulary is paired circles, keys, doors, paths, constellations, and paper ephemera (letters, tickets, cards, pages). A chapter motif depicts that chapter’s premise, as already written in `assets/ART_MAP.json`. A part opener is a room or a place, not a larger copy of one of its chapters. A signature hero is a full scene with enough objects to carry an evening.

Figures, when they appear, are anonymous adults in ordinary clothes, seen small or in part. No named characters, no celebrity likenesses, no cartoon mascots.

## Chapter motif

Placed size: **2.20 in wide**, no taller than 1.80 in. The width is the constant so every chapter template matches.

Placement: centered at the top of the live area on the chapter opener, then 0.18 in of parchment, then the chapter number and title at full measure. The motif does not sit in the outer margin and does not intrude on the gutter.

SVG:

- File: the path already stored on that entry in `assets/ART_MAP.json`
- `viewBox="0 0 220 180"` (use a shorter height only when the drawing needs air; never wider than 220)
- Transparent ground
- Ink stroke `#241F1C` at 1.6 viewBox units; accent stroke at the same weight
- Flat fills only from the palette
- No external images, no scripts, no font dependency. If the assigned motif includes a word (yes, no, maybe, pass), outline that word and repeat it in the alt text
- Alt text is the `alt` string already in `assets/ART_MAP.json`, copied into `assets/ASSET_MANIFEST.csv`

A functional diagram (a turn order, a timeline, a floor plan the chapter actually uses) is a separate asset at up to 5.40 in wide. It is not a substitute for the motif, and its labels match the written mechanics.

## Part-opener composition

Each part opens on a recto. The page is parchment. A midnight headband occupies the top 1.85 in of the trim and may bleed at the head, fore-edge, and gutter. Inside the band, inset to a 0.45 in safe area: “Part 01” in Calibri 11 pt gold, then the part title in Palatino Linotype 26 pt ivory, two lines maximum.

Below the band the ground is parchment. The scene sits in a frame 5.40 in by 4.40 in, aligned to the live area, with a 0.75 pt copper hairline. SVG `viewBox="0 0 540 440"`, stroke about 2.2 viewBox units (about 1.6 pt on the page). File: `assets/parts/01-opener.svg` through `assets/parts/13-opener.svg`.

Under the frame: a short invitation in Georgia 11.5/16 ink, four lines maximum, on parchment. Then three guideposts in Calibri 9.5 pt charcoal, labeled with words: Lighter, Stay, Deeper. A teal or copper dot may sit beside a guidepost; the word is the signal.

The invitation is never set on midnight. The headband is the only dark field on the opener.

Scenes, emotional themes, and one-sentence draw briefs are in `PART_OPENERS.md`.

## Cover architecture

Artboard for front and back, including bleed: 7.25 in by 10.25 in. Trim is the center 7.00 by 10.00. Type and the emblem stay at least 0.45 in inside the trim.

**Front.** Midnight full bleed. Two copper hairlines, 0.5 pt, 6 pt apart, inset 0.55 in from trim. In the upper third, an original emblem: two overlapping circles, a key, and a few gold stars, drawn in the same line language as the chapters. Title, Palatino Linotype Bold, ivory, optically centered slightly above the middle. One subtitle line in Palatino Linotype Italic, parchment, 13 pt. No couple, no bed, no script wedding lettering, no map.

**Spine.** Width comes from the final page count, paper, and printer. Until those exist, any width study is a labeled mockup (`assets/covers/spine-mockup.svg`) and stays out of the release PDF. Treatment when the spine is real: midnight, title in Palatino ivory reading top to bottom, a copper hairline near the head, edition mark in Calibri at the foot. If the spine is under 0.35 in, set the title only.

**Back.** Midnight ground. Invitation in Georgia 12/16 ivory, kept short and true. The thirteen part names in Calibri 9 pt parchment, as a list, not a puzzle. A 2.00 by 1.20 in clear box at the lower right is reserved for a barcode; leave it empty and label the guide “barcode reserved.” No false barcode, no false review quotes.

**Title page.** Interior, parchment ground, no bleed. The emblem at 1.60 in, then the title in Palatino 32 pt ink, then edition line in Calibri 9 pt charcoal.

Files: `assets/covers/front.svg`, `assets/covers/back.svg`, `assets/covers/title-page.svg`.

## Journal pages

Journal pages are for handwriting. The ground is parchment `#F6F1E7`. The writing block is ivory `#FBF8F2`. There is no midnight, charcoal, or navy field behind lines, and no full-bleed dark band on a journal page. A chapter opener’s headband does not continue onto the journal spread.

Rules are 0.6 pt, `#D9CFC0`, 0.32 in apart (room for an adult hand). They begin at least 0.15 in under the prompt and stop 0.05 in inside the live area so ink does not fall into the gutter. Prompts sit above the lines in Georgia 11/15 ink. Lines stay blank. Fictional examples, if a chapter needs one, are labeled fictional and live in the prose, not on the rules.

Partner regions use the six-column grid: Partner A on columns 1–3, Partner B on columns 4–6, 0.22 in between. Each region is headed “Partner A” or “Partner B” in Calibri 9 pt charcoal, with the letter repeated in a 0.22 in ink circle. Color does not identify the partner. When a prompt is shared, a full-width block is headed “Together,” with a 0.75 pt copper rule over the word. The word does the work.

A pause control is a 0.28 in ring stroked in `#3E6464`, 1.25 pt, with the word “Pause” or “Pass” in Calibri beside it. The ring without the word is not used.

Ink coverage on a journal page stays light: rules, a small motif no wider than 0.80 in if one is repeated from the chapter, and type. No solid panel larger than a 0.15 in rule. Optional paper grain, if used at all, is a separate 300 DPI texture under 8% ink, and it must leave ink-on-ivory contrast at or above 7:1. If the grain cannot hold that, omit it.

The same margins apply: 0.70 in outer edges, 0.90 in gutter.

## Tags, cards, and diagrams

Time, energy, and depth appear as words in Calibri. A small original mark may accompany the word (a clock, one to three bars, a shallow or deep line). The mark without the word is not used.

Yes / No / Maybe are three equal cards. Each card carries its word. A corner of copper, teal, or burgundy may echo the word; the corner is not the choice.

Index tabs are copper. The numeral is Calibri Bold 12 pt ivory (4.75:1 on copper). The part name also appears in the index list in ink, so a reader who cannot see the tab color still has the name.

Cards for play are 2.50 by 3.50 in, parchment ground, 1.5 pt copper border, title in Palatino 13 pt ink, metadata in Calibri 8.5 pt charcoal. Crop marks sit outside the card. Cut sheets use the same palette and do not depend on color to tell one card from another.

Diagrams use ink lines, Calibri labels, and the palette accents as secondary strokes. An arrow that matters is labeled. A door, a turn, or a score matches the chapter as written.

## Signature heroes

Six heroes, richer than the 2.20 in motifs and smaller than a part opener. Placed 5.40 in by 3.60 in at the opening of the signature, SVG `viewBox="0 0 540 360"`, file `assets/signatures/S01-hero.svg` through `assets/signatures/S06-hero.svg`. Flat color may include a midnight interior and a parchment light. Briefs are in `SIGNATURE_ART.md`.

## Accessibility

- Body, prompts, and part invitations meet AAA on their grounds (ink on parchment or ivory).
- Labels in charcoal on parchment meet AAA. Teal labels are 11 pt or larger. Gold type appears only on midnight or charcoal, at 11 pt or larger.
- Copper and gold do not carry small text on parchment.
- No choice, warning, partner, pause, or score is communicated by color alone. Words or outlines repeat it.
- Alt text is required for every informative figure and is stored in `assets/ASSET_MANIFEST.csv`. Chapter alts already live on each entry in `assets/ART_MAP.json`. Decorative rules and grain are marked decorative and get an empty alt.
- Heading order follows the book: part, chapter, section. A picture does not replace a heading.
- The pause ring, the pass door, and partner letters stay visible in grayscale because they have a stroke and a word.
- Links in digital editions are underlined or otherwise marked, not colored only.

## Print rules

- Interior journal and text pages print on parchment. Handwriting never sits on a full-bleed navy, midnight, or charcoal ground.
- Cover and the part-opener headband may be full-bleed midnight. The opener’s invitation and all journal lines stay on parchment.
- Motifs, openers, heroes, emblem, and diagrams are SVG. Raster is reserved for an optional grain at 300 DPI at the placed size.
- Minimum stroke on the page: 0.5 pt for a hairline rule, about 1.15 pt for a motif contour.
- Text black is ink `#241F1C`, not a four-color rich black.
- The print PDF is the light palette. There is no dark-mode inversion of journal pages.
- Spine geometry in the release file waits for the real bulk. A beautiful cover does not invent a spine width.
- Hex values above are the source of truth. If a later CMYK conversion shifts copper or gold, recheck the pairs in the contrast table before setting type on those fields.

## Page-level QA

Before a page is called done:

1. Trim is 7.00 by 10.00 in. Outer margins are 0.70 in. Gutter is at least 0.90 in. Nothing essential sits in the gutter or closer than 0.70 in to the fore-edge, head, or foot.
2. Type is Palatino Linotype, Georgia, or Calibri, from the system, with no embedded font file.
3. Body and prompts are ink on parchment or ivory. A journal page has no dark full-bleed.
4. The chapter motif is about 2.20 in wide, matches its `ART_MAP.json` sentence, and does not collide with the title or the gutter.
5. The part opener uses the headband-plus-parchment composition and the scene from `PART_OPENERS.md`, not a blown-up chapter motif.
6. Color is never the only carrier of meaning. Pause, Pass, Partner A, and Partner B are written out.
7. Alt text is in the manifest. Decorative rules are marked decorative.
8. The drawing is original: no copyrighted character, no scavenger-hunt trail, no romance-cover clinch.
9. Lines on a journal page are 0.32 in apart, blank, and long enough to write on.
10. A signature hero matches `SIGNATURE_ART.md` and is 5.40 by 3.60 in.

## Coordination

The illustrator draws the locked chapter motifs, the thirteen openers, the six heroes, and the cover from these briefs and from `ART_MAP.json`. The publication engineer implements the trim, the 0.70 in outer margins, the 0.90 in gutter, the type stacks, the journal rules, and the headband from this file. Alt text and rights go in `assets/ASSET_MANIFEST.csv`. A change to a hex value or a motif subject starts in `PALETTE_LOCK.md` or `ART_MAP.json`, not as a local restyle.
