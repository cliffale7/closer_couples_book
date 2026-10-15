# Editorial closeout: contrast clusters

Text inspection of `## Before you begin`, `## The experience`, and `## Three ways to play` on branch `phase3/book-completion`. Not a human playtest. No chapter or signature was rewritten. IDs, titles, duration sentences, journal fences, and Notes were left as they stood. 108 chapter files and six signature files were still present after the inspection.

A cluster is **already distinct** when swapping the procedures would change the opening move, the turn, or the object you leave with. A new adjective in the hook was not treated as a difference. Where that test held, the prose was left alone.

Hashes below are SHA-256, first 12 hex characters, of those three sections concatenated. Recompute them with the command under Inspection.

## Inspection

From the repository root, hash `## Before you begin`, `## The experience`, and `## Three ways to play` for every ID in the table. The run that produced this closeout printed `chapters 108`, `signatures 6`, and `missing []`. No two IDs shared a practical-middle hash.

```python
import hashlib, pathlib, re
root = pathlib.Path(".")
files = list((root / "chapters").rglob("*.md")) + list((root / "signature").glob("S*.md"))
by_id = {re.match(r"^(S?\d+)", p.name).group(1): p for p in files}
print("chapters", len(list((root / "chapters").rglob("*.md"))))
print("signatures", len(list((root / "signature").glob("S*.md"))))

def section(text, head):
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == head)
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out).strip()

for i in ["001", "005", "081"]:  # replace with the full ID list in the table
    text = by_id[i].read_text(encoding="utf-8")
    blob = "\n".join(section(text, h) for h in [
        "## Before you begin", "## The experience", "## Three ways to play"])
    print(i, hashlib.sha256(blob.encode("utf-8")).hexdigest()[:12])
```

