# Phase 3 art audit

Art-director recommendations for the existing Night Library drawings. The owner has not approved these decisions, and nothing here is an owner sign-off.

Contact-sheet page screenshots are not produced in this pass. No SVG file was edited. The Night Library palette is unchanged.

## Scope and method

Reviewed 130 files: `assets/covers/cover-front.svg`, `assets/covers/cover-back.svg`, `assets/covers/title-page.svg`, `assets/parts/01-opener.svg` through `13-opener.svg`, `assets/signatures/S01-hero.svg` through `S06-hero.svg`, and `assets/chapters/001/motif.svg` through `108/motif.svg`.

Each file was checked as SVG against `assets/styles/DESIGN_SYSTEM.md`, the locked sentence in `assets/ART_MAP.json`, `assets/styles/PART_OPENERS.md`, or `assets/styles/SIGNATURE_ART.md`. The check was well-formed XML, palette colors, viewBox, stroke weight at the placed size, and whether the picture is the assigned subject. A repeated key, door, cup, or chair is the shared vocabulary. It is a uniqueness failure only when two assets are the same picture.

Every decision is `keep`, `improve`, or `replace`. The one reason is subject match, line weight, uniqueness, or a broken file.

## Counts

| Decision | Count |
| --- | ---: |
| keep | 117 |
| improve | 10 |
| replace | 3 |
| **total** | **130** |

No file is a broken file. No file is scored for uniqueness. All 3 replaces are subject match. Of the 10 improves, 8 are subject match and 2 are line weight.

## Replace list

| File | Reason |
| --- | --- |
| `assets/chapters/005/motif.svg` | Subject match. The key, spoon, ticket, and star are separate objects. They do not form a question mark. |
| `assets/chapters/024/motif.svg` | Subject match. The phone stands upright and face-forward. The chapter asks for a phone lying face down. |
| `assets/chapters/061/motif.svg` | Subject match. The drawing is a cloud, a small rectangle, and a frown. It does not show a need outlined inside the shape of a joke. |

## Noted, not scored as a new decision

- Motif files use `viewBox="0 0 440 280"` and a 3.2-unit ink contour. Placed at 2.20 in wide, that contour is about 1.15 pt, which is the print weight in the design system. The written token `0 0 220 180` is not what these files use. That difference is not scored as a line-weight failure.
- Part openers are `0 0 540 440`. Signature heroes are `0 0 540 360`. Cover artboards are 522 by 738 pt (7.25 by 10.25 in, including bleed). The title page is 504 by 720 pt (7 by 10 in).
- The title-page emblem is about 2.2 in across. The design system asks for 1.60 in. The emblem is the right drawing, so the file stays `keep`.
- On disk the covers are `cover-front.svg` and `cover-back.svg`. The design-system filenames `front.svg` and `back.svg` are not the files that exist. The files that exist are the ones reviewed.

## Covers

- `assets/covers/cover-front.svg` — **keep** — subject match. Midnight ground, two copper hairlines, two circles, a key, gold stars, the title, and one subtitle.
- `assets/covers/cover-back.svg` — **keep** — subject match. Short invitation, the thirteen part names as a list, and an empty box labeled barcode reserved.
- `assets/covers/title-page.svg` — **keep** — subject match. Parchment ground, the night-library emblem, the title, and the edition line.

## Part openers

- `assets/parts/01-opener.svg` — **keep** — subject match. A library table, two lamps of unequal height, two book stacks, and blank pages down the center.
- `assets/parts/02-opener.svg` — **keep** — subject match. A night window with the shade at the sill, one lamp, and an empty chair.
- `assets/parts/03-opener.svg` — **keep** — subject match. Two cups, an open pocket watch, and one teal arc over the table.
- `assets/parts/04-opener.svg` — **keep** — subject match. Two different keys on one hook, a lit wall lamp, and a closed door.
- `assets/parts/05-opener.svg` — **improve** — subject match. The burgundy drape, dark room, and low lamp match. The shoes are four ellipses.
- `assets/parts/06-opener.svg` — **improve** — subject match. The board and the crowned pawn match. The piece off the board reads as a stone, not a knight.
- `assets/parts/07-opener.svg` — **keep** — subject match. An orrery of a stair, a seed, an eye, and a lamp above a blank journal.
- `assets/parts/08-opener.svg` — **keep** — subject match. A covered porch in the rain, an open door, two mugs, and a lantern.
- `assets/parts/09-opener.svg` — **keep** — subject match. A dusk platform, two tickets in one hand, one suitcase, and a board that reads only KA.
- `assets/parts/10-opener.svg` — **keep** — subject match. A windowsill with a gold-edged photograph, a warm cup, and a blank page.
- `assets/parts/11-opener.svg` — **keep** — subject match. Unlabeled drawers, one of them open on a single teal shell.
- `assets/parts/12-opener.svg` — **keep** — subject match. Two chairs at a dawn window and a pencil path toward the sun.
- `assets/parts/13-opener.svg` — **keep** — subject match. A screw press, a tray of blank cards, copper type, one card drying, and a midnight shadow under the bench.

