# Our Story — companion architecture

Our Story is a separate keepsake volume for the couple who is using The Closer Project. It is a companion to the main book, not a second copy of the chapters and not a scorecard. The main book teaches and hosts an activity. This volume holds what the two people choose to write afterward, then and later.

No real memory is supplied here. Prompts are blank until the people who lived the hour fill them. Private answers stay private. The names Rowan and Vale appear only in one clearly marked fictional layout sample.

Builders assemble the printable and editable companion from this file, `journal/PROMPT_BANK.md`, and `journal/templates/`. Writers later paste bank prompts into each chapter’s Our Story block. They do not invent the couple’s journal.

## 1. Front matter

Print the companion with its own title page so it cannot be mistaken for the main volume. Suggested order:

1. **Half title.** Our Story.
2. **Companion statement.** “A personal companion to The Closer Project. The activities live in the main volume. This book is the record you two choose to keep.”
3. **Title page.** Our Story. A companion journal. Room for two names or initials, left blank. No fictional names on the title page.
4. **How to use the book.** Date what you write. Skip what you do not want stored. Passing, pausing, and changing a prompt are ordinary. A filled page is a memory aid, not a grade.
5. **Two voices.** The equality rules in the next section, in plain language.
6. **Privacy and consent.** Private pages are optional to share. Either person may close a page. Sensual notes (activities 033–040) are discreet and optional. A written yes is not a promise to act, and a game result is not consent to touch.
7. **Keeping it for years.** Date every entry. Add repeat sheets rather than erasing. Attach keepsakes with a caption. Once a year, write a chapters-of-us recap.
8. **Map of the sheets.** Session log, partner page, shared page, revisit, chronology, milestone, memento, letter, and the special sheets tied to single activities.
9. **Cross-reference.** All 108 IDs in catalog order, with part title, activity title, and the special sheet if one exists. Titles match `source/experience_catalog.json`. Premises stay in the prompt bank. Signature sessions S01–S06, when they exist, use these same sheets and sit in their own short cross-reference. They do not replace 001–108.
10. **Blank dedication.** Eight handwriting rules. No suggested sentiment.
11. **Blank start page.** Date we began this companion, place, initials if wanted, and eight rules for a first sentence if they want one.

Front matter contains no sample answers except the fictional chronology line specified below, and that line stays in the builder’s notes unless a layout proof needs it. Label any such proof “Fictional. Rowan and Vale are not the readers.”

## 2. How the two voices stay equal

Partner A and Partner B are seats for a single sitting, not genders, ranks, or permanent identities. Record initials on the session log. Swap seats at the next sitting if you like.

- Each person gets a partner page with the same paper size, margins, type size, and number of handwriting rules.
- The prompts differ. The prompt bank gives each seat language suited to that activity. Do not print the same prompt on both pages.
- On a facing spread, neither page is labeled primary. Verso and recto use the same header.
- “My experience” is the heading on both pages.
- The shared page is joint. Either person may write. Both may add. Neither rewrites the other’s sentences. Initials beside a paragraph are welcome and optional.
- The default for a partner page is private. Sharing it is a second, explicit choice. Say that once on the page, in ordinary sentences.
- In print, private pages should be easy to keep apart: a disc-bound or binder companion, or a perforated signature that can move to a personal stack. In the local export, each voice is its own file.
- The chronology indexes a private page only when the writer marks it indexable.

Asymmetric activities still give both people a full page. If one seat guides and the other walks, or one speaks and the other listens, the prompts name those seats and the line counts match. If they swap roles, they use another copy of the partner page rather than squeezing both roles onto half the lines.

## 3. What a single visit contains

Use this order for every activity, including a repeat:

1. `session-log.md` — facts of the sitting, first session or later.
2. `partner-page.md` — Partner A, then Partner B, equal.
3. `shared-page.md` — the joint narrative.
4. A special sheet only when the activity calls for it (see the table below).
5. `memento-caption.md` if something is kept.
6. One new line on `chronology-index.md`.
7. Later, `revisit-then-now.md` when they want a long comparison. Repeating the session set is always allowed; the then-versus-now sheet is extra, not a cap.

Attempt 1 is the first session. There is no last attempt.

## 4. Shared pages

The shared sheet asks for narrative: what happened, the unexpected moment, a line worth keeping, what you discovered, what you want remembered, an optional “what next,” and a pointer to a memento. The activity-specific shared prompt from the prompt bank prints above “What actually happened.”

Checkboxes are limited to facts (done, paused, passed; share or keep). The story fields are ruled lines. Do not add points, streaks, or compatibility totals.

## 5. Repeat logs

The repeatable pack is the session log, the partner page, the shared page, and the then-versus-now sheet, printed without a specific ID filled in. The publication build should later emit that pack as editable source plus print-ready PDF and DOCX under a repeatable-session label. Unlimited copies. The couple writes the ID, the title, and the attempt number by hand.

A repeat records: attempt number, date, version played (short, standard, extended, or another label they invent), what changed, and a new memory. Old pages stay. Correction belongs on a new sheet, dated, not scribbled over the earlier hand unless the writer is amending their own line.