| id | practical-middle hash | first move in The experience |
| --- | --- | --- |
| 001 | `d9cb844be9cb` | Three questions a polite stranger could ask, drafted in silence. |
| 005 | `9d3ec8f038fc` | Three never-asked questions, spread across more than one kind. |
| 081 | `a204784a3b69` | Deal twelve slips, keep five, fold them into a bowl. |
| 041 | `5664fbe34585` | One teller builds three unlabeled stories. |
| 107 | `7d6d24651009` | Fix the true story and the one seam; sit on the slip. |
| 039 | `dd81a3705f0d` | Apart, one condition and five lines of a meeting. |
| 046 | `77749ad635b4` | One world, in a single sentence, from the menu or at that scale. |
| 006 | `3109a32f8c9c` | Four exhibits; each label has what it is, which stretch, why. |
| 102 | `9063e1e57899` | Fifteen quiet minutes; the two labels stay exact. |
| 073 | `063d581c149e` | About 10 minutes, no talking; five lines on the beginning. |
| 074 | `9ca0f59ea8a9` | About 8 minutes; up to five small memories. |
| 075 | `fed4ffa8edd0` | Slug lines into four columns only. |
| 076 | `045bc0a928e5` | About 5 minutes; four beats of a changed picture. |
| 077 | `a5b0d41bff9c` | Lay one line and mark years or chapters on it. |
| 078 | `e5f53f9339dd` | About 8 minutes apart; one thank-you in three sentences. |
| 079 | `9e9b44b5a1f7` | Liner notes before any sound. |
| 080 | `5cd720ded13f` | A facedown card with only the date. |
| 025 | `b76fc08502f3` | About 10 minutes apart; two items in each of three rows. |
| 028 | `f701c2ef9baf` | Parallel draft: situations, tells, maintenance. |
| 057 | `6a14cf1ce0ae` | A hard-day pattern under the seven headings. |
| 029 | `99a84c85f35a` | Every cell of the weather grid is a behavior. |
| 026 | `1abd28467bb3` | Round one is one obvious, true appreciation. |
| 105 | `f6121228f764` | A four-column decoder; the episode stays covered. |
| 030 | `69ba6ae47a79` | One compliment, then about 10 seconds before the receiving sentence. |
| 010 | `84c24b2432fd` | One fear; the surface line; the partner does not supply the next. |
| 052 | `3dcc568df0e5` | A three-line belief card written before anyone speaks. |
| 087 | `d36a800e90b6` | An ordinary sentence: the day, the lunch, the week ahead. |
| 097 | `b9c54f474a53` | One sentence: the reaction and the cause walked in with. |
| 009 | `ad0ce2f99e77` | The pause phrase, then one admission. |
| 020 | `d14ff7e4345d` | Name the topic and whether it is good news. |
| 013 | `fd3495b4358f` | Four kinds in view, then a harmless pre-check. |
| 016 | `5072be5f186c` | One modest topic, said in a sentence. |
| 017 | `9ffda36da742` | Sit face to face and look. No message is assigned. |
| 018 | `86001a8c007d` | Say the gesture assignment, touch out, then stop talking. |
| 032 | `340e362d2b5b` | Day zero is the receiver's map. |
| 048 | `ffefacdf1b6b` | Three missions, written apart, then sealed. |
| 099 | `3908bb14b378` | Blank sheets go where the other person will not read them. |
| 043 | `cc7826923323` | Private phrases about the other person's current habits. |
| 101 | `31734369ea2d` | One realistic, one funny, one gray scenario. |
| 089 | `f1d2b88c89fa` | Borrowed cards stay visible beside the new lines. |
| 104 | `32c3fd5b33e3` | Aim at ten principles, then draw events. |
| 055 | `d680e3317f8b` | A personal list; at least half ordinary or cheap. |
| 093 | `18cfea072f22` | A shared page, one line at a time, twelve or fewer. |
| 008 | `10d4fc14628d` | Simultaneous biographies, contradictions included. |
| 011 | `4e7c19094180` | One hidden part and conditions a person could offer. |
| 083 | `330d1a30900e` | A lens, then the assumption, the fact, and what it complicates. |
| 027 | `9e9355c68ea4` | One scene: place, shift, sentence not said. |
| 033 | `692fe103a7b0` | Three movements, in order, both people in the guest chair. |
| 031 | `ce3cd7998790` | The year goes in the first line of a letter. |
| 090 | `634ec1ad77d5` | One happy scene, past tense, that has not happened. |
| 098 | `07befe0b8eda` | One interviews; the other answers as the centenarian. |
| S05 | `7a3d158f26fd` | Seal pieces of this season; the date stays outside the seal. |

## 001 / 005 / 081

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 001 opens in silence with three questions a stranger could ask without shared history (a year they felt like themselves, a habit a new friend would misread, a belief they rarely say in a group). One person interviews for a timed turn, may ask two follow-ups, and does not answer inside that turn. Materials are two seats, a timer, and paper. The reveal is the answer itself. You leave having each named one fact familiarity had filed as already known. 005 opens with three questions never asked of this person, spread across more than one kind, then a shuffled six-card deck. The next card waits until the asker reflects one concrete detail, and a wrong detail is corrected in a sentence. Materials are blank cards, a pen, and a timer. The artifact is the stack of answers that survived that echo. 081 never lets the asker choose in the moment. Twelve slips are dealt from the bank of twenty-four, or from blank paper; five are kept, folded with an initial outward, and dropped in a bowl. A coin opens. At most four draws. Each draw ends as an answer, a pass, or an offer-back. Unread slips are torn up or returned face down. Materials are the bank or blank paper, two pens, a bowl, and a coin. Playing one procedure under another title would drop the stranger turn, the per-card echo, or the chance-and-destroy cap.

## 041 / 107

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 041 opens with one teller privately building three unlabeled stories of matched length. Two happened. The fiction is its own scene, not a stitch inside a real day. The listener makes one guess. The uncovering names the fiction in one sentence, then restates each truth as something to remember. Materials are three matched cards, a pen, a timer, and a Keep slip. 107 opens by fixing one true story and writing the single seam on a slip the teller sits on. The listener gets three yes-or-no guesses at the load-bearing detail. The reveal restores the true version, names the symbol as a wish, a fear, or an unrealized possibility, and adds one plain sentence for why the fiction appealed. Materials are optional: one slip. Guessing which whole story is fake is not hunting a seam.