## Signature heroes

- `assets/signatures/S01-hero.svg` — **improve** — subject match. The long table, lowering lamps, facing chairs, and face-down far card match. Rules from the near cards run off the cards and across the chairs.
- `assets/signatures/S02-hero.svg` — **keep** — subject match. One lamp, a record on the player, a burgundy throw, two glasses, and a dark window.
- `assets/signatures/S03-hero.svg` — **improve** — subject match. The two chairs, coat, receipt, and blank Tuesday match. The pot between the chairs reads as a lampshade, not a teapot.
- `assets/signatures/S04-hero.svg` — **keep** — subject match. A night hall opening onto a lit kitchen, a dark walk with a coat, and a quiet chair.
- `assets/signatures/S05-hero.svg` — **keep** — subject match. A sealed capsule with date scratches, a photograph, a letter, and a key.
- `assets/signatures/S06-hero.svg` — **keep** — subject match. A row of unmatched glasses, one raised, one burgundy, a night window, and a blank card at the far end.

## Chapter motifs

- `assets/chapters/001/motif.svg` — **keep** — subject match. Two empty chairs and a question-mark constellation.
- `assets/chapters/002/motif.svg` — **keep** — subject match. A closed book, a loose ribbon, and a lamp.
- `assets/chapters/003/motif.svg` — **keep** — subject match. Five stones along a path, the last one in a hand.
- `assets/chapters/004/motif.svg` — **keep** — subject match. An adult coat and a paper boat on the same hook.
- `assets/chapters/005/motif.svg` — **replace** — subject match. The key, spoon, ticket, and star are separate objects. They do not form a question mark.
- `assets/chapters/006/motif.svg` — **keep** — subject match. Three plinths and one empty frame.
- `assets/chapters/007/motif.svg` — **keep** — subject match. A path that forks and then rejoins.
- `assets/chapters/008/motif.svg` — **keep** — subject match. A ruled page with a half-mask in the margin.
- `assets/chapters/009/motif.svg` — **keep** — subject match. An envelope with the flap lifted.
- `assets/chapters/010/motif.svg` — **keep** — subject match. Layered ground and a lamp at the lowest line.
- `assets/chapters/011/motif.svg` — **keep** — subject match. A coat with a teal garment showing underneath.
- `assets/chapters/012/motif.svg` — **keep** — subject match. A slip and an unused seal set apart from it.
- `assets/chapters/013/motif.svg` — **improve** — subject match. The speech bubble and the door are right. The word Pass collides with the door stile.
- `assets/chapters/014/motif.svg` — **keep** — subject match. A cup with a copper crack.
- `assets/chapters/015/motif.svg` — **keep** — subject match. A chair drawn small inside a large room.
- `assets/chapters/016/motif.svg` — **keep** — subject match. Armor on a stand beside a table.
- `assets/chapters/017/motif.svg` — **keep** — subject match. Two profiles and four minute-marks, with no hearts.
- `assets/chapters/018/motif.svg` — **keep** — subject match. Closed mouths, two palms, and a copper phrase in the air.
- `assets/chapters/019/motif.svg` — **keep** — subject match. Two breath arcs meeting over one bench.
- `assets/chapters/020/motif.svg` — **keep** — subject match. An open speaker, a still listener, and lines of words between them.
- `assets/chapters/021/motif.svg` — **improve** — subject match. The blindfold is offered, not worn. The hallway reads as an empty frame.
- `assets/chapters/022/motif.svg` — **keep** — subject match. An open palm hovering over a dashed line.
- `assets/chapters/023/motif.svg` — **keep** — subject match. Two figures in a still embrace and one minute-mark.
- `assets/chapters/024/motif.svg` — **replace** — subject match. The phone stands upright and face-forward. The chapter asks for a phone lying face down.
- `assets/chapters/025/motif.svg` — **keep** — subject match. A key, cup, page, cloth, spoon, and lamp, with no labeled boxes.
- `assets/chapters/026/motif.svg` — **keep** — subject match. Notes stacked from plain cards to one card that carries a lamp.
- `assets/chapters/027/motif.svg` — **keep** — subject match. A clock stopped on one hour.
- `assets/chapters/028/motif.svg` — **keep** — subject match. A tilted manual with three warning marks.
- `assets/chapters/029/motif.svg` — **keep** — subject match. A menu card, a kettle, and four weather marks.
- `assets/chapters/030/motif.svg` — **keep** — subject match. A card kept on one side of a divided table.
- `assets/chapters/031/motif.svg` — **keep** — subject match. A sealed letter beside a row of year-ticks.
- `assets/chapters/032/motif.svg` — **keep** — subject match. Seven ordinary objects, each with one copper mark.
- `assets/chapters/033/motif.svg` — **keep** — subject match. One timeline and two sparks set apart.
- `assets/chapters/034/motif.svg` — **keep** — subject match. Three equal cards whose words read yes, no, and maybe.
- `assets/chapters/035/motif.svg` — **keep** — subject match. Small notes leading to a set table.
- `assets/chapters/036/motif.svg` — **keep** — subject match. A record, a citrus slice, a cloth, a glass, and a lamp.
- `assets/chapters/037/motif.svg` — **keep** — subject match. A closed locket on an open palm.
- `assets/chapters/038/motif.svg` — **keep** — subject match. Two pairs of feet and an empty music stand.
- `assets/chapters/039/motif.svg` — **keep** — subject match. One doorway with two different openings.
- `assets/chapters/040/motif.svg` — **keep** — subject match. A room plan, a patch of light, and a closed door.
- `assets/chapters/041/motif.svg` — **keep** — subject match. Three story cards, the middle one tilted.
- `assets/chapters/042/motif.svg` — **keep** — subject match. A fork with a different hat on each path.
- `assets/chapters/043/motif.svg` — **keep** — subject match. Two paddles and a cake crossed out.
- `assets/chapters/044/motif.svg` — **keep** — subject match. Two coats whose sleeves are on the wrong arms.
- `assets/chapters/045/motif.svg` — **keep** — subject match. A cup on a podium and a small gavel.
- `assets/chapters/046/motif.svg` — **keep** — subject match. A planet and two homemade flags.
- `assets/chapters/047/motif.svg` — **keep** — subject match. Three doors labeled truth, dare, and discover, each with a key.
- `assets/chapters/048/motif.svg` — **keep** — subject match. Sealed envelopes sitting on a week grid.
- `assets/chapters/049/motif.svg` — **keep** — subject match. One lived road and a second road drawn dashed beside it.
- `assets/chapters/050/motif.svg` — **keep** — subject match. Ordinary objects arranged on a table.
- `assets/chapters/051/motif.svg` — **keep** — subject match. A portrait whose outline is still dashed.
- `assets/chapters/052/motif.svg` — **keep** — subject match. A stone split open onto a smaller stone.
- `assets/chapters/053/motif.svg` — **keep** — subject match. An empty bank of seats and one figure on the stage.
- `assets/chapters/054/motif.svg` — **keep** — subject match. A ruled page and a small beast in the margin.
- `assets/chapters/055/motif.svg` — **keep** — subject match. A list, a mountain, and a plate with a cup.
- `assets/chapters/056/motif.svg` — **keep** — subject match. Three question-mark constellations and no answer key.
- `assets/chapters/057/motif.svg` — **keep** — subject match. A manual, a kettle, and a folded blanket.
- `assets/chapters/058/motif.svg` — **keep** — subject match. Two speech shapes that do not match, and a pencil.
- `assets/chapters/059/motif.svg` — **keep** — subject match. Two chairs angled toward each other.
- `assets/chapters/060/motif.svg` — **keep** — subject match. A bench, a spool, and thread, with no arrow.
- `assets/chapters/061/motif.svg` — **replace** — subject match. The drawing is a cloud, a small rectangle, and a frown. It does not show a need outlined inside the shape of a joke.
- `assets/chapters/062/motif.svg` — **keep** — subject match. A four-room plan with sun in two rooms and wind in two.
- `assets/chapters/063/motif.svg` — **keep** — subject match. A marked card and a starred card shown as two sides of one note.
- `assets/chapters/064/motif.svg` — **keep** — subject match. A jar of coins, with one coin on its way out.
- `assets/chapters/065/motif.svg` — **improve** — subject match. The closed door is right. The two hands on the handle read as one knot.
- `assets/chapters/066/motif.svg` — **improve** — subject match. The paper boat does not read as a folded banknote.
- `assets/chapters/067/motif.svg` — **keep** — subject match. Two overlapping circles and a third circle outside them.
- `assets/chapters/068/motif.svg` — **keep** — subject match. A die, a coin, and a card, each with a veto mark.
- `assets/chapters/069/motif.svg` — **keep** — subject match. Loose parts at both sides and one stool built in the middle.
- `assets/chapters/070/motif.svg` — **keep** — subject match. Spectacles with a landscape in one lens.
- `assets/chapters/071/motif.svg` — **keep** — subject match. A Tuesday grid with one seal on the page.
- `assets/chapters/072/motif.svg` — **keep** — subject match. A low wall and two pairs of legs stepping over it.
- `assets/chapters/073/motif.svg` — **keep** — subject match. Two pages, each marked 1.
- `assets/chapters/074/motif.svg` — **keep** — subject match. A small gesture and the same gesture enlarged in a lens.
- `assets/chapters/075/motif.svg` — **keep** — subject match. A ticket, a speech shape, and a frame on one string.
- `assets/chapters/076/motif.svg` — **keep** — subject match. The same profile in two frames, the second one changed.
- `assets/chapters/077/motif.svg` — **keep** — subject match. A long line with knots along it.
- `assets/chapters/078/motif.svg` — **keep** — subject match. A card with an address square and a pencil beside it.
- `assets/chapters/079/motif.svg` — **keep** — subject match. A line of notes running over a row of year-marks.
- `assets/chapters/080/motif.svg` — **keep** — subject match. One circled day, with sun and rain beside the grid.
- `assets/chapters/081/motif.svg` — **keep** — subject match. A question box and a hand setting one slip aside.
- `assets/chapters/082/motif.svg` — **keep** — subject match. A balance scale left uneven.
- `assets/chapters/083/motif.svg` — **keep** — subject match. A pocket turned out around one teal marble.
- `assets/chapters/084/motif.svg` — **keep** — subject match. A standing figure and a dark figure given a face.
- `assets/chapters/085/motif.svg` — **keep** — subject match. Three doors under a handwritten if.
- `assets/chapters/086/motif.svg` — **keep** — subject match. A club pin and two cups, with no gavel.
- `assets/chapters/087/motif.svg` — **keep** — subject match. Four steps, each carrying a question mark.
- `assets/chapters/088/motif.svg` — **keep** — subject match. A napkin equation left unfinished.
- `assets/chapters/089/motif.svg` — **keep** — subject match. A blank page and two pens.
- `assets/chapters/090/motif.svg` — **keep** — subject match. A postcard with a stamp and an unwritten message.
- `assets/chapters/091/motif.svg` — **keep** — subject match. A sheet titled MORE OF, with no second column.
- `assets/chapters/092/motif.svg` — **keep** — subject match. Two kites on different strings.
- `assets/chapters/093/motif.svg` — **keep** — subject match. An open suitcase holding a page and a ticket.
- `assets/chapters/094/motif.svg` — **keep** — subject match. An open door between a bare branch and new leaves.
- `assets/chapters/095/motif.svg` — **keep** — subject match. A short card with a single line on it.
- `assets/chapters/096/motif.svg` — **keep** — subject match. One written page and a facing page still blank.
- `assets/chapters/097/motif.svg` — **keep** — subject match. A label peeling back and a fan brush.
- `assets/chapters/098/motif.svg` — **keep** — subject match. Two worn cups and three blank cards.
- `assets/chapters/099/motif.svg` — **improve** — line weight. The three postcards are stroked under half a point at the 2.20 in placed width.
- `assets/chapters/100/motif.svg` — **keep** — subject match. An inner weather shape and a closed umbrella.
- `assets/chapters/101/motif.svg` — **keep** — subject match. Two different hats over one card.
- `assets/chapters/102/motif.svg` — **keep** — subject match. Two panels, one with a clock and one with an eye, each ruled like a label.
- `assets/chapters/103/motif.svg` — **keep** — subject match. A room, one solid clue and one dashed clue, and two keys on one arc.
- `assets/chapters/104/motif.svg` — **keep** — subject match. A small map and a storm-shaped card.
- `assets/chapters/105/motif.svg` — **keep** — subject match. Five tickets, each with a different code.
- `assets/chapters/106/motif.svg` — **improve** — line weight. The hundred beads are stroked at about 0.29 pt, under the half-point print minimum.
- `assets/chapters/107/motif.svg` — **keep** — subject match. A ruled page and one star.
- `assets/chapters/108/motif.svg` — **keep** — subject match. A corridor of doors and keys that can be offered or kept.