Multi-day activities (notably 032, 048, and 099) use one session log for the whole stretch, with the date range in the date field, plus a short dated note inside the shared narrative for each day they care to mention. They are not productivity charts. Blank days are unmarked, not failures.

## 6. Chronology index

The index is the spine of the memoir. One entry per sitting:

- Date
- Activity ID and title
- Attempt number
- Place
- One optional line the writers want the index to hold
- Where to find the pages in this companion

Copy the index sheet forever. When they recopy for legibility, they may sort by date. A second copy sorted by ID is useful and optional. The index does not narrate growth for them. The optional line can be blank.

The annual recap and the private export both read this index. Private pages omitted from the index stay out of the shared keepsake.

## 7. Milestones

A milestone is a dated page for a moment they want to find later: a move, a repair, a trip, a decision, an anniversary, a hard week they got through, a joke that became permanent. It is not an award and not a progress level.

The page can point at an activity ID when the moment grew out of one, or it can stand alone. Milestones also get a chronology line, with the ID cell reading “milestone” when no activity applies.

## 8. Memento slots

Physical keepsakes (tickets, drawings, photos, the object they built in 069) get a caption sheet and a pocket or envelope. The caption holds the date, the activity ID if any, who may see it, and where the object lives.

Digital files stay under `journal/private/mementos/` on the couple’s machine. The caption stores a local filename, not a web address. The companion does not upload photos. Rights language on the sheet is simple: we made this, or we have the right to keep a copy, and we are not granting anyone else the right to publish it.

If a memento is private to one person, the caption lives with that person’s pages and the chronology line is omitted unless they mark it indexable.

## 9. Annual chapters-of-us recap

Once a year, or on a date they choose, they write a recap. Activity 094, The Annual Reintroduction, can be the conversation that feeds the recap. The recap can also be written in a year they never opened 094. The prompts below are the recap itself. Paste them into two partner pages and one shared page, with a fresh chronology line (`ID: annual`, title: Chapters of us, plus the year).

Each partner page, equal rules, private unless shared:

- **Partner A.** What this year contained for me, in scenes rather than a verdict, and what I want more of next year.
- **Partner B.** What this year contained for me, including a change in what I need or enjoy, and what I want protected next year.

Shared page:

- The year as a chapter: a few scenes, a difficulty we are willing to name, a delight, and what we are taking into next year.
- Pointers only: dates from the chronology, milestone titles, mementos added. No ranking of who grew more.

Then versus now, optional: lay last year’s recap beside this one and use `revisit-then-now.md`.

Handwriting: paste each prompt onto the matching template and keep that template’s rules. Each prompt gets at least eight rules, printed at least 0.32 inch apart. At letter size this recap is four pages (two partner pages and a shared sheet that runs to a second page), plus any memento captions they add.

```journal
annual: chapters-of-us
lines_per_prompt: 8
line_spacing_min_in: 0.32
sheets: [partner-page, shared-page, revisit-then-now]
```

## 10. Special sheets

| Sheet | Activities | Role |
| --- | --- | --- |
| `postcard.md` | 099 The Invisible Postcards | One note per noticed moment, kept until the agreed exchange |
| `yes-no-maybe.md` | 034 The Yes, No, Maybe Game | Discreet, optional, comparable without pressure |
| `hundred-points.md` | 106 The Intimacy Negotiators | 100 imaginary points and an evening nobody is owed |
| `museum-label.md` | 006 The Museum of Me; 102 The Museum of Unsaid Things | One label per exhibit; empty cases allowed |
| `escape-clue-sheet.md` | 103 The Relationship Escape Room | Cooperative puzzles in an agreed place |
| `civilization-charter.md` | 104 The Two-Person Civilization | Founding articles and a later amendment |
| `letter-page.md` | Writing activities, especially 008, 012, 028, 031, 078, 095 | A full letter surface |
| `revisit-then-now.md` | Any ID, any later year | Long comparison |

Activity 103 is a cooperative puzzle the two of them build and solve together from personal history, knowledge of each other, and complementary skills. The clue sheet stays in the room they agreed on. It does not send either person searching a town or a house for hidden objects.

Activities 033–040 are discreet and optional in the prompt bank and on any sheet those IDs use. The yes/no/maybe sheet states that a change of mind replaces the old mark.

## 11. Print rules for handwriting

Measure the printed page, not the markdown.

- Handwriting baselines are at least **0.32 inch** apart (about 23 points). Prefer 0.36 inch when the signature still closes. Never tighten leading to fit a template on one sheet.
- Eight rules are the minimum under a story prompt. Add a continuation sheet when the answer needs more.
- Single-fact blanks (date, place, ID) each occupy their own line, also at least 0.32 inch from the next baseline, so the form itself can be filled with a pen.
- Suggested page: US Letter. Margins at least 0.85 inch inside (binding), 0.70 inch outside, 0.70 inch top, 0.75 inch bottom. Rules stay out of the gutter.
- Usable height at those margins is about 9.55 inches. Eight rules consume 2.56 inches before the prompt text. A partner page with two eight-rule prompts fits one sheet. A shared page with six story fields is three sheets. A then-versus-now spread is two sheets. Do not solve overflow by shrinking the gap.
- Rules are underscores or true baseline rules, long enough for a full sentence and short of the outer margin. No tiny boxed grids for stories.
- Header on every continuation: Our Story, activity ID, date, attempt, whose page.
- QA: print one partner page and one shared continuation, measure three consecutive baselines, and fail the export if any gap is under 0.32 inch.