## 039 / 046

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 039 opens apart. Each person chooses one condition and writes five lines: where, when, what each of you is doing, one sensory detail, and the moment of noticing. Real faces and personalities stay. There is no plot. The listener has two sentences and no critique. You close with one line each: "What would still attract me is ______," and the scene also names what that other life would have hidden. Materials are paper or a notes app. There is no extended version that starts a second era. 046 opens together on one world, a single sentence from the six-world menu or a sentence at that scale. Each person keeps the name they already use and adds a job. The blank in the procedure is "I am ____, window-letterer," not a standing fictional couple. Turns trade sentences through a meeting, a spark, and a fixable mess, and the repair has to happen inside the fiction. Two return lines each name a trait the real person already has, then the job titles come off. Materials are a timer and optional paper. A costume meeting with no disaster is 039. A caper that brings a trait home is 046.

## 006 / 102

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 006 opens by labeling four cards Object, Person, Song, and Event. Each label has three lines: what it is, which stretch of life it holds, and why it is in the collection. The visitor asks one question per gallery so the piece can be seen more clearly, and both people give a tour. A tour ends when the visitor thanks the curator in one sentence that names a piece. A real object is optional. A timer is part of the setup. 102 opens with about 15 minutes of quiet writing on a fixed pair, copied exactly: "What happened" and "What I wish you'd understood." After one question, the curator says whether the label is to be carried, was only for the saying, or is not on display. The visitor names which labels they can carry. Every other card, including a closed room, is returned or destroyed. Symmetry is optional. Materials are cards and a pen, with no timer and no object-person-song-event set. A life tour cannot be played as a pocket of unsaid things.

## Part 10, 073–080

**Judgment:** already distinct. 080 has not drifted back into 073. 073–079 were left unchanged. 080 was not rewritten again.

**Files changed:** none.

