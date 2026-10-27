"""Typeset deck cards at 3.5 by 5.5 inches.

Art is placed at 2.88 by 3.84 inches. A native 864 by 1152 image is then
300 pixels per inch. That is source detail, not an upscale.

A press file adds 3 mm bleed. The trim proof is the size a card is cut to.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

PARTS = {
    1: ("Knowing", "The Art of Really Knowing Someone", "#A85A32", "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z"),
    2: ("Courage", "Vulnerability and the Courage to Be Seen", "#7C3A46", "M12 2l7 4v6c0 5-3.2 8.4-7 10-3.8-1.6-7-5-7-10V6z"),
    3: ("Closeness", "The Science and Experience of Closeness", "#3E6464", "M7 16c0-4 2.2-7 5-7s5 3 5 7"),
    4: ("Chosen", "Love, Affection, and Feeling Chosen", "#C4787A", "M12 20s-7-4.4-7-9a4 4 0 0 1 7-2 4 4 0 0 1 7 2c0 4.6-7 9-7 9z"),
    5: ("Desire", "Desire, Attraction, and Sensual Intimacy", "#5C3A4E", "M12 21c4-3 7-6.2 7-10a5 5 0 0 0-9-3 5 5 0 0 0-5 3c0 3.8 3 7 7 10z"),
    6: ("Play", "Playfulness, Laughter, and a Little Mischief", "#C4892A", "M12 3l2.2 5.2L20 10l-5.8 1.8L12 17l-2.2-5.2L4 10l5.8-1.8z"),
    7: ("Inner", "The Inner World: Dreams, Meaning, and Identity", "#3D4A7A", "M14 3a7 7 0 1 0 7 10 6 6 0 1 1-7-10z"),
    8: ("Trust", "Trust, Communication, and Emotional Safety", "#4A5560", "M8 11V8a4 4 0 0 1 8 0v3h1v9H7v-9h1zm2 0h4V8a2 2 0 0 0-4 0z"),
    9: ("Adventure", "Shared Adventures and New Experiences", "#3E6B4F", "M5 19c4-1 6-4 7-7 1 3 3 6 7 7-4-2-6-6-7-10-1 4-3 8-7 10z"),
    10: ("Story", "The Past, the Present, and the Story of Us", "#C6A15B", "M6 5h5a3 3 0 0 1 3 3v12s-1-1-3-1H6V5zm12 0h-5a3 3 0 0 0-3 3v12s1-1 3-1h5V5z"),
    11: ("Curiosity", "Radical Curiosity and the Surprising Stuff", "#B85C38", "M4 12h16M12 4c2.5 2.2 4 5 4 8s-1.5 5.8-4 8c-2.5-2.2-4-5-4-8s1.5-5.8 4-8z"),
    12: ("Future", "Building a Closer Future Together", "#7A8F6A", "M12 20V10M12 14c-3 0-5-2-5-5 3 0 5 2 5 5zm0 0c3 0 5-2 5-5-3 0-5 2-5 5z"),
    13: ("Workshop", "The Inventor's Workshop", "#1B2433", "M12 8a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM4 12h3m10 0h3M6.5 6.5l2 2m7 7l2 2m0-11l-2 2m-7 7l-2 2"),
}

PAPER = "#f4efe4"
INK = "#241c16"


def part_of(card_id: str) -> int:
    n = int(card_id[1:])
    return (n - 1) // 5 + 1


def ink_on(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#1c140f" if lum > 0.62 else "#f7f1e6"


def words(card: dict) -> int:
    bits = [card.get("hook", ""), card.get("ending", ""), card.get("pass", ""), card.get("safety", "")]
    bits.extend(card.get("steps") or [])
    bits.extend(card.get("bank") or [])
    return len(" ".join(bits).split())


def load_cards() -> list[dict]:
    cards = []
    for path in sorted((DECK / "cards").glob("part-*.json")):
        cards.extend(json.loads(path.read_text(encoding="utf-8")))
    cards.sort(key=lambda c: c["card_id"])
    return cards


def symbol(part: int, color: str) -> str:
    d = PARTS[part][3]
    return (
        f'<svg class="mark" viewBox="0 0 24 24" aria-hidden="true">'
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" '
        f'stroke-linejoin="round" stroke-linecap="round"/></svg>'
    )


def esc(text: str) -> str:
    return html.escape(text or "")


def front_html(card: dict, art: Path | None) -> str:
    part = part_of(card["card_id"])
    name, full, color, _ = PARTS[part]
    band_ink = ink_on(color)
    if art is None:
        picture = '<div class="await">Illustration not approved</div>'
    else:
        picture = f'<img src="../../art/{card["card_id"]}/final.jpg" alt="">'
    return f"""
    <article class="card front">
      <div class="frame" style="border-color:{color}">
        <div class="art">{picture}</div>
        <footer style="background:{color};color:{band_ink}">
          <p class="kicker">{symbol(part, band_ink)} {card['card_id']} · {esc(name)}</p>
          <h1>{esc(card['title'])}</h1>
          <p class="meta">{esc(full)}</p>
        </footer>
      </div>
    </article>
    """


def back_html(card: dict) -> str:
    part = part_of(card["card_id"])
    name, full, color, _ = PARTS[part]
    band_ink = ink_on(color)
    steps = "".join(f"<li>{esc(step)}</li>" for step in card.get("steps") or [])
    bank_items = card.get("bank") or []
    bank = ""
    if bank_items:
        lis = "".join(f"<li>{esc(item)}</li>" for item in bank_items)
        bank = f'<ol class="bank">{lis}</ol>'
    safety = card.get("safety") or ""
    safety_html = f'<p class="safety">{esc(safety)}</p>' if safety else ""
    touch = "Touch card. Pick it on purpose." if card.get("touch") else "No touch required."
    return f"""
    <article class="card back">
      <header style="background:{color};color:{band_ink}">
        {symbol(part, band_ink)}
        <div>
          <p class="kicker">Part {part:02d} · {esc(name)}</p>
          <p class="full">{esc(full)}</p>
        </div>
      </header>
      <div class="body">
        <h1>{esc(card['title'])}</h1>
        <p class="hook">{esc(card.get('hook',''))}</p>
        <ol>{steps}</ol>
        {bank}
        <p class="ending">{esc(card.get('ending',''))}</p>
        {safety_html}
        <p class="pass">{esc(card.get('pass',''))}</p>
      </div>
      <footer>
        <span>{esc(card.get('time',''))}</span>
        <span>{touch}</span>
        <span>Book {esc(card['source_id'])}</span>
      </footer>
    </article>
    """


STYLE = """
@page { size: 3.5in 5.5in; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #d9d3c7; }
.card {
  width: 3.5in; height: 5.5in; page-break-after: always;
  background: #f4efe4; color: #241c16; position: relative; overflow: hidden;
}
.front .frame {
  position: absolute; inset: 0.14in; border: 1.5pt solid; display: flex;
  flex-direction: column; background: #f7f3ea;
}
.art {
  width: 2.88in; height: 3.84in; margin: 0.1in auto 0; overflow: hidden;
  background: #efe6d4;
}
.art img { width: 2.88in; height: 3.84in; object-fit: cover; display: block; }
.await {
  height: 100%; display: flex; align-items: center; justify-content: center;
  font: 10pt Calibri, sans-serif;
}
.front footer { margin-top: auto; padding: 0.1in 0.12in 0.12in; }
.front h1 { font: 12.5pt/1.15 Georgia, serif; margin: 0.04in 0 0.02in; }
.front .kicker, .back .kicker {
  display: flex; align-items: center; gap: 0.06in;
  font: 8pt Calibri, sans-serif; letter-spacing: 0.04em; text-transform: uppercase;
  margin: 0;
}
.front .meta { margin: 0; font: 8pt Calibri, sans-serif; }
.mark { width: 0.16in; height: 0.16in; flex: none; }
.back header {
  height: 0.48in; display: flex; gap: 0.08in; align-items: center;
  padding: 0.06in 0.16in;
}
.back .full { margin: 0; font: 8pt Calibri, sans-serif; }
.back .body { padding: 0.1in 0.16in 0.34in; }
.back h1 { font: 12.5pt/1.1 Georgia, serif; margin: 0 0 0.04in; }
.hook { font: italic 10pt/1.25 Georgia, serif; margin: 0 0 0.05in; }
.back ol { margin: 0 0 0.05in 0.16in; padding: 0; }
.back li { font: 10pt/1.25 Calibri, sans-serif; margin: 0 0 0.04in; }
.bank { margin-top: 0.04in; }
.ending { font: 10pt/1.25 Calibri, sans-serif; margin: 0.04in 0; }
.safety, .pass { font: 9.5pt/1.25 Calibri, sans-serif; margin: 0.03in 0; }
.pass { font-style: italic; }
.back footer {
  position: absolute; left: 0.16in; right: 0.16in; bottom: 0.1in;
  display: flex; justify-content: space-between; gap: 0.06in;
  font: 8pt Calibri, sans-serif; color: #5c5148; border-top: 0.4pt solid #d9cbb8;
  padding-top: 0.04in;
}
"""

BLEED_STYLE = STYLE.replace(
    "@page { size: 3.5in 5.5in; margin: 0; }",
    "@page { size: 3.736in 5.736in; margin: 0; }",
).replace(
    "width: 3.5in; height: 5.5in;",
    "width: 3.736in; height: 5.736in; padding: 0.118in;",
)


def document(body: str, bleed: bool) -> str:
    style = BLEED_STYLE if bleed else STYLE
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>{style}</style></head><body>{body}</body></html>"
    )


def art_path(card_id: str) -> Path | None:
    folder = DECK / "art" / card_id
    for name in ("final.jpg", "source.jpg"):
        path = folder / name
        if path.exists():
            return path
    return None


def main() -> None:
    import build_all

    cards = load_cards()
    out = DECK / "design" / "proofs"
    out.mkdir(parents=True, exist_ok=True)
    report = []
    for card in cards:
        n = words(card)
        flag = "LONG" if n > 175 else "ok"
        report.append(f"{card['card_id']} {n} {flag} art={'yes' if art_path(card['card_id']) else 'no'}")
    (DECK / "qa" / "wordcounts.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    ready = [c for c in cards if art_path(c["card_id"])]
    if not ready:
        print("no illustrated cards")
        return
    fronts = "\n".join(front_html(c, art_path(c["card_id"])) for c in ready)
    backs = "\n".join(back_html(c) for c in ready)
    # Front then back, so a duplex print can be flipped on the short edge if the
    # printer is set to that. Pairing is C01 front, C01 back, C02 front, C02 back.
    paired = []
    for card in ready:
        paired.append(front_html(card, art_path(card["card_id"])))
        paired.append(back_html(card))
    trim = out / "production-trim.html"
    bleed = out / "production-bleed.html"
    trim.write_text(document("\n".join(paired), bleed=False), encoding="utf-8")
    bleed.write_text(document("\n".join(paired), bleed=True), encoding="utf-8")
    build_all.print_pdf(trim, out / "production-trim.pdf", timeout=180)
    build_all.print_pdf(bleed, out / "production-bleed.pdf", timeout=180)
    singles = DECK / "export" / "cards"
    singles.mkdir(parents=True, exist_ok=True)
    for card in ready:
        cid = card["card_id"]
        one = document(front_html(card, art_path(cid)) + back_html(card), bleed=False)
        html_path = singles / f"{cid}.html"
        html_path.write_text(one, encoding="utf-8")
        build_all.print_pdf(html_path, singles / f"{cid}.pdf", timeout=120)
    print("cards", len(cards), "illustrated", len(ready))


if __name__ == "__main__":
    main()