In these source files, eight rules appear as a blockquote of underscores. A fenced `journal` block at the top of each template tells the builder the same contract in fields a script can read. Expand the fence; do not drop the rules.

```journal
line_spacing_min_in: 0.32
min_rules_per_prompt: 8
on_overflow: add a sheet
qa: measure printed baselines
```

## 12. How a private local export works later

Real notes never enter Git and never enter the public release. `.gitignore` already excludes `journal/private/`, `**/personal-notes/`, and `**/*_PRIVATE_MEMOIR_*`. Do not add an exception that puts those paths back.

The couple’s notes, if they choose a digital copy, live only here:

```text
journal/private/sessions/<YYYY-MM-DD>-<ID>-attempt-<N>/
  session.yaml      metadata, no story bodies
  partner-a.md      one voice
  partner-b.md      the other voice
  shared.md         joint narrative
  mementos.yaml     local filenames and captions
journal/private/milestones/
journal/private/annual/
journal/private/mementos/
journal/private/exports/
```

This architecture does not create those session files and does not invent their contents.

`session.yaml` shape, version `our-story-session/1`:

```yaml
schema: our-story-session/1
activity_id: "001"          # or "annual" or "milestone"
title: ""                   # catalog title, copied by them if they wish
attempt: 1
date: ""
time: ""
place: ""
version_played: ""          # short, standard, extended, or their label
mood: ""                    # optional words, never a required scale
intention: ""
status: ""                  # done, paused, or passed
initials:
  partner_a: ""
  partner_b: ""
index_me: false             # chronology includes this only when true
share:
  partner_a: private        # private or shared
  partner_b: private
  shared: shared
special_sheet: ""           # postcard, yes-no-maybe, and so on
```

Story text stays in the markdown files, whose headings match the templates. A later local tool may create the folder and the blank files. It must not pre-fill answers.

**Export, when it is built, runs offline on their machine.**

1. Read only under `journal/private/`.
2. Write only under `journal/private/exports/`.
3. Name files so the existing ignore rule catches strays: `Our_Story_PRIVATE_MEMOIR_<YYYYMMDD>_shared.docx` and a matching `.pdf`.
4. Abort if the output path is not gitignored.
5. Do not `git add`, commit, push, or open a network connection.
6. Offer three local modes: shared keepsake (only items marked shared), one voice’s own copy, and a full local copy. All three remain under `journal/private/exports/`.
7. Order the shared keepsake by date using the chronology, with a second optional order by activity ID.
8. The release build of The Closer Project uses the blank templates and, if it needs a layout proof, a fictional Rowan and Vale sample stored outside `journal/private/` and labeled fictional. The release entry point errors if it is pointed at `journal/private/`.
9. EPUB remains a reading edition of the main book. Long notes belong to this companion’s DOCX and PDF.
10. Fillable PDF fields, if a later build proves they save and reopen, write back into the same private folder. If a basic PDF reader cannot do that, ship the editable DOCX and the paper rules instead of promising form fields.

A fictional layout sample, not a memory of any real couple:

```yaml
# FICTIONAL. Rowan and Vale are not the readers. Do not commit this as anyone's journal.
schema: our-story-session/1
activity_id: "075"
title: "Our Greatest Hits"
attempt: 1
date: "2026-04-03"
place: "kitchen table"
version_played: standard
status: done
index_me: true
share:
  partner_a: private
  partner_b: private
  shared: shared
note: "Fictional shared line for layout only: they left burnt toast on the hits list and did not decide who was right."
```

## 13. What the chapter writers embed later

The prompt bank holds four prompts for each ID from 001 through 108: Partner A, Partner B, a shared narrative prompt, and a revisit prompt. Writers place them in the chapter’s `journal` fence. The chapter contract also asks for a second bullet under each partner. Use a narrower follow-up inside the same premise, or the second slot printed on `partner-page.md`. Do not replace the bank prompt with a generic feelings question, and do not demand that secrets be transcribed.

The shared fence in the chapter can keep the contract’s standing lines (what happened, the line worth keeping, what we discovered, what we might do next). The bank’s shared prompt is the activity-specific line above them.

## 14. File map

| Path | Purpose |
| --- | --- |
| `journal/COMPANION_STRUCTURE.md` | This architecture |
| `journal/PROMPT_BANK.md` | Prompts for IDs 001–108 |
| `journal/templates/*.md` | Blank printable sheets |
| `journal/private/` | Their notes, gitignored, never authored by this project |