**Contrast:** Eight memoir sittings, eight tools. 073 seals two five-line drafts of the beginning (where it starts, what was unsure, a polished detail, a guess about the other's feeling, a fact still unknown), then marks same memory, news, and remembered differently. The finished object is two unfused drafts, and an optional joint paragraph that keeps one agreed fact and one uncertainty. 074 trades underestimated impact one item at a time, up to five, and stores only agreed pairs in two columns: what was done, and what it meant. 075 sorts slug lines into four columns (funniest, most romantic, unexpected, meaningful), allows an empty column to stay empty, and finishes a set list of up to three keepers plus one detail a retelling should stop sanding down. 076 sketches four beats (smaller picture, place, detail that refused to fit, wider picture), waits a minute, and reflects a change of picture. The portraits stay as "I used to think" and "I came to see." No joint verdict is required. 077 lays one shared line, marks years or chapters, and keeps a disputed date as two notes. The artifact is one editable timeline, closed by naming a stretch you still use and a stretch that deserves a kinder retelling. 078 delivers one thanks in three sentences (the act, the cost as you understand it, what changed). The cost may be wrong. A kept sentence enters the shared journal only if the receiver says yes. Otherwise it is spoken and released. 079 writes liner notes before any sound (title, source, what the piece carries). The title may stand with the sound off. You are unfinished until one story survives without the track, plus one private encore. 080 hides only the date, on a facedown card, then fills one sideways clock in view: opened, middle, turn, closed. One locating question per band. The extra object is a slip labeled "Do not restage." Two clocks if the dates differ; both lines if they match. No winner. Swapping 073 and 080 would either unveil a finished essay, which 080 no longer does, or turn the beginning into a four-band afternoon, which is not 073. A life map is not a day clock. A set list is not a refusal to restage.

## 025 / 028 / 057 / 029

**Judgment:** already distinct. 029 is a different exercise and was included in the read. Left unchanged.

**Files changed:** none.

**Contrast:** 025 opens with about 10 minutes apart and two visible or audible acts in each of Words, Gestures, and Behaviors. You read both sheets and mark every item Already happens, I did not know, or Hard for me, then circle a behavior that shows up on both. The close is one surprise each. Materials are two sheets. The artifact is the compared lists, not a type. 028 opens as a self-manual under three headings only: operating notes (two needs as situations), warning signs (two observable tells), and maintenance (two small cares, at least one you do without your partner). You read one manual at a time. The reader asks one curious question and may say which maintenance item they can support. Nobody edits the other page. An optional "please do not" line is a misfire, not a house rule. The artifact is two owner's manuals for ordinary weeks. 057 opens on the first stretch of a day that has already gone wrong. Seven headings: early signs, what misleads, what helps in the first 10 minutes, what makes that window worse, what is not about you, when to give space, when to stay nearby. The reader reads the page back and asks one clarifying question. A mild hypothetical is optional and comes after both pages exist. The artifact is a dated, revocable account of that window. 029 opens on a five-row grid, in order if you want a shared map: lonely, stressed, insecure, sad, disconnected. Three columns: what it looks like, what helps, what makes it worse. The partner reads a row back and marks I can do this, I can sometimes, or This conflicts. The longer sitting adds a signal word per filled row. A signal consults the row. It does not command, and it does not authorize touch. The artifact is the menu and the marks, with conflicts parked. A love-act comparison, an ordinary-week manual, a bad-day window, and a weather menu are four different pages. Writing "what helps" on all of them would still not let you play one under another's rules.

## 026 / 074 / 078 / 105 / 030

**Judgment:** already distinct. Left unchanged. 074 and 078 are the same chapters judged in Part 10; they were not given a second procedure.

**Files changed:** none.

**Contrast:** 026 is three live rounds that get more specific: an obvious true line, then a scene from the last month, then something easy to miss. After every line the receiver says "I heard that," or corrects a fact. Equal numbers. A fourth line is allowed only if it arrives unhunted. Materials are three blank lines and an optional timer. You may keep one line by repeating it once. 074 is weight the doer may have filed as ordinary. Up to five memories, at least three smaller than a gift or a trip, traded one at a time. The receiver may remember the event differently. The shared page has two columns and holds only pairs both people agree to keep. 078 is one unpaid thanks. Three sentences: what you did, what you think it cost (marked as your understanding, allowed to be wrong), what changed. The receiver may correct the cost. Then you ask once whether any sentence may be kept. A no means the thanks was spoken and released. 105 is a guess. Five observations the other person can see; the actual episode stays covered. The receiver names the episode they have been crediting. The writer reveals the real one. The sheet marks same or different. A mismatch is a successful turn. The choice itself is not a score of attention. 030 is the receive. One concrete compliment, about 10 seconds of quiet, then one sentence that does not joke, argue, credit luck, or hand a compliment back. After the practice, ordinary manners may return. The longer sitting names which dodge was postponed. A list of missed weights is not a belated thank-you, a decoder, or a 10-second landing.

## 010 / 052 / 087 / 097

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** Four doors, and the staircases are not the same. 010 starts from a fear you can already say. The card is Surface, Under it, Under that. The partner asks only "What might sit under that?" and does not offer a candidate. You stop at three. The last line names a need, an experience, or a belief, in the speaker's words, or "I don't know" with the kind named. The partner reads the three lines back and asks "What did I scramble?" Materials are a pencil, a timer, and the card. The artifact is the corrected ladder. 052 starts from a rule about money, manners, loyalty, work, or pleasure. The card is written before anyone speaks: Origin (a person, a punishment, a reward, or a blank), Importance now (a present scene), Revision (what would move it, and "nothing would change it" is complete). The listener repeats the importance in one sentence and asks one question, preferably what the belief protects. The close is whether it feels more rooted, more puzzling, or simply better described. You do not announce a conversion. 087 starts from lunch, or another ordinary sentence. The asker uses at most four follow-ups from a printed set of directions, reflects, and asks "Is that close?" after each. The speaker keeps the last word on meaning. Then you switch to a different afternoon. A written ladder is a full version. 097 starts from a strong feeling whose first cause is allowed to be wrong. The explorer writes the reaction and the assumed cause and leaves that sentence in view. The archaeologist asks, roughly in order, what happened just before, what the body did, what meaning arrived first, what else might be true, and what the feeling might be protecting or wanting, reflecting the explorer's nouns and asking "Is that close?" The explorer closes with keep, revise, or abandon. The archaeologist does not hand over a better cause. A fear ladder, a belief card, a lunch ladder, and a dig that may retire its own opening sentence are not one drill.

## 009 / 020 / 013 / 016

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 009 is one chosen admission. During the telling and for 3 minutes after, the listener sets aside repair. The permitted sentence is "I'm taking this in." When the minutes end, the speaker chooses: a named kind of response, or the turn ends with the truth received. Materials are two seats and a pause phrase. 020 is a listening drill with a clock on the talk. You name the topic and whether it is good news. The speaker has about 6 uninterrupted minutes. The listener then has about 2 minutes on two stems, "I heard..." and "It sounded like you felt...," and the speaker has 1 minute to correct. "What did I miss?" checks meaning. It does not argue. The artifact is a reflection the speaker recognizes. 013 is a narrow menu: embarrassment, regret, insecurity, or a harmless private truth. The speaker says "This is mine to tell, and it is harmless" before the story. The listener asks two curious questions and does not advise. Harm leaves the game. The artifact is one allowed offer, or a pass. 016 is a style ban for a set window: joke-as-cover, defense, and the résumé answer. You pick one modest topic first. When you catch your own cover, you may say "Let me try that plainly" and restate one sentence. The partner does not score hits. Their reply is one honest feeling about what they heard. The artifact is the window, not an armor score. One admission plus a pause, a timed reflection, two curious questions on a menu, and a ban on three costumes are four evenings.

## 017 / 018

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 017 opens by sitting where you can see each other and looking toward each other's eyes. Nobody has a message to send. Blinks and a brief glance away are allowed. A raised hand or "stop" ends the bout and still counts. When the timer ends, you look away on purpose. Each person names one sensation, one thought, or one impulse from their own side. You do not interpret the other face. The standard bout is 4 minutes, then one notice each. Materials are two seats and a timer you can stop. The artifact is the notice. 018 opens by saying the assignment out loud: show the day, or a memory, or an invitation in the room. Touch is out unless you agreed before the timer, and a spoken stop word ends the silence. You answer in gesture. Afterward each person says what they meant and what they thought arrived. Mismatches stay as findings. There is no score. Materials are light enough to see faces and hands, and the stop word. The artifact is the gap between the two versions. Looking with no job is not a gestured day.

## 032 / 048 / 099

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** All three cross days. The moves do not. 032 opens on day zero with a map the receiver already described: two acts that would land, one act to avoid, a money ceiling, and the length of the window. Each day, if you can, you do one act from that map. At night, four sentences: what you offered, what you noticed, what you felt, and "nothing in particular" when that is true. No totals. The close, about 20 minutes, asks what you noticed. There is no single-evening version, on purpose. The artifact is the log, including the flat days. 048 opens with three sealed missions: thoughtful, funny, affectionate. Each card carries a smaller version already authorized. Over the days the receiver marks did, shrank, or passed. A pass needs no reason. The giver does not investigate. At the reunion the receiver speaks first. The artifact is the report of being offered care, not a score. A receive-this mission counts. Declining a hug completes the affectionate one. 099 opens by hiding blank cards. Both of you know notes are being kept. You do not know the wording. During the days you write what the other person already did: helped, impressed, delighted, or attracted you, if you opted into attraction. You are not handing out tasks. At the exchange, "I don't remember that" is welcome. A card that feels like pressure can be taken back. The artifact is the traded stack, and remembering it is optional. A mapped kindness, a sealed assignment with a shrink, and a delayed observation are three tools.

## 043 / 101

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 043 opens with private phrases about what you believe is true of the other person now: habits, tastes, stresses, comforts, wishes. You reveal one question at a time. The person described speaks first and marks the guess Now, Older, or Borrowed. Optional stars stay scattered and are not added up. The debrief asks which guess described an older version or a borrowed assumption. You may update one fact in a sentence. Materials are two answer sheets and the twelve printed questions. The artifact is the marked sheet and, if you want it, one retired guess. 101 opens on a scenario, drawn from three banks (realistic, funny, morally gray), one of each in a standard night. Before anyone speaks, each person writes the choice they think the other would make and three beats: a value, a fear or a hope, and a practical constraint. The person whose mind it is then gives the actual choice and the actual reasons, and says which beat was theirs. If you score, the choice scores zero whether you matched it or missed it. A real value scores 2. A understood constraint scores 1. A wrong value is not rescued by a lucky yes. Each person writes the value they missed. Materials are the scenario banks and the slips. The artifact is the missed value, in the other person's words when those words were offered. Matching a drink is not borrowing a reason.

## 089 / 104

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 089 opens by setting borrowed assumptions where you can see them. Each person names imports (family, religion, culture, an app, an old relationship) on cards a stranger could follow. You may decline, keep, or mark "examine." Then you draft four living agreements for this month: how you greet after time apart, how you repair a small miss, how you celebrate, how you protect solitude. A refusal is written down. Round three picks one tiny ritual for two weeks and a review date. The artifact is that draft, revisable, not a constitution. 104 opens inside a fiction. Each person drafts six candidate laws a stranger could follow. You merge toward ten, record up to two dissents, and leave empty rows rather than fake a harmony. Then you shuffle twelve event cards and draw. For each card you name the principle under strain, say what it costs to keep and what it costs to change, and choose amend, defend, exception, or leave the card open. Strain scores the constitution, not the founders. At 4 or more you retire a principle or add a freedom that begins "Citizens may always…" The signature is play, and it is not house rules unless you end the game first and say so. The fictional example country misses the joke and the stores on purpose, so copying the sample does not finish the draw. Agreements you could keep this month are not a paper country under event cards.

## 055 / 093

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 055 is a personal list the partner witnesses. Draft at least eight items, at least four ordinary or cheap, and mark grand items in the margin so they do not set the standard. "Someday, and maybe never" is a category. After both lists are heard, each partner makes two marks only: one item they would like to help with, said with the cost if there is one, and one item they will not take over. The speaker then sorts ordinary and soon, grand and maybe never, and help welcome. The partner initials only the help-welcome items they mean. No initial, no obligation. You close by reading one ordinary item and one maybe-never item. Hearing a wish is not a budget. 093 is one shared page, twelve lines or fewer, added one at a time so the handwriting cannot belong to one person. Each line gets a kind: adventure, tradition, achievement, or ridiculous. At least two are unserious on purpose, and at least two are ordinary enough for a tired week. A cost band in words: free, modest, or save-for. Either person may veto. An optional star is a preference for the next season, not a vow. You close by reading the ridiculous items, then one ordinary item. A witnessed private appetite is not a joint menu.

## 008 / 011 / 083

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 008 opens with both of you drafting a short biography at the same time, contradictions included. Four ingredients: two traits that pull against each other, a motive that does not match the public story, one vulnerability without a rescue clause, and one quality friends underuse. The author decides which sentences are heard. The partner asks two clarifications and does not edit. The artifact is the portrait you chose to release, plus the questions or a pass. 011 opens on a two-column page, Hide and What would help. Two specific hidden parts, so one can stay unread, and two observable conditions beside each. The partner's only reply is a restatement of the conditions and whether they can offer each one, cannot, or are unsure. They do not negotiate the conditions down, and "you are safe with me" is not a blanket. The speaker corrects a softened condition. The artifact is one pair, heard under that reply rule, and one item that may remain unread. 083 opens with a lens, drawn or chosen, and no guessing round. The speaker says three lines: the assumption they think is in the room, a fact that is entirely true, and what that complicates. The listener asks up to three questions, then one reflection: "The assumption that moved is ___." The speaker may correct it once. A storage instruction can follow: keep the assumption, let the detail fade. The artifact is the updated assumption, not a biography and not a terms sheet. A written self-portrait, a hidden part with conditions, and one volunteered complication of a stale picture are three disclosures.

## 027 / 076 / 033

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 027 opens on one scene of when the other person started to matter more, or when closeness deepened. Place, what shifted, and what you did not say. "It accumulated" is a complete story if you name the repeats. The listener keeps their own version in their pocket and may ask one question about the teller's experience. After both have spoken, differences stay standing. You close with a title of six words or fewer. The artifact is the titled scene. 076 opens on a revision of understanding. About 5 quiet minutes, four beats: the smaller picture, the place, the detail that refused to fit, the wider picture. After the telling, a minute of quiet before the listener speaks. The listener reflects the change and does not have to agree or perform the quality. On the page, "I used to think" and "I came to see" can stand side by side. No joint verdict is required. 033 is an interview in three movements, in this order: first attraction, current attraction, and how you understand chemistry now. Both of you sit in the guest chair. The interviewer gets two follow-ups and does not grade. Sexual and bodily detail are optional. When both turns are done, each person names one sentence they want kept. The interview books nothing. A desire named as a fact stays a fact. A scene of mattering, a changed portrait, and a three-movement attraction interview do not share a turn.

## 031 / 090 / 098 / S05

**Judgment:** already distinct. Left unchanged.

**Files changed:** none.

**Contrast:** 031 opens by putting a year in the first line and looking back at now. Two qualities of the love you hope are still there, and two qualities of the partner or of yourself. Both drafts finish before either is read. You may read, hand the page over, or keep it sealed. The listener, if there is one, says thank you and asks one question about a quality, not about a plan. The longer sitting adds one ordinary practice as a postscript, which the reader may join or leave as yours. The artifact is the letter, including a sealed one. 090 opens with one happy scene that has not happened, written in the past tense: a place, a line of dialogue, a sensory detail, and a feeling. You read it as a memory. The listener offers one hearing sentence and does not annex the dream. Then a shorter bridge: one condition already true, one that would have to be built, one step available this month, and one element that is weather and cannot be forced. Label both pages fiction-as-memory. A shared step happens only where the scenes overlap by a real yes. 098 opens as an interview at about 100, or "a long life from now" if the number is unkind. One person answers in scenes. The other does not correct the fiction. Contradictory decades stay. After both interviews, the costume comes partway off and each person names up to three invented memories they would actually try. Fewer than three is complete. For each want that survives: the scene, a step without heroics, and a piece that remains fantasy unless the other person wants it. You do not average them into one century. S05 opens on pieces of this season, not an invented future. An envelope or a box, an optional picture, optional letters, a shared note. Both of you write the opening date on a slip clipped outside the seal, so a later pen can change it. The key stays in the house. Either person may ask to open early, and opening early is allowed. If one of you is away, the capsule waits unless a sentence you both wrote at sealing says otherwise. The artifact is the sealed container and the editable date. A letter from a year you have not lived, a scene told as a memory, a contradictory century, and a box of this season are four objects.

## Handoff

**Source files read:** `CURSOR_PHASE3_FIRST_EDITION_COMPLETION.md` (through the contrast assignment), `styles/CHAPTER_CONTRACT.md`, `styles/HOUSE_STYLE.md`, `review/phase3/CONTRAST_001_046.md`, `review/phase3/CONTRAST_PART10.md`, `review/developmental/MANUSCRIPT_NOTES.md`, and the practical middles of every ID in the hash table, including `signature/S05-the-capsule-we-open-later.md`. 104's example was read far enough to confirm the fictional country misses cards instead of pre-answering the deck.

**Deliverable changed:** `review/phase3/EDITORIAL_CLOSEOUT.md` only. No chapter, signature, script, asset, journal, or release file was edited. No commit.

**Acceptance:** a reader can tell each cluster's opening move, rules, and finished object apart from the pages as they stand. Canonical IDs and journal fences were not retouched, so old memoir answers still point at the same chapters.

**Not claimed:** no couple sat down and played these. The hashes are a text check. Owner play remains owner play.

**Still open:** none of the assigned clusters. Nothing was left half-revised.
