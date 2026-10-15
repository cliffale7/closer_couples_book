# -*- coding: utf-8 -*-
"""Render Night Library chapter motifs and the locked companion plates.

Reads assets/ART_MAP.json and writes assets/chapters/NNN/motif.svg.
Also writes part openers, signature heroes, covers, textures, icons,
and assets/ASSET_MANIFEST.csv.

Run from the project root or from anywhere:
    python scripts/render_motifs.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART_MAP = ROOT / "assets" / "ART_MAP.json"

# Night Library palette. No other hex values belong in these drawings.
MIDNIGHT = "#1B2433"
CHARCOAL = "#2C3544"
PARCHMENT = "#F6F1E7"
IVORY = "#FBF8F2"
INK = "#241F1C"
COPPER = "#A85A32"
GOLD = "#C6A15B"
TEAL = "#3E6464"
BURGUNDY = "#7C3A46"
LINE = "#D9CFC0"
ALLOWED_HEX = {
    MIDNIGHT, CHARCOAL, PARCHMENT, IVORY, INK, COPPER, GOLD, TEAL, BURGUNDY, LINE,
}

# Motif viewBox is 440 by 280, so a 1.6-unit stroke on the 220-wide
# design-system grid becomes 3.2 here and still prints near 1.15 pt
# when the mark is placed 2.20 inches wide.
MSW = 3.2
DSW = 2.0
PSW = 2.2  # part openers and signature heroes, per the design system

LICENSE = "original, project use, 2026-10-14"

FONT = {
    "A": ["M8 100 L40 4 L72 100", "M22 62 H58"],
    "B": ["M10 4 V100", "M10 4 H44 Q74 4 74 28 Q74 52 44 52 H10", "M10 52 H48 Q78 52 78 76 Q78 100 48 100 H10"],
    "C": ["M74 24 Q66 4 40 4 Q8 4 8 50 Q8 96 40 96 Q66 96 74 78"],
    "D": ["M10 4 V100", "M10 4 H42 Q78 4 78 50 Q78 96 42 96 H10"],
    "E": ["M72 4 H10 V100 H72", "M10 52 H54"],
    "F": ["M10 100 V4 H72", "M10 52 H52"],
    "H": ["M10 4 V100", "M70 4 V100", "M10 52 H70"],
    "I": ["M40 4 V100", "M22 4 H58", "M22 100 H58"],
    "K": ["M10 4 V100", "M70 4 L10 56", "M30 42 L72 100"],
    "L": ["M10 4 V100 H72"],
    "M": ["M8 100 V8 L40 58 L72 8 V100"],
    "N": ["M10 100 V8 L70 100 V8"],
    "O": ["M40 4 Q78 4 78 50 Q78 96 40 96 Q2 96 2 50 Q2 4 40 4"],
    "P": ["M10 100 V4 H46 Q76 4 76 32 Q76 56 46 56 H10"],
    "R": ["M10 100 V4 H46 Q76 4 76 30 Q76 54 46 54 H10", "M38 54 L74 100"],
    "S": ["M66 24 Q58 4 36 4 Q8 4 8 28 Q8 50 40 54 Q74 58 74 80 Q74 96 40 96 Q14 96 8 78"],
    "T": ["M8 4 H72", "M40 4 V100"],
    "U": ["M10 4 V64 Q10 96 40 96 Q70 96 70 64 V4"],
    "V": ["M8 4 L40 100 L72 4"],
    "W": ["M4 4 L22 100 L40 42 L58 100 L76 4"],
    "X": ["M10 4 L70 100", "M70 4 L10 100"],
    "Y": ["M8 4 L40 52 L72 4", "M40 52 V100"],
    "1": ["M28 22 L40 4 V100", "M22 100 H58"],
}


def xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class Draw:
    def __init__(self):
        self.buf: list[str] = []

    def path(self, d, stroke=INK, fill="none", sw=MSW, opacity=None, dash=None):
        attrs = [
            f'd="{d}"',
            f'fill="{fill}"',
            f'stroke="{stroke}"',
            f'stroke-width="{sw:g}"',
            'stroke-linecap="round"',
            'stroke-linejoin="round"',
        ]
        if opacity is not None:
            attrs.append(f'opacity="{opacity:g}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        self.buf.append("<path " + " ".join(attrs) + "/>")

    def line(self, x1, y1, x2, y2, **kw):
        self.path(f"M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}", **kw)

    def circ(self, cx, cy, r, stroke=INK, fill="none", sw=MSW, opacity=None, dash=None):
        extra = f' opacity="{opacity:g}"' if opacity is not None else ""
        dextra = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw:g}"{extra}{dextra}/>'
        )

    def ell(self, cx, cy, rx, ry, stroke=INK, fill="none", sw=MSW, opacity=None):
        extra = f' opacity="{opacity:g}"' if opacity is not None else ""
        self.buf.append(
            f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"{extra}/>'
        )

    def rect(self, x, y, w, h, rx=0, stroke=INK, fill="none", sw=MSW, opacity=None, dash=None):
        extra = f' opacity="{opacity:g}"' if opacity is not None else ""
        dextra = f' stroke-dasharray="{dash}"' if dash else ""
        self.buf.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx:.2f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"{extra}{dextra}/>'
        )

    def poly(self, pts, **kw):
        body = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"
        self.path(body, **kw)

    def group(self, transform):
        self.buf.append(f'<g transform="{transform}">')

    def end(self):
        self.buf.append("</g>")

    def raw(self, text):
        self.buf.append(text)


def draw_word(d: Draw, text: str, x: float, y: float, h: float, stroke=INK, sw=2.4, tracking=1.0):
    """Outlined capitals. y is the baseline. No live font."""
    scale = h / 100.0
    cursor = x
    for ch in text:
        if ch == " ":
            cursor += 50 * scale
            continue
        paths = FONT[ch.upper()]
        d.group(f"translate({cursor:.2f} {y - h:.2f}) scale({scale:.5f})")
        for p in paths:
            d.path(p, stroke=stroke, sw=sw / scale, fill="none")
        d.end()
        cursor += 88 * scale * tracking
    return cursor


def star(d, x, y, r, stroke=GOLD, fill=GOLD, sw=DSW):
    pts = []
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((x + r * math.cos(ang), y + r * math.sin(ang)))
        ang2 = ang + math.pi / 5
        pts.append((x + r * 0.42 * math.cos(ang2), y + r * 0.42 * math.sin(ang2)))
    d.poly(pts, stroke=stroke, fill=fill, sw=sw)


def chair(d, x, y, s=1.0, face=1, sw=MSW, stroke=INK, accent=COPPER):
    """Side chair. (x, y) is the floor under the back leg. face=1 looks right."""
    def X(px):
        return x + face * px * s
    def Y(py):
        return y + py * s
    d.line(X(0), Y(0), X(0), Y(-92), stroke=stroke, sw=sw)
    d.line(X(46), Y(0), X(46), Y(-40), stroke=stroke, sw=sw)
    d.line(X(-6), Y(-40), X(52), Y(-40), stroke=stroke, sw=sw)
    d.path(
        f"M{X(0):.2f} {Y(-92):.2f} Q{X(18):.2f} {Y(-104):.2f} {X(30):.2f} {Y(-86):.2f}",
        stroke=stroke, sw=sw,
    )
    d.line(X(0), Y(-68), X(16), Y(-64), stroke=accent, sw=sw * 0.75)
    d.line(X(4), Y(0), X(40), Y(0), stroke=stroke, sw=sw * 0.7)


def armchair(d, x, y, s=1.0, face=1, sw=PSW):
    def X(px):
        return x + face * px * s
    def Y(py):
        return y + py * s
    d.path(
        f"M{X(0):.2f} {Y(0):.2f} L{X(0):.2f} {Y(-70):.2f} Q{X(10):.2f} {Y(-96):.2f} "
        f"{X(36):.2f} {Y(-96):.2f} L{X(48):.2f} {Y(-70):.2f} L{X(70):.2f} {Y(-58):.2f} "
        f"L{X(70):.2f} {Y(-36):.2f} L{X(48):.2f} {Y(-28):.2f} L{X(48):.2f} {Y(0):.2f}",
        stroke=INK, sw=sw, fill=PARCHMENT,
    )
    d.line(X(8), Y(0), X(8), Y(-28), stroke=INK, sw=sw)
    d.line(X(0), Y(-28), X(48), Y(-28), stroke=COPPER, sw=sw * 0.8)


def book(d, x, y, w=70, h=92, sw=MSW, closed=True, tilt=0):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({tilt:.1f})")
    d.rect(0, 0, w, h, rx=2, fill=PARCHMENT, stroke=INK, sw=sw)
    d.line(8, 0, 8, h, stroke=COPPER, sw=sw * 0.8)
    if closed:
        d.line(w - 6, 4, w - 3, h - 4, stroke=INK, sw=sw * 0.55)
        d.line(w - 10, 4, w - 7, h - 4, stroke=INK, sw=sw * 0.55)
    else:
        for i, yy in enumerate(range(16, int(h) - 8, 12)):
            d.line(18, yy, w - 14, yy, stroke=LINE if i % 2 else INK, sw=sw * 0.45)
    d.end()


def ribbon(d, x, y, sw=MSW, stroke=BURGUNDY):
    d.path(
        f"M{x:.2f} {y:.2f} C{x+30:.2f} {y-28:.2f} {x+10:.2f} {y+36:.2f} {x+48:.2f} {y+18:.2f} "
        f"C{x+70:.2f} {y+8:.2f} {x+40:.2f} {y+52:.2f} {x+78:.2f} {y+44:.2f}",
        stroke=stroke, sw=sw, fill="none",
    )


def lamp(d, x, y, s=1.0, sw=MSW, lit=True, stem=48, stroke=INK):
    """(x, y) is the bottom of the base."""
    d.ell(x, y - 4 * s, 18 * s, 6 * s, stroke=stroke, fill=PARCHMENT, sw=sw)
    d.line(x, y - 8 * s, x, y - stem * s, stroke=stroke, sw=sw)
    shade_top = y - (stem + 26) * s
    shade_bot = y - (stem - 4) * s
    d.poly(
        [
            (x - 10 * s, shade_top),
            (x + 10 * s, shade_top),
            (x + 22 * s, shade_bot),
            (x - 22 * s, shade_bot),
        ],
        stroke=stroke, fill=IVORY, sw=sw,
    )
    if lit:
        d.ell(x, shade_bot - 6 * s, 4 * s, 7 * s, stroke=GOLD, fill=GOLD, sw=sw * 0.4)
        d.line(x - 16 * s, shade_bot, x - 28 * s, shade_bot + 18 * s, stroke=COPPER, sw=sw * 0.55)
        d.line(x + 16 * s, shade_bot, x + 28 * s, shade_bot + 18 * s, stroke=COPPER, sw=sw * 0.55)


def wall_lamp(d, x, y, s=1.0, sw=PSW, lit=True):
    d.line(x, y, x + 26 * s, y, stroke=INK, sw=sw)
    d.poly(
        [
            (x + 14 * s, y - 8 * s),
            (x + 38 * s, y - 8 * s),
            (x + 32 * s, y + 16 * s),
            (x + 8 * s, y + 16 * s),
        ],
        stroke=INK, fill=IVORY, sw=sw,
    )
    if lit:
        d.ell(x + 24 * s, y + 6 * s, 4 * s, 6 * s, stroke=GOLD, fill=GOLD, sw=sw * 0.4)
        d.path(
            f"M{x+4*s:.1f} {y+18*s:.1f} Q{x+24*s:.1f} {y+48*s:.1f} {x+46*s:.1f} {y+20*s:.1f}",
            stroke=COPPER, sw=sw * 0.7,
        )


def key(d, x, y, s=1.0, rot=0, sw=MSW, stroke=COPPER):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({rot:.1f}) scale({s:.3f})")
    local = sw / s
    d.circ(0, 0, 12, stroke=stroke, sw=local, fill="none")
    d.circ(0, 0, 5, stroke=stroke, sw=local, fill="none")
    d.line(11, 0, 46, 0, stroke=stroke, sw=local)
    d.line(32, 0, 32, 9, stroke=stroke, sw=local)
    d.line(39, 0, 39, 7, stroke=stroke, sw=local)
    d.end()


def spoon(d, x, y, s=1.0, rot=0, sw=MSW):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({rot:.1f}) scale({s:.3f})")
    local = sw / s
    d.ell(0, -18, 12, 16, stroke=INK, fill=IVORY, sw=local)
    d.path(f"M0 -2 C8 18 6 40 0 58", stroke=INK, sw=local)
    d.end()


def ticket(d, x, y, w=54, h=28, rot=0, sw=MSW, fill=IVORY, stroke=INK, accent=COPPER):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({rot:.1f})")
    d.poly(
        [(6, 0), (w - 6, 0), (w, 6), (w, h - 6), (w - 6, h), (6, h), (0, h - 6), (0, 6)],
        stroke=stroke, fill=fill, sw=sw,
    )
    d.line(w * 0.72, 3, w * 0.72, h - 3, stroke=accent, sw=sw * 0.7, dash="3 3")
    d.end()


def stone(d, x, y, s=1.0, sw=MSW, fill=LINE, stroke=INK):
    d.path(
        f"M{x-16*s:.1f} {y:.1f} Q{x-18*s:.1f} {y-14*s:.1f} {x-4*s:.1f} {y-18*s:.1f} "
        f"Q{x+14*s:.1f} {y-20*s:.1f} {x+18*s:.1f} {y-6*s:.1f} Q{x+16*s:.1f} {y+6*s:.1f} "
        f"{x:.1f} {y+4*s:.1f} Q{x-14*s:.1f} {y+6*s:.1f} {x-16*s:.1f} {y:.1f} Z",
        stroke=stroke, fill=fill, sw=sw,
    )


def paper_boat(d, x, y, s=1.0, sw=MSW, note=False):
    d.poly(
        [
            (x, y),
            (x + 78 * s, y),
            (x + 64 * s, y + 24 * s),
            (x + 14 * s, y + 24 * s),
        ],
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.poly(
        [
            (x + 18 * s, y),
            (x + 39 * s, y - 30 * s),
            (x + 60 * s, y),
        ],
        stroke=INK, fill=PARCHMENT, sw=sw,
    )
    d.line(x + 39 * s, y - 30 * s, x + 39 * s, y + 8 * s, stroke=COPPER, sw=sw * 0.7)
    if note:
        d.rect(x + 22 * s, y + 6 * s, 34 * s, 12 * s, stroke=COPPER, sw=sw * 0.6, fill="none")
        d.circ(x + 39 * s, y + 12 * s, 3.5 * s, stroke=COPPER, sw=sw * 0.55)


def coat(d, x, y, s=1.0, sw=MSW, fill=PARCHMENT, stroke=INK, sleeve_l=1.0, sleeve_r=1.0, hem=78):
    """Coat hanging from (x, y) at the collar."""
    sl = sleeve_l
    sr = sleeve_r
    d.path(
        f"M{x:.1f} {y:.1f} L{x-34*s:.1f} {y+18*s:.1f} L{x-46*s*sl:.1f} {y+(52*sl)*s:.1f} "
        f"L{x-28*s:.1f} {y+(56*sl)*s:.1f} L{x-18*s:.1f} {y+28*s:.1f} "
        f"L{x-16*s:.1f} {y+hem*s:.1f} L{x+16*s:.1f} {y+hem*s:.1f} "
        f"L{x+18*s:.1f} {y+28*s:.1f} L{x+28*s:.1f} {y+(56*sr)*s:.1f} "
        f"L{x+46*s*sr:.1f} {y+(52*sr)*s:.1f} L{x+34*s:.1f} {y+18*s:.1f} Z",
        stroke=stroke, fill=fill, sw=sw,
    )
    d.path(
        f"M{x-8*s:.1f} {y+2*s:.1f} Q{x:.1f} {y+16*s:.1f} {x+8*s:.1f} {y+2*s:.1f}",
        stroke=stroke, sw=sw * 0.7,
    )


def hook(d, x, y, s=1.0, sw=MSW):
    d.line(x - 16 * s, y, x + 18 * s, y, stroke=INK, sw=sw)
    d.line(x, y, x, y + 16 * s, stroke=COPPER, sw=sw)
    d.path(
        f"M{x:.1f} {y+16*s:.1f} Q{x+18*s:.1f} {y+18*s:.1f} {x+16*s:.1f} {y+4*s:.1f}",
        stroke=COPPER, sw=sw,
    )


def door(d, x, y, w=78, h=150, sw=MSW, knob="right", ajar=0):
    """ajar > 0 swings the door toward the viewer as a narrower leaf."""
    d.rect(x - 6, y - 6, w + 12, h + 8, stroke=INK, sw=sw, fill="none")
    if ajar <= 0:
        d.rect(x, y, w, h, stroke=INK, fill=PARCHMENT, sw=sw)
        d.rect(x + 8, y + 10, w - 16, h * 0.38, stroke=INK, sw=sw * 0.7)
        d.rect(x + 8, y + h * 0.48, w - 16, h * 0.38, stroke=INK, sw=sw * 0.7)
        kx = x + w - 16 if knob == "right" else x + 16
        d.circ(kx, y + h * 0.55, 4, stroke=COPPER, fill=COPPER, sw=sw * 0.4)
    else:
        leaf_w = max(18, w * (1 - ajar))
        d.poly(
            [(x, y), (x + leaf_w, y + 8), (x + leaf_w, y + h - 6), (x, y + h)],
            stroke=INK, fill=PARCHMENT, sw=sw,
        )
        d.line(x + 6, y + 4, x + 6, y + h - 2, stroke=COPPER, sw=sw * 0.6)
        d.circ(x + leaf_w - 8, y + h * 0.55, 3.5, stroke=COPPER, fill=COPPER, sw=sw * 0.4)


def cup(d, x, y, s=1.0, sw=MSW, crack=False, worn=False):
    d.path(
        f"M{x-22*s:.1f} {y:.1f} Q{x-24*s:.1f} {y+36*s:.1f} {x:.1f} {y+40*s:.1f} "
        f"Q{x+24*s:.1f} {y+36*s:.1f} {x+22*s:.1f} {y:.1f}",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.ell(x, y, 22 * s, 7 * s, stroke=INK, fill=PARCHMENT, sw=sw)
    d.path(
        f"M{x+22*s:.1f} {y+8*s:.1f} Q{x+40*s:.1f} {y+14*s:.1f} {x+22*s:.1f} {y+28*s:.1f}",
        stroke=INK, sw=sw,
    )
    if crack:
        d.path(
            f"M{x-8*s:.1f} {y+4*s:.1f} L{x-2*s:.1f} {y+16*s:.1f} L{x+6*s:.1f} {y+14*s:.1f} L{x+2*s:.1f} {y+34*s:.1f}",
            stroke=COPPER, sw=sw * 0.85,
        )
    if worn:
        d.path(
            f"M{x-16*s:.1f} {y+2*s:.1f} Q{x-6*s:.1f} {y-2*s:.1f} {x+4*s:.1f} {y+1*s:.1f}",
            stroke=COPPER, sw=sw * 0.7,
        )


def envelope(d, x, y, w=120, h=78, sw=MSW, flap="closed", seal=True):
    d.rect(x, y, w, h, stroke=INK, fill=IVORY, sw=sw)
    d.line(x, y + h, x + w / 2, y + h * 0.45, stroke=INK, sw=sw * 0.7)
    d.line(x + w, y + h, x + w / 2, y + h * 0.45, stroke=INK, sw=sw * 0.7)
    if flap == "closed":
        d.poly(
            [(x, y), (x + w / 2, y + h * 0.48), (x + w, y)],
            stroke=INK, fill=PARCHMENT, sw=sw,
        )
    else:
        d.poly(
            [(x, y), (x + w / 2, y - h * 0.42), (x + w, y)],
            stroke=INK, fill=PARCHMENT, sw=sw,
        )
    if seal and flap == "closed":
        d.circ(x + w / 2, y + h * 0.34, 8, stroke=COPPER, fill=COPPER, sw=sw * 0.4)
    elif seal and flap != "closed":
        d.circ(x + w * 0.72, y + h * 0.62, 8, stroke=COPPER, fill="none", sw=sw * 0.7)


def page(d, x, y, w=120, h=150, sw=MSW, lines=6, blank=False, tilt=0):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({tilt:.1f})")
    d.rect(0, 0, w, h, stroke=INK, fill=IVORY, sw=sw)
    if not blank:
        for i in range(lines):
            yy = 22 + i * ((h - 36) / max(1, lines))
            end = w - 16 - (8 if i % 3 == 2 else 0)
            d.line(14, yy, end, yy, stroke=LINE, sw=sw * 0.55)
    d.end()


def card(d, x, y, w=78, h=108, sw=MSW, tilt=0, fill=IVORY, face="lines"):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({tilt:.1f})")
    d.rect(0, 0, w, h, rx=3, stroke=INK, fill=fill, sw=sw)
    if face == "lines":
        for i in range(4):
            d.line(10, 24 + i * 16, w - 12, 24 + i * 16, stroke=LINE, sw=sw * 0.5)
    elif face == "back":
        d.line(8, 8, w - 8, h - 8, stroke=COPPER, sw=sw * 0.55)
        d.rect(6, 6, w - 12, h - 12, stroke=COPPER, sw=sw * 0.5)
    elif face == "blank":
        pass
    elif face == "memory":
        lamp(d, w * 0.5, h * 0.72, s=0.42, sw=sw * 0.85, stem=36)
    d.end()


def hand_palm(d, x, y, s=1.0, sw=MSW, flip=1):
    pts = [
        (-18, 10), (-30, -8), (-48, -16), (-54, -36), (-40, -44), (-28, -26),
        (-32, -48), (-36, -88), (-22, -94), (-14, -58),
        (-12, -66), (-8, -104), (2, -108), (10, -64),
        (12, -62), (16, -98), (26, -100), (28, -58),
        (30, -54), (38, -82), (46, -76), (38, -36),
        (30, -6), (16, 12),
    ]
    d.poly([(x + flip * px * s, y + py * s) for px, py in pts], stroke=INK, fill=PARCHMENT, sw=sw)
    d.path(
        f"M{x+flip*-6*s:.1f} {y-18*s:.1f} Q{x+flip*8*s:.1f} {y-28*s:.1f} {x+flip*20*s:.1f} {y-16*s:.1f}",
        stroke=COPPER, sw=sw * 0.55,
    )


def hand_side(d, x, y, s=1.0, sw=MSW, face=1):
    """Side hand, wrist to the left when face=1, fingers to the right."""
    def X(px):
        return x + face * px * s
    def Y(py):
        return y + py * s
    d.path(
        f"M{X(0):.1f} {Y(8):.1f} L{X(0):.1f} {Y(-16):.1f} L{X(28):.1f} {Y(-28):.1f} "
        f"L{X(46):.1f} {Y(-18):.1f} L{X(34):.1f} {Y(-6):.1f} L{X(48):.1f} {Y(2):.1f} "
        f"L{X(30):.1f} {Y(10):.1f} L{X(18):.1f} {Y(6):.1f} L{X(8):.1f} {Y(16):.1f} Z",
        stroke=INK, fill=PARCHMENT, sw=sw,
    )


def profile(d, x, y, s=1.0, face=1, sw=MSW, changed=False):
    """Adult profile. (x, y) is the chin. face=1 looks right."""
    def X(px):
        return x + face * px * s
    def Y(py):
        return y + py * s
    d.path(
        f"M{X(-8):.1f} {Y(18):.1f} L{X(-18):.1f} {Y(8):.1f} "
        f"C{X(-36):.1f} {Y(-8):.1f} {X(-34):.1f} {Y(-58):.1f} {X(-8):.1f} {Y(-70):.1f} "
        f"C{X(6):.1f} {Y(-78):.1f} {X(8):.1f} {Y(-60):.1f} {X(14):.1f} {Y(-48):.1f} "
        f"L{X(28):.1f} {Y(-46):.1f} L{X(14):.1f} {Y(-40):.1f} "
        f"Q{X(18):.1f} {Y(-30):.1f} {X(10):.1f} {Y(-24):.1f} "
        f"Q{X(16):.1f} {Y(-16):.1f} {X(8):.1f} {Y(-12):.1f} "
        f"Q{X(2):.1f} {Y(-4):.1f} {X(0):.1f} {Y(0):.1f} "
        f"Q{X(-8):.1f} {Y(6):.1f} {X(-6):.1f} {Y(16):.1f}",
        stroke=INK, fill="none", sw=sw,
    )
    d.line(X(-16), Y(-62), X(-2), Y(-60), stroke=INK, sw=sw * 0.7)
    mouth_y = -16 if not changed else -18
    d.path(
        f"M{X(6):.1f} {Y(mouth_y):.1f} Q{X(12):.1f} {Y(mouth_y + (2 if changed else -1)):.1f} {X(8):.1f} {Y(mouth_y + 4):.1f}",
        stroke=INK, sw=sw * 0.7,
    )
    if changed:
        d.circ(X(4), Y(-34), 3.2 * s, stroke=COPPER, sw=sw * 0.6)


def minute_mark(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x - 10*s:.1f} {y + 8*s:.1f} A{14*s:.1f} {14*s:.1f} 0 0 1 {x + 12*s:.1f} {y - 6*s:.1f}",
        stroke=COPPER, sw=sw,
    )
    d.line(x, y - 16 * s, x, y - 4 * s, stroke=INK, sw=sw)


def bench(d, x, y, w=180, sw=MSW):
    d.line(x, y, x + w, y, stroke=INK, sw=sw)
    d.line(x + 16, y, x + 10, y + 28, stroke=INK, sw=sw)
    d.line(x + w - 16, y, x + w - 10, y + 28, stroke=INK, sw=sw)
    d.line(x + 18, y - 22, x + 18, y, stroke=INK, sw=sw)
    d.line(x + w - 18, y - 22, x + w - 18, y, stroke=INK, sw=sw)
    d.line(x + 18, y - 22, x + w - 18, y - 22, stroke=COPPER, sw=sw * 0.75)


def table(d, x, y, w=200, h=18, sw=MSW):
    d.rect(x, y, w, h, stroke=INK, fill=PARCHMENT, sw=sw)
    d.line(x + 16, y + h, x + 10, y + h + 48, stroke=INK, sw=sw)
    d.line(x + w - 16, y + h, x + w - 10, y + h + 48, stroke=INK, sw=sw)


def table_top(d, x, y, w=280, depth=70, sw=MSW):
    d.poly(
        [(x, y), (x + w, y), (x + w - depth * 0.35, y + depth), (x + depth * 0.35, y + depth)],
        stroke=INK, fill=PARCHMENT, sw=sw,
    )


def phone(d, x, y, s=1.0, sw=MSW):
    d.rect(x, y, 46 * s, 78 * s, rx=6, stroke=INK, fill=CHARCOAL, sw=sw)
    d.circ(x + 23 * s, y + 14 * s, 4 * s, stroke=COPPER, fill=COPPER, sw=sw * 0.3)
    d.rect(x + 16 * s, y + 64 * s, 14 * s, 4 * s, rx=2, stroke=LINE, sw=sw * 0.5)


def clock(d, x, y, r=58, sw=MSW, hour=4, minute=0):
    d.circ(x, y, r, stroke=INK, fill=IVORY, sw=sw)
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        inner = r - (10 if i % 3 == 0 else 6)
        d.line(
            x + inner * math.cos(ang), y + inner * math.sin(ang),
            x + (r - 3) * math.cos(ang), y + (r - 3) * math.sin(ang),
            stroke=COPPER if i == hour else INK, sw=sw * (0.9 if i == hour else 0.55),
        )
    ha = -math.pi / 2 + (hour % 12 + minute / 60) * math.pi / 6
    ma = -math.pi / 2 + minute * math.pi / 30
    d.line(x, y, x + r * 0.48 * math.cos(ha), y + r * 0.48 * math.sin(ha), stroke=INK, sw=sw)
    d.line(x, y, x + r * 0.72 * math.cos(ma), y + r * 0.72 * math.sin(ma), stroke=COPPER, sw=sw * 0.75)
    d.circ(x, y, 3.2, stroke=INK, fill=INK, sw=sw * 0.3)


def kettle(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x-28*s:.1f} {y:.1f} Q{x-32*s:.1f} {y-40*s:.1f} {x:.1f} {y-48*s:.1f} "
        f"Q{x+32*s:.1f} {y-40*s:.1f} {x+28*s:.1f} {y:.1f} Z",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.ell(x, y - 48 * s, 16 * s, 6 * s, stroke=INK, fill=PARCHMENT, sw=sw)
    d.path(
        f"M{x+26*s:.1f} {y-30*s:.1f} Q{x+48*s:.1f} {y-36*s:.1f} {x+46*s:.1f} {y-16*s:.1f}",
        stroke=COPPER, sw=sw,
    )
    d.path(
        f"M{x-16*s:.1f} {y-48*s:.1f} Q{x-20*s:.1f} {y-70*s:.1f} {x:.1f} {y-66*s:.1f} "
        f"Q{x+18*s:.1f} {y-70*s:.1f} {x+14*s:.1f} {y-48*s:.1f}",
        stroke=INK, sw=sw,
    )


def frame_rect(d, x, y, w, h, sw=MSW, inner=True):
    d.rect(x, y, w, h, stroke=INK, sw=sw, fill=IVORY)
    if inner:
        d.rect(x + 8, y + 8, w - 16, h - 16, stroke=COPPER, sw=sw * 0.65)


def plinth(d, x, y, s=1.0, sw=MSW):
    d.poly(
        [
            (x, y),
            (x + 54 * s, y),
            (x + 46 * s, y - 14 * s),
            (x + 8 * s, y - 14 * s),
        ],
        stroke=INK, fill=PARCHMENT, sw=sw,
    )
    d.rect(x + 12 * s, y - 48 * s, 30 * s, 34 * s, stroke=INK, fill=IVORY, sw=sw)
    d.line(x + 8 * s, y - 14 * s, x + 46 * s, y - 14 * s, stroke=COPPER, sw=sw * 0.7)


def mask_half(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x:.1f} {y:.1f} Q{x+36*s:.1f} {y-8*s:.1f} {x+40*s:.1f} {y+28*s:.1f} "
        f"Q{x+28*s:.1f} {y+48*s:.1f} {x:.1f} {y+36*s:.1f} Z",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.ell(x + 16 * s, y + 16 * s, 7 * s, 5 * s, stroke=COPPER, sw=sw * 0.7)
    d.line(x + 4 * s, y, x - 8 * s, y + 8 * s, stroke=INK, sw=sw * 0.7)
    d.line(x + 34 * s, y + 6 * s, x + 48 * s, y + 2 * s, stroke=INK, sw=sw * 0.7)


def wax_seal(d, x, y, r=16, sw=MSW, unused=False):
    d.circ(x, y, r, stroke=COPPER, fill=COPPER if not unused else "none", sw=sw)
    if not unused:
        d.circ(x, y, r * 0.45, stroke=PARCHMENT, sw=sw * 0.6)
    else:
        d.circ(x, y, r * 0.45, stroke=COPPER, sw=sw * 0.55)


def speech(d, x, y, w=120, h=70, sw=MSW, tail="left", shape="round"):
    if shape == "round":
        d.rect(x, y, w, h, rx=18, stroke=INK, fill=IVORY, sw=sw)
    else:
        d.rect(x, y, w, h, rx=2, stroke=INK, fill=PARCHMENT, sw=sw)
    if tail == "left":
        d.poly([(x + 22, y + h - 2), (x + 10, y + h + 22), (x + 48, y + h - 2)], stroke=INK, fill=IVORY, sw=sw)
    elif tail == "right":
        d.poly([(x + w - 48, y + h - 2), (x + w - 10, y + h + 22), (x + w - 22, y + h - 2)], stroke=INK, fill=PARCHMENT, sw=sw)
    for i in range(3):
        d.line(x + 16, y + 20 + i * 14, x + w - 18, y + 20 + i * 14, stroke=LINE, sw=sw * 0.55)


def armor(d, x, y, s=1.0, sw=MSW):
    """Helmet and breastplate on a stand. (x, y) floor."""
    d.line(x, y, x, y - 120 * s, stroke=COPPER, sw=sw)
    d.line(x - 28 * s, y, x + 28 * s, y, stroke=INK, sw=sw)
    d.line(x - 18 * s, y - 8 * s, x + 18 * s, y - 8 * s, stroke=INK, sw=sw)
    d.path(
        f"M{x-26*s:.1f} {y-70*s:.1f} Q{x:.1f} {y-96*s:.1f} {x+26*s:.1f} {y-70*s:.1f} "
        f"L{x+22*s:.1f} {y-28*s:.1f} L{x-22*s:.1f} {y-28*s:.1f} Z",
        stroke=INK, fill=PARCHMENT, sw=sw,
    )
    d.path(
        f"M{x-16*s:.1f} {y-108*s:.1f} Q{x:.1f} {y-128*s:.1f} {x+16*s:.1f} {y-108*s:.1f} "
        f"L{x+14*s:.1f} {y-86*s:.1f} L{x-14*s:.1f} {y-86*s:.1f} Z",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.line(x - 10 * s, y - 78 * s, x + 10 * s, y - 78 * s, stroke=COPPER, sw=sw * 0.6)


def blindfold(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x:.1f} {y:.1f} Q{x+40*s:.1f} {y-12*s:.1f} {x+80*s:.1f} {y:.1f} "
        f"Q{x+40*s:.1f} {y+16*s:.1f} {x:.1f} {y:.1f} Z",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.line(x, y, x - 28 * s, y + 10 * s, stroke=COPPER, sw=sw * 0.8)
    d.line(x + 80 * s, y, x + 112 * s, y + 8 * s, stroke=COPPER, sw=sw * 0.8)
    d.line(x - 28 * s, y + 10 * s, x - 20 * s, y + 26 * s, stroke=COPPER, sw=sw * 0.65)
    d.line(x + 112 * s, y + 8 * s, x + 100 * s, y + 24 * s, stroke=COPPER, sw=sw * 0.65)


def hallway(d, x, y, w=160, h=120, sw=MSW):
    d.rect(x, y, w, h, stroke=INK, sw=sw, fill=IVORY)
    inset = 28
    d.rect(x + inset, y + 16, w - 2 * inset, h - 40, stroke=COPPER, sw=sw * 0.7)
    d.line(x, y, x + inset, y + 16, stroke=INK, sw=sw * 0.7)
    d.line(x + w, y, x + w - inset, y + 16, stroke=INK, sw=sw * 0.7)
    d.line(x, y + h, x + inset, y + h - 24, stroke=INK, sw=sw * 0.7)
    d.line(x + w, y + h, x + w - inset, y + h - 24, stroke=INK, sw=sw * 0.7)


def spark(d, x, y, s=1.0, sw=MSW, stroke=BURGUNDY):
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        d.line(
            x, y,
            x + math.cos(rad) * 14 * s, y + math.sin(rad) * 14 * s,
            stroke=stroke, sw=sw * 0.7,
        )
    d.circ(x, y, 3 * s, stroke=stroke, fill=stroke, sw=sw * 0.3)


def weather(d, kind, x, y, s=1.0, sw=MSW):
    if kind == "sun":
        d.circ(x, y, 10 * s, stroke=GOLD, fill=GOLD, sw=sw * 0.4)
        for i in range(8):
            ang = i * math.pi / 4
            d.line(
                x + math.cos(ang) * 14 * s, y + math.sin(ang) * 14 * s,
                x + math.cos(ang) * 22 * s, y + math.sin(ang) * 22 * s,
                stroke=GOLD, sw=sw * 0.6,
            )
    elif kind == "cloud":
        d.circ(x, y, 10 * s, stroke=INK, fill=IVORY, sw=sw)
        d.circ(x + 12 * s, y + 2 * s, 8 * s, stroke=INK, fill=IVORY, sw=sw)
        d.circ(x - 12 * s, y + 3 * s, 7 * s, stroke=INK, fill=IVORY, sw=sw)
    elif kind == "rain":
        weather(d, "cloud", x, y, s, sw)
        for dx in (-8, 0, 8):
            d.line(x + dx * s, y + 14 * s, x + (dx - 3) * s, y + 26 * s, stroke=TEAL, sw=sw * 0.7)
    elif kind == "wind":
        d.path(
            f"M{x-16*s:.1f} {y:.1f} H{x+18*s:.1f} Q{x+28*s:.1f} {y:.1f} {x+24*s:.1f} {y-8*s:.1f}",
            stroke=TEAL, sw=sw,
        )
        d.path(
            f"M{x-20*s:.1f} {y+10*s:.1f} H{x+8*s:.1f}",
            stroke=TEAL, sw=sw * 0.8,
        )


def pen(d, x, y, s=1.0, rot=-35, sw=MSW, color=INK):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({rot:.1f}) scale({s:.3f})")
    local = sw / s
    d.line(0, 0, 70, 0, stroke=color, sw=local)
    d.poly([(70, -4), (86, 0), (70, 4)], stroke=COPPER, fill=COPPER, sw=local * 0.5)
    d.line(16, -5, 16, 5, stroke=COPPER, sw=local * 0.6)
    d.end()


def pencil(d, x, y, s=1.0, rot=-20, sw=MSW):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({rot:.1f}) scale({s:.3f})")
    local = sw / max(0.2, s)
    d.rect(0, -4, 62, 8, stroke=INK, fill=IVORY, sw=local)
    d.poly([(62, -4), (78, 0), (62, 4)], stroke=COPPER, fill=COPPER, sw=local * 0.5)
    d.line(10, -4, 10, 4, stroke=COPPER, sw=local * 0.55)
    d.end()


def glass(d, x, y, s=1.0, sw=MSW, fill="none", rim=None):
    d.path(
        f"M{x-14*s:.1f} {y-40*s:.1f} L{x-10*s:.1f} {y:.1f} Q{x:.1f} {y+8*s:.1f} {x+10*s:.1f} {y:.1f} "
        f"L{x+14*s:.1f} {y-40*s:.1f}",
        stroke=INK, fill=fill, sw=sw,
    )
    d.ell(x, y - 40 * s, 14 * s, 5 * s, stroke=rim or INK, fill="none", sw=sw)


def record(d, x, y, r=28, sw=MSW):
    d.circ(x, y, r, stroke=INK, fill=CHARCOAL, sw=sw)
    d.circ(x, y, r * 0.55, stroke=LINE, sw=sw * 0.45)
    d.circ(x, y, r * 0.22, stroke=COPPER, fill=PARCHMENT, sw=sw * 0.6)
    d.circ(x, y, 2.4, stroke=INK, fill=INK, sw=sw * 0.3)


def citrus(d, x, y, s=1.0, sw=MSW):
    d.circ(x, y, 16 * s, stroke=INK, fill=IVORY, sw=sw)
    d.line(x - 12 * s, y, x + 12 * s, y, stroke=COPPER, sw=sw * 0.55)
    d.line(x, y - 12 * s, x, y + 12 * s, stroke=COPPER, sw=sw * 0.55)
    d.path(
        f"M{x+10*s:.1f} {y-8*s:.1f} Q{x+28*s:.1f} {y-24*s:.1f} {x+18*s:.1f} {y-2*s:.1f}",
        stroke=BURGUNDY, sw=sw,
    )


def cloth(d, x, y, s=1.0, sw=MSW, fill=BURGUNDY):
    d.path(
        f"M{x:.1f} {y:.1f} Q{x+30*s:.1f} {y-20*s:.1f} {x+70*s:.1f} {y:.1f} "
        f"Q{x+50*s:.1f} {y+16*s:.1f} {x+36*s:.1f} {y+28*s:.1f} "
        f"Q{x+16*s:.1f} {y+14*s:.1f} {x:.1f} {y:.1f} Z",
        stroke=INK, fill=fill, sw=sw,
    )


def locket(d, x, y, s=1.0, sw=MSW, open_=False):
    d.path(
        f"M{x:.1f} {y-16*s:.1f} Q{x+16*s:.1f} {y-22*s:.1f} {x+16*s:.1f} {y:.1f} "
        f"Q{x+16*s:.1f} {y+20*s:.1f} {x:.1f} {y+26*s:.1f} "
        f"Q{x-16*s:.1f} {y+20*s:.1f} {x-16*s:.1f} {y:.1f} "
        f"Q{x-16*s:.1f} {y-22*s:.1f} {x:.1f} {y-16*s:.1f} Z",
        stroke=INK, fill=IVORY, sw=sw,
    )
    if not open_:
        d.line(x, y - 16 * s, x, y + 26 * s, stroke=COPPER, sw=sw * 0.65)
    d.circ(x, y - 22 * s, 3 * s, stroke=COPPER, sw=sw * 0.6)


def feet_pair(d, x, y, s=1.0, sw=MSW, face=1):
    for dx in (-16, 14):
        cx = x + face * dx * s
        d.ell(cx, y, 12 * s, 22 * s, stroke=INK, fill=PARCHMENT, sw=sw)
        for i, tdx in enumerate((-7, -2, 3, 8)):
            d.circ(cx + face * tdx * s, y - 20 * s, 3.4 * s, stroke=INK, fill=PARCHMENT, sw=sw * 0.65)


def music_stand(d, x, y, s=1.0, sw=MSW):
    d.poly(
        [
            (x - 28 * s, y - 70 * s),
            (x + 28 * s, y - 78 * s),
            (x + 24 * s, y - 48 * s),
            (x - 24 * s, y - 46 * s),
        ],
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.line(x, y, x, y - 58 * s, stroke=INK, sw=sw)
    d.line(x, y, x - 26 * s, y, stroke=INK, sw=sw)
    d.line(x, y, x + 22 * s, y + 4 * s, stroke=INK, sw=sw)
    d.line(x - 8 * s, y - 6 * s, x + 16 * s, y - 2 * s, stroke=COPPER, sw=sw * 0.7)


def hat(d, x, y, kind="brim", s=1.0, sw=MSW, band=GOLD):
    if kind == "brim":
        d.ell(x, y, 28 * s, 8 * s, stroke=INK, fill=PARCHMENT, sw=sw)
        d.path(
            f"M{x-16*s:.1f} {y:.1f} Q{x-18*s:.1f} {y-28*s:.1f} {x:.1f} {y-36*s:.1f} "
            f"Q{x+18*s:.1f} {y-28*s:.1f} {x+16*s:.1f} {y:.1f}",
            stroke=INK, fill=IVORY, sw=sw,
        )
        d.path(
            f"M{x-14*s:.1f} {y-8*s:.1f} Q{x:.1f} {y-4*s:.1f} {x+14*s:.1f} {y-8*s:.1f}",
            stroke=band, sw=sw * 0.75,
        )
    elif kind == "cap":
        d.path(
            f"M{x-20*s:.1f} {y:.1f} Q{x-16*s:.1f} {y-30*s:.1f} {x+8*s:.1f} {y-32*s:.1f} "
            f"L{x+14*s:.1f} {y:.1f} Z",
            stroke=INK, fill=IVORY, sw=sw,
        )
        d.line(x + 8 * s, y - 6 * s, x + 32 * s, y - 2 * s, stroke=INK, sw=sw)
        d.line(x - 10 * s, y - 8 * s, x + 10 * s, y - 6 * s, stroke=band, sw=sw * 0.7)
    elif kind == "crown":
        d.poly(
            [
                (x - 24 * s, y),
                (x - 18 * s, y - 22 * s),
                (x - 8 * s, y - 8 * s),
                (x, y - 28 * s),
                (x + 8 * s, y - 8 * s),
                (x + 18 * s, y - 22 * s),
                (x + 24 * s, y),
            ],
            stroke=GOLD, fill=IVORY, sw=sw,
        )
    elif kind == "silly":
        d.ell(x, y, 26 * s, 7 * s, stroke=INK, fill=PARCHMENT, sw=sw)
        d.path(
            f"M{x-12*s:.1f} {y:.1f} Q{x:.1f} {y-40*s:.1f} {x+14*s:.1f} {y-6*s:.1f}",
            stroke=INK, fill=IVORY, sw=sw,
        )
        d.circ(x + 2 * s, y - 36 * s, 6 * s, stroke=GOLD, fill=GOLD, sw=sw * 0.4)


def paddle(d, x, y, s=1.0, sw=MSW):
    d.rect(x, y, 36 * s, 48 * s, rx=4, stroke=INK, fill=IVORY, sw=sw)
    d.line(x + 18 * s, y + 48 * s, x + 18 * s, y + 84 * s, stroke=COPPER, sw=sw)


def cake(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x-30*s:.1f} {y:.1f} L{x-24*s:.1f} {y-28*s:.1f} L{x+24*s:.1f} {y-28*s:.1f} L{x+30*s:.1f} {y:.1f} Z",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.path(
        f"M{x-16*s:.1f} {y-28*s:.1f} L{x-12*s:.1f} {y-48*s:.1f} L{x+12*s:.1f} {y-48*s:.1f} L{x+16*s:.1f} {y-28*s:.1f} Z",
        stroke=INK, fill=PARCHMENT, sw=sw,
    )
    d.line(x - 34 * s, y - 8 * s, x + 34 * s, y - 52 * s, stroke=INK, sw=sw * 0.55)
    d.line(x - 34 * s, y - 52 * s, x + 34 * s, y - 8 * s, stroke=INK, sw=sw * 0.55)


def gavel(d, x, y, s=1.0, sw=MSW):
    d.rect(x, y, 36 * s, 14 * s, rx=3, stroke=INK, fill=PARCHMENT, sw=sw)
    d.line(x + 18 * s, y + 14 * s, x + 28 * s, y + 40 * s, stroke=COPPER, sw=sw)


def planet(d, x, y, r=36, sw=MSW):
    d.circ(x, y, r, stroke=INK, fill=IVORY, sw=sw)
    d.path(
        f"M{x-r:.1f} {y+4:.1f} Q{x:.1f} {y-10:.1f} {x+r:.1f} {y+2:.1f}",
        stroke=COPPER, sw=sw * 0.7,
    )
    d.path(
        f"M{x-r*0.4:.1f} {y-r*0.2:.1f} Q{x:.1f} {y-r*0.55:.1f} {x+r*0.45:.1f} {y-r*0.15:.1f}",
        stroke=TEAL, sw=sw * 0.55,
    )


def flag(d, x, y, s=1.0, sw=MSW, shape="tri"):
    d.line(x, y, x, y - 70 * s, stroke=COPPER, sw=sw)
    if shape == "tri":
        d.poly(
            [(x, y - 70 * s), (x + 36 * s, y - 56 * s), (x, y - 42 * s)],
            stroke=INK, fill=PARCHMENT, sw=sw,
        )
    else:
        d.rect(x, y - 70 * s, 32 * s, 22 * s, stroke=INK, fill=IVORY, sw=sw)
        d.line(x, y - 59 * s, x + 32 * s, y - 59 * s, stroke=COPPER, sw=sw * 0.6)


def calendar(d, x, y, cols=7, rows=5, cw=22, ch=18, sw=MSW, marks=None):
    marks = marks or {}
    width = cols * cw
    height = rows * ch + 16
    d.rect(x, y, width, height, stroke=INK, fill=IVORY, sw=sw)
    d.rect(x, y, width, 16, stroke=INK, fill=PARCHMENT, sw=sw)
    for c in range(cols + 1):
        d.line(x + c * cw, y + 16, x + c * cw, y + height, stroke=LINE, sw=sw * 0.45)
    for r in range(rows + 1):
        d.line(x, y + 16 + r * ch, x + width, y + 16 + r * ch, stroke=LINE, sw=sw * 0.45)
    for (c, r), kind in marks.items():
        cx = x + c * cw + cw / 2
        cy = y + 16 + r * ch + ch / 2
        if kind == "dot":
            d.circ(cx, cy, 2.4, stroke=INK, fill=INK, sw=sw * 0.3)
        elif kind == "ring":
            d.circ(cx, cy, min(cw, ch) * 0.36, stroke=COPPER, sw=sw * 0.7)
        elif kind == "seal":
            d.circ(cx, cy, min(cw, ch) * 0.32, stroke=COPPER, fill=COPPER, sw=sw * 0.35)


def suitcase(d, x, y, s=1.0, sw=MSW, open_=False):
    if not open_:
        d.rect(x, y, 92 * s, 62 * s, rx=4, stroke=INK, fill=PARCHMENT, sw=sw)
        d.path(
            f"M{x+30*s:.1f} {y:.1f} V{y-16*s:.1f} H{x+62*s:.1f} V{y:.1f}",
            stroke=INK, sw=sw,
        )
        d.line(x + 46 * s, y, x + 46 * s, y + 62 * s, stroke=COPPER, sw=sw * 0.6)
        d.rect(x + 40 * s, y + 26 * s, 12 * s, 8 * s, stroke=COPPER, sw=sw * 0.6)
    else:
        d.rect(x, y + 20 * s, 100 * s, 58 * s, rx=3, stroke=INK, fill=PARCHMENT, sw=sw)
        d.poly(
            [(x + 8 * s, y + 20 * s), (x + 18 * s, y - 10 * s), (x + 92 * s, y - 4 * s), (x + 96 * s, y + 20 * s)],
            stroke=INK, fill=IVORY, sw=sw,
        )
        d.line(x, y + 48 * s, x + 100 * s, y + 48 * s, stroke=COPPER, sw=sw * 0.55)


def postcard(d, x, y, w=70, h=48, sw=MSW, tilt=0):
    d.group(f"translate({x:.2f} {y:.2f}) rotate({tilt:.1f})")
    d.rect(0, 0, w, h, stroke=INK, fill=IVORY, sw=sw)
    d.rect(w - 18, 6, 12, 14, stroke=COPPER, sw=sw * 0.6)
    d.line(8, h * 0.55, w * 0.62, h * 0.55, stroke=LINE, sw=sw * 0.5)
    d.line(8, h * 0.72, w * 0.5, h * 0.72, stroke=LINE, sw=sw * 0.5)
    d.end()


def bowl(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x-34*s:.1f} {y:.1f} Q{x:.1f} {y+28*s:.1f} {x+34*s:.1f} {y:.1f}",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.ell(x, y, 34 * s, 8 * s, stroke=INK, fill=PARCHMENT, sw=sw)


def bead(d, x, y, r=4.2, sw=1.4, fill=IVORY):
    d.circ(x, y, r, stroke=COPPER, fill=fill, sw=sw)


def jar(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x-26*s:.1f} {y-18*s:.1f} L{x-30*s:.1f} {y+36*s:.1f} Q{x:.1f} {y+48*s:.1f} {x+30*s:.1f} {y+36*s:.1f} "
        f"L{x+26*s:.1f} {y-18*s:.1f}",
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.rect(x - 20 * s, y - 30 * s, 40 * s, 14 * s, stroke=INK, fill=PARCHMENT, sw=sw)
    d.ell(x, y - 18 * s, 26 * s, 6 * s, stroke=INK, sw=sw)


def coin(d, x, y, r=8, sw=MSW):
    d.circ(x, y, r, stroke=COPPER, fill=GOLD, sw=sw * 0.7)
    d.circ(x, y, r * 0.45, stroke=COPPER, sw=sw * 0.45)


def die(d, x, y, s=1.0, sw=MSW):
    d.rect(x, y, 36 * s, 36 * s, rx=4, stroke=INK, fill=IVORY, sw=sw)
    for px, py in ((10, 10), (18, 18), (26, 26)):
        d.circ(x + px * s, y + py * s, 2.3 * s, stroke=INK, fill=INK, sw=sw * 0.3)


def veto(d, x, y, s=1.0, sw=MSW):
    d.circ(x, y, 8 * s, stroke=COPPER, sw=sw * 0.8)
    d.line(x - 5 * s, y - 5 * s, x + 5 * s, y + 5 * s, stroke=COPPER, sw=sw * 0.8)


def spectacles(d, x, y, s=1.0, sw=MSW):
    d.circ(x, y, 22 * s, stroke=INK, sw=sw, fill="none")
    d.circ(x + 52 * s, y, 22 * s, stroke=INK, sw=sw, fill="none")
    d.path(
        f"M{x+22*s:.1f} {y:.1f} Q{x+26*s:.1f} {y-8*s:.1f} {x+30*s:.1f} {y:.1f}",
        stroke=COPPER, sw=sw,
    )
    d.line(x - 22 * s, y, x - 36 * s, y + 4 * s, stroke=INK, sw=sw)
    d.line(x + 74 * s, y, x + 88 * s, y + 4 * s, stroke=INK, sw=sw)


def mountain(d, x, y, s=1.0, sw=MSW):
    d.poly(
        [(x, y), (x + 28 * s, y - 48 * s), (x + 48 * s, y - 22 * s), (x + 70 * s, y - 58 * s), (x + 104 * s, y)],
        stroke=INK, fill=IVORY, sw=sw,
    )


def plate(d, x, y, s=1.0, sw=MSW):
    d.ell(x, y, 28 * s, 12 * s, stroke=INK, fill=IVORY, sw=sw)
    d.ell(x, y, 16 * s, 7 * s, stroke=COPPER, sw=sw * 0.55)
    d.circ(x + 6 * s, y - 2 * s, 4 * s, stroke=INK, fill=PARCHMENT, sw=sw * 0.6)


def blanket(d, x, y, s=1.0, sw=MSW):
    d.rect(x, y, 78 * s, 48 * s, stroke=INK, fill=PARCHMENT, sw=sw)
    d.line(x, y + 16 * s, x + 78 * s, y + 16 * s, stroke=COPPER, sw=sw * 0.6)
    d.line(x + 8 * s, y, x + 8 * s, y + 48 * s, stroke=INK, sw=sw * 0.45)


def spool(d, x, y, s=1.0, sw=MSW):
    d.rect(x, y, 28 * s, 22 * s, stroke=INK, fill=IVORY, sw=sw)
    d.line(x, y, x, y + 22 * s, stroke=COPPER, sw=sw)
    d.line(x + 28 * s, y, x + 28 * s, y + 22 * s, stroke=COPPER, sw=sw)
    d.path(
        f"M{x+28*s:.1f} {y+8*s:.1f} C{x+48*s:.1f} {y-8*s:.1f} {x+40*s:.1f} {y+30*s:.1f} {x+70*s:.1f} {y+16*s:.1f}",
        stroke=COPPER, sw=sw * 0.7,
    )


def scale(d, x, y, s=1.0, sw=MSW, tilt=-8):
    d.line(x, y, x, y - 70 * s, stroke=INK, sw=sw)
    d.line(x - 24 * s, y, x + 24 * s, y, stroke=INK, sw=sw)
    d.group(f"translate({x:.2f} {y - 70 * s:.2f}) rotate({tilt:.1f})")
    d.line(-70 * s, 0, 70 * s, 0, stroke=COPPER, sw=sw)
    d.line(-58 * s, 0, -64 * s, 28 * s, stroke=INK, sw=sw * 0.7)
    d.line(-42 * s, 0, -36 * s, 28 * s, stroke=INK, sw=sw * 0.7)
    d.path(
        f"M{-70*s:.1f} {28*s:.1f} Q{-50*s:.1f} {40*s:.1f} {-30*s:.1f} {28*s:.1f}",
        stroke=INK, sw=sw,
    )
    d.line(42 * s, 0, 36 * s, 16 * s, stroke=INK, sw=sw * 0.7)
    d.line(58 * s, 0, 64 * s, 16 * s, stroke=INK, sw=sw * 0.7)
    d.path(
        f"M{30*s:.1f} {16*s:.1f} Q{50*s:.1f} {26*s:.1f} {70*s:.1f} {16*s:.1f}",
        stroke=INK, sw=sw,
    )
    d.end()


def umbrella_closed(d, x, y, s=1.0, sw=MSW):
    d.line(x, y, x + 8 * s, y - 120 * s, stroke=INK, sw=sw)
    d.path(
        f"M{x-6*s:.1f} {y-20*s:.1f} Q{x+4*s:.1f} {y-90*s:.1f} {x+16*s:.1f} {y-24*s:.1f}",
        stroke=TEAL, sw=sw,
    )
    d.path(
        f"M{x+4*s:.1f} {y-78*s:.1f} L{x+18*s:.1f} {y-70*s:.1f}",
        stroke=COPPER, sw=sw * 0.7,
    )


def kite(d, x, y, s=1.0, sw=MSW, string_to=None, accent=COPPER):
    d.poly(
        [(x, y - 36 * s), (x + 22 * s, y), (x, y + 42 * s), (x - 22 * s, y)],
        stroke=INK, fill=IVORY, sw=sw,
    )
    d.line(x, y - 36 * s, x, y + 42 * s, stroke=accent, sw=sw * 0.6)
    d.line(x - 22 * s, y, x + 22 * s, y, stroke=accent, sw=sw * 0.6)
    d.path(
        f"M{x:.1f} {y+42*s:.1f} q{6*s:.1f} {10*s:.1f} 0 {18*s:.1f} q{-8*s:.1f} {8*s:.1f} -2 {16*s:.1f}",
        stroke=accent, sw=sw * 0.6,
    )
    if string_to:
        d.line(x, y, string_to[0], string_to[1], stroke=INK, sw=sw * 0.55)


def shell(d, x, y, s=1.0, sw=PSW):
    d.path(
        f"M{x-20*s:.1f} {y:.1f} Q{x-18*s:.1f} {y-16*s:.1f} {x:.1f} {y-8*s:.1f} "
        f"Q{x+8*s:.1f} {y-28*s:.1f} {x+18*s:.1f} {y-6*s:.1f} "
        f"Q{x+28*s:.1f} {y+6*s:.1f} {x:.1f} {y+10*s:.1f} Q{x-16*s:.1f} {y+8*s:.1f} {x-20*s:.1f} {y:.1f} Z",
        stroke=TEAL, fill=IVORY, sw=sw,
    )
    d.path(
        f"M{x-8*s:.1f} {y+4*s:.1f} Q{x:.1f} {y-12*s:.1f} {x+10*s:.1f} {y+2*s:.1f}",
        stroke=TEAL, sw=sw * 0.6,
    )


def leaf(d, x, y, s=1.0, sw=MSW):
    d.path(
        f"M{x:.1f} {y:.1f} Q{x+16*s:.1f} {y-18*s:.1f} {x+4*s:.1f} {y-28*s:.1f} "
        f"Q{x-14*s:.1f} {y-16*s:.1f} {x:.1f} {y:.1f} Z",
        stroke=TEAL, fill=IVORY, sw=sw,
    )


def question_constellation(d, x, y, s=1.0, sw=DSW):
    pts = [
        (0.62, 0.05), (0.82, 0.16), (0.90, 0.34), (0.74, 0.50),
        (0.52, 0.60), (0.46, 0.74), (0.50, 0.86),
    ]
    abs_pts = [(x + px * 80 * s, y + py * 130 * s) for px, py in pts]
    for a, b in zip(abs_pts, abs_pts[1:]):
        d.line(a[0], a[1], b[0], b[1], stroke=GOLD, sw=sw)
    for px, py in abs_pts:
        star(d, px, py, 7 * s, sw=sw * 0.7)
    star(d, x + 0.50 * 80 * s, y + 1.02 * 130 * s, 8 * s, sw=sw * 0.7)


def floor_line(d, x1, x2, y, sw=DSW):
    d.line(x1, y, x2, y, stroke=LINE, sw=sw)


def wrapped(viewbox, width, height, label, body, decorative=False):
    if decorative:
        open_tag = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
            f'width="{width}" height="{height}" role="presentation" aria-hidden="true">'
        )
        title = ""
    else:
        open_tag = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
            f'width="{width}" height="{height}" role="img" aria-label="{xml(label)}">'
        )
        title = f"<title>{xml(label)}</title>"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        + open_tag
        + title
        + body
        + "\n</svg>\n"
    )


# --- chapter scenes -------------------------------------------------------

SCENES = {}


def scene(n):
    def deco(fn):
        SCENES[f"{n:03d}"] = fn
        return fn
    return deco


@scene(1)
def s001(d):
    # Two empty chairs; a question-mark constellation. Accent: gold.
    floor_line(d, 36, 250, 246)
    chair(d, 58, 244, s=1.05, face=1)
    chair(d, 214, 244, s=1.05, face=-1)
    question_constellation(d, 262, 28, s=1.15)


@scene(2)
def s002(d):
    book(d, 78, 78, w=86, h=112)
    ribbon(d, 150, 120, stroke=COPPER)
    lamp(d, 318, 214, s=1.15, stem=62)


@scene(3)
def s003(d):
    d.path("M40 200 C120 190 150 150 210 156 C280 164 300 120 390 108", stroke=COPPER, sw=MSW)
    for i, px in enumerate((70, 130, 190, 260)):
        stone(d, px, 188 - i * 12, s=0.85 + i * 0.04)
    hand_side(d, 318, 96, s=1.15, face=1)
    stone(d, 372, 92, s=0.7, fill=IVORY)


@scene(4)
def s004(d):
    hook(d, 210, 42, s=1.3)
    coat(d, 196, 70, s=1.25, hem=86)
    d.line(228, 58, 300, 96, stroke=COPPER, sw=DSW)
    paper_boat(d, 286, 112, s=0.85)


@scene(5)
def s005(d):
    # One question mark. The spoon is the hook, the ticket the descending
    # stroke, the key the stem, and the star the dot.
    spoon(d, 171, 107, s=1.75, rot=-125)
    ticket(d, 268, 58, w=100, h=28, rot=112)
    key(d, 222, 160, s=1.5, rot=90)
    star(d, 222, 258, 13)


@scene(6)
def s006(d):
    plinth(d, 36, 214, s=1.15)
    plinth(d, 150, 230, s=1.35)
    plinth(d, 290, 206, s=1.0)
    frame_rect(d, 348, 46, 62, 78, sw=MSW)


@scene(7)
def s007(d):
    d.path(
        "M36 168 C90 166 110 120 150 118 C190 116 200 150 230 86 "
        "C270 20 300 150 340 150 C380 150 390 120 412 124",
        stroke=COPPER, sw=MSW,
    )
    d.path(
        "M150 118 C170 150 210 188 250 176 C300 160 320 150 340 150",
        stroke=INK, sw=MSW,
    )


@scene(8)
def s008(d):
    page(d, 70, 48, w=250, h=190, lines=7)
    mask_half(d, 268, 70, s=1.35)


@scene(9)
def s009(d):
    envelope(d, 110, 96, w=200, h=110, flap="lifted", seal=True)


@scene(10)
def s010(d):
    bands = [46, 78, 112, 150, 190]
    for i, yy in enumerate(bands):
        d.path(
            f"M40 {yy} Q140 {yy - 16} 230 {yy} T420 {yy + 4}",
            stroke=INK if i < 4 else COPPER, sw=MSW if i == 4 else DSW,
        )
    d.rect(48, 36, 344, 176, stroke=LINE, sw=DSW, fill="none")
    lamp(d, 220, 228, s=0.55, stem=28, lit=True)


@scene(11)
def s011(d):
    hook(d, 200, 36, s=1.2)
    coat(d, 200, 78, s=1.05, hem=96, fill=TEAL, stroke=TEAL, sleeve_l=0.85, sleeve_r=0.85)
    coat(d, 200, 64, s=1.15, hem=70, fill=PARCHMENT)


@scene(12)
def s012(d):
    page(d, 70, 46, w=200, h=180, lines=6)
    d.rect(86, 62, 70, 22, stroke=COPPER, sw=DSW, fill="none")
    wax_seal(d, 330, 150, r=28, unused=True)
    d.line(292, 150, 318, 168, stroke=COPPER, sw=DSW)


@scene(13)
def s013(d):
    speech(d, 36, 48, w=180, h=90, tail="left")
    door(d, 270, 70, w=92, h=160)
    # Upper panel, inset from both stiles and clear of the rail and the knob.
    draw_word(d, "PASS", 292, 116, 15, stroke=INK, sw=2.2)


@scene(14)
def s014(d):
    cup(d, 210, 100, s=2.0, crack=True)


@scene(15)
def s015(d):
    d.rect(28, 24, 384, 232, stroke=INK, sw=MSW, fill="none")
    d.line(28, 200, 412, 200, stroke=LINE, sw=DSW)
    d.line(80, 24, 80, 256, stroke=LINE, sw=1.4)
    d.line(360, 24, 360, 256, stroke=LINE, sw=1.4)
    chair(d, 200, 198, s=0.42, face=1, sw=DSW)


@scene(16)
def s016(d):
    table(d, 250, 150, w=140, h=14)
    armor(d, 120, 230, s=1.15)


@scene(17)
def s017(d):
    profile(d, 150, 168, s=1.35, face=1)
    profile(d, 290, 168, s=1.35, face=-1)
    for i, xx in enumerate((78, 118, 330, 372)):
        minute_mark(d, xx, 70 + (i % 2) * 18, s=0.85)


@scene(18)
def s018(d):
    profile(d, 90, 150, s=1.05, face=1)
    profile(d, 360, 150, s=1.05, face=-1)
    d.path("M118 118 Q150 108 168 118", stroke=INK, sw=DSW)  # closed mouth already in profile
    hand_palm(d, 150, 230, s=0.55, flip=1)
    hand_palm(d, 250, 230, s=0.55, flip=-1)
    d.path("M168 150 C200 110 250 110 286 148", stroke=COPPER, sw=MSW)
    d.line(200, 132, 230, 124, stroke=COPPER, sw=DSW)
    d.line(214, 146, 246, 140, stroke=COPPER, sw=DSW)


@scene(19)
def s019(d):
    bench(d, 120, 176, w=200)
    d.path("M70 150 Q140 40 210 120", stroke=TEAL, sw=MSW)
    d.path("M370 150 Q300 40 230 120", stroke=TEAL, sw=MSW)


@scene(20)
def s020(d):
    profile(d, 100, 170, s=1.2, face=1)
    d.path("M128 124 Q140 118 136 128", stroke=COPPER, sw=DSW)  # open mouth
    d.line(124, 130, 138, 128, stroke=COPPER, sw=DSW)
    profile(d, 340, 170, s=1.2, face=-1)
    for i, yy in enumerate((88, 108, 128)):
        d.line(150, yy, 230, yy - 6, stroke=INK, sw=DSW)
        d.line(250, yy + 16, 176, yy + 8, stroke=TEAL, sw=DSW)


@scene(21)
def s021(d):
    # Offered in the hand. No head, so it cannot be worn.
    hand_side(d, 24, 86, s=1.15, face=1)
    blindfold(d, 62, 74, s=0.78)
    # Corridor: ceiling, two walls, a floor, and a door at the far end.
    d.poly([(188, 250), (430, 250), (392, 168), (226, 168)], stroke=INK, fill=PARCHMENT, sw=MSW)
    d.poly([(188, 28), (430, 28), (392, 78), (226, 78)], stroke=INK, fill=CHARCOAL, sw=MSW)
    d.poly([(188, 28), (226, 78), (226, 168), (188, 250)], stroke=INK, fill=IVORY, sw=MSW)
    d.poly([(430, 28), (392, 78), (392, 168), (430, 250)], stroke=INK, fill=IVORY, sw=MSW)
    d.rect(226, 78, 166, 90, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.rect(286, 98, 46, 70, stroke=INK, fill=IVORY, sw=DSW)
    d.circ(322, 136, 3.2, stroke=COPPER, fill=COPPER, sw=1.6)
    d.line(188, 214, 226, 156, stroke=COPPER, sw=DSW)
    d.line(430, 214, 392, 156, stroke=COPPER, sw=DSW)
    d.line(236, 250, 270, 168, stroke=LINE, sw=1.6)
    d.line(309, 250, 309, 168, stroke=LINE, sw=1.6)
    d.line(382, 250, 348, 168, stroke=LINE, sw=1.6)


@scene(22)
def s022(d):
    hand_palm(d, 210, 200, s=1.35)
    d.path("M120 214 H300", stroke=LINE, sw=DSW, dash="6 8")


@scene(23)
def s023(d):
    # Two clothed adults, still, not a dip or a clinch.
    d.path(
        "M150 210 L150 120 Q140 70 168 62 Q190 78 186 110 L210 150 L236 108 "
        "Q250 70 286 78 Q300 100 286 140 L286 210",
        stroke=INK, sw=MSW, fill="none",
    )
    d.circ(168, 58, 16, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.circ(274, 70, 16, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.path("M186 118 Q210 100 236 122", stroke=COPPER, sw=MSW)
    minute_mark(d, 340, 80, s=1.4)


@scene(24)
def s024(d):
    table(d, 70, 120, w=300, h=16)
    # Horizontal back of the phone on the table. Camera island, no screen.
    d.rect(124, 62, 192, 84, rx=12, stroke=INK, fill=CHARCOAL, sw=MSW)
    d.rect(142, 76, 44, 32, rx=6, stroke=LINE, fill=MIDNIGHT, sw=DSW)
    d.circ(156, 92, 6, stroke=COPPER, fill=COPPER, sw=1.6)
    d.circ(174, 92, 5, stroke=IVORY, fill=CHARCOAL, sw=1.6)


@scene(25)
def s025(d):
    key(d, 70, 70, s=1.1, rot=-20)
    cup(d, 168, 64, s=1.05)
    page(d, 230, 48, w=70, h=90, lines=4, tilt=-8)
    cloth(d, 48, 160, s=1.1, fill=PARCHMENT)
    spoon(d, 300, 150, s=1.0, rot=20)
    lamp(d, 360, 210, s=0.7, stem=40)


@scene(26)
def s026(d):
    card(d, 150, 150, w=150, h=70, tilt=-4, face="lines")
    card(d, 140, 112, w=150, h=70, tilt=-2, face="lines")
    card(d, 128, 70, w=150, h=78, tilt=2, face="blank")
    lamp(d, 196, 128, s=0.38, stem=26)


@scene(27)
def s027(d):
    clock(d, 220, 140, r=78, hour=4, minute=0)


@scene(28)
def s028(d):
    book(d, 70, 48, w=200, h=160, tilt=-6)
    d.group("translate(70 48) rotate(-6)")
    for i, yy in enumerate((36, 70, 104)):
        d.poly([(150, yy), (166, yy + 14), (150, yy + 28), (134, yy + 14)], stroke=COPPER, fill=IVORY, sw=DSW)
        d.circ(150, yy + 14, 3, stroke=INK, sw=1.4)
    d.end()


@scene(29)
def s029(d):
    card(d, 48, 40, w=90, h=180, face="lines")
    kettle(d, 210, 200, s=1.35)
    for i, kind in enumerate(("sun", "cloud", "rain", "wind")):
        weather(d, kind, 300 + (i % 2) * 70, 70 + (i // 2) * 90, s=1.0)


@scene(30)
def s030(d):
    table_top(d, 40, 90, w=360, depth=110)
    d.line(220, 100, 220, 185, stroke=COPPER, sw=MSW)
    card(d, 250, 108, w=78, h=58, face="lines")


@scene(31)
def s031(d):
    envelope(d, 70, 70, w=180, h=120, flap="closed", seal=True)
    d.line(280, 180, 400, 180, stroke=INK, sw=MSW)
    for i, xx in enumerate((290, 318, 346, 374)):
        d.line(xx, 168, xx, 192, stroke=COPPER if i == 3 else INK, sw=DSW)
    d.rect(360, 120, 36, 48, stroke=COPPER, fill=IVORY, sw=DSW)


@scene(32)
def s032(d):
    # Seven ordinary days, each with one copper mark. No axis and no score.
    cup(d, 48, 168, s=0.65)
    d.circ(48, 118, 4.5, stroke=COPPER, fill=COPPER, sw=1)
    key(d, 108, 176, s=0.72, rot=-28)
    d.circ(108, 108, 4.5, stroke=COPPER, fill=COPPER, sw=1)
    leaf(d, 168, 188)
    d.circ(164, 132, 4.5, stroke=COPPER, fill=COPPER, sw=1)
    spoon(d, 214, 160, s=0.62, rot=18)
    d.circ(214, 100, 4.5, stroke=COPPER, fill=COPPER, sw=1)
    book(d, 250, 150, w=34, h=46)
    d.circ(268, 136, 4.5, stroke=COPPER, fill=COPPER, sw=1)
    stone(d, 328, 196, s=0.75)
    d.circ(328, 150, 4.5, stroke=COPPER, fill=COPPER, sw=1)
    lamp(d, 390, 196, s=0.42, stem=28)
    d.circ(390, 128, 4.5, stroke=COPPER, fill=COPPER, sw=1)


@scene(33)
def s033(d):
    d.line(40, 150, 400, 150, stroke=INK, sw=MSW)
    for xx in (40, 140, 250, 400):
        d.line(xx, 140, xx, 160, stroke=COPPER, sw=DSW)
    spark(d, 110, 110, s=1.1)
    spark(d, 330, 86, s=1.35)


@scene(34)
def s034(d):
    labels = ("YES", "NO", "MAYBE")
    for i, word in enumerate(labels):
        x = 28 + i * 138
        d.rect(x, 48, 124, 180, rx=4, stroke=INK, fill=IVORY, sw=MSW)
        d.rect(x, 48, 124, 10, stroke=COPPER, fill=COPPER, sw=1)
        size = 36 if word != "MAYBE" else 24
        draw_word(d, word, x + 14, 160, size, sw=2.6)


@scene(35)
def s035(d):
    d.path("M40 60 C90 90 80 140 130 150 C180 160 160 80 230 100", stroke=LINE, sw=DSW)
    card(d, 36, 40, w=36, h=28, face="blank", tilt=-8)
    card(d, 90, 100, w=36, h=28, face="blank", tilt=6)
    card(d, 150, 70, w=36, h=28, face="blank", tilt=-4)
    table(d, 250, 140, w=150, h=12)
    d.ell(290, 138, 16, 6, stroke=INK, sw=DSW)
    d.ell(350, 136, 16, 6, stroke=INK, sw=DSW)
    cup(d, 318, 96, s=0.55)


@scene(36)
def s036(d):
    record(d, 70, 80, r=32)
    citrus(d, 150, 86, s=1.3)
    cloth(d, 40, 160, s=1.15, fill=BURGUNDY)
    glass(d, 250, 170, s=1.4, rim=GOLD)
    lamp(d, 360, 200, s=0.95, stem=50)


@scene(37)
def s037(d):
    hand_palm(d, 200, 230, s=1.45)
    locket(d, 214, 150, s=1.5, open_=False)


@scene(38)
def s038(d):
    feet_pair(d, 120, 170, s=1.3, face=1)
    feet_pair(d, 250, 176, s=1.25, face=-1)
    music_stand(d, 360, 210, s=1.15)


@scene(39)
def s039(d):
    d.rect(150, 40, 150, 200, stroke=INK, sw=MSW, fill="none")
    d.path("M150 40 Q225 10 300 40", stroke=COPPER, sw=MSW)
    d.line(225, 40, 225, 240, stroke=COPPER, sw=DSW)
    d.rect(168, 70, 40, 70, stroke=INK, sw=DSW)
    d.rect(246, 90, 36, 90, rx=2, stroke=INK, sw=DSW)
    d.circ(196, 150, 3, stroke=COPPER, fill=COPPER, sw=1)
    d.rect(258, 168, 10, 6, stroke=COPPER, sw=DSW)


@scene(40)
def s040(d):
    d.rect(40, 36, 360, 210, stroke=INK, sw=MSW, fill=IVORY)
    d.line(40, 140, 400, 140, stroke=INK, sw=DSW)
    d.line(210, 36, 210, 246, stroke=INK, sw=DSW)
    d.rect(300, 48, 70, 36, stroke=COPPER, sw=MSW, fill=GOLD)
    door(d, 70, 156, w=70, h=80, sw=DSW)
    d.line(78, 196, 132, 196, stroke=COPPER, sw=DSW)


@scene(41)
def s041(d):
    card(d, 40, 60, w=100, h=140, tilt=-3, face="lines")
    card(d, 160, 70, w=100, h=140, tilt=8, face="lines")
    card(d, 290, 58, w=100, h=140, tilt=-1, face="lines")


@scene(42)
def s042(d):
    d.path("M40 200 L200 200 L200 80", stroke=COPPER, sw=MSW, fill="none")
    d.path("M200 200 L360 200 L400 120", stroke=INK, sw=MSW, fill="none")
    hat(d, 186, 70, kind="silly", s=1.1)
    hat(d, 360, 110, kind="crown", s=1.0)


@scene(43)
def s043(d):
    paddle(d, 60, 70, s=1.3)
    paddle(d, 150, 80, s=1.2)
    cake(d, 320, 180, s=1.4)


@scene(44)
def s044(d):
    hook(d, 120, 36, s=1.0)
    hook(d, 300, 36, s=1.0)
    coat(d, 108, 58, s=1.05, sleeve_l=1.35, sleeve_r=0.45, hem=80)
    coat(d, 288, 58, s=1.05, sleeve_l=0.4, sleeve_r=1.4, hem=70, fill=IVORY)


@scene(45)
def s045(d):
    d.poly([(150, 200), (250, 200), (236, 120), (164, 120)], stroke=INK, fill=PARCHMENT, sw=MSW)
    d.rect(176, 88, 48, 32, stroke=COPPER, sw=DSW, fill=IVORY)
    cup(d, 200, 40, s=0.85)
    gavel(d, 300, 150, s=1.4)


@scene(46)
def s046(d):
    planet(d, 180, 140, r=70)
    flag(d, 250, 210, s=1.0, shape="tri")
    flag(d, 310, 230, s=0.85, shape="rect")


@scene(47)
def s047(d):
    words = ("TRUTH", "DARE", "DISCOVER")
    for i, word in enumerate(words):
        x = 24 + i * 142
        door(d, x, 70, w=112, h=160, sw=DSW)
        size = 18 if word != "DISCOVER" else 13
        draw_word(d, word, x + 8, 150, size, sw=1.8)
        key(d, x + 36, 214, s=0.7, rot=-20)


@scene(48)
def s048(d):
    calendar(d, 40, 40, cols=7, rows=4, cw=28, ch=28, marks={(1, 0): "dot", (4, 1): "dot", (2, 2): "dot"})
    envelope(d, 70, 78, w=36, h=24, sw=DSW, seal=True)
    envelope(d, 150, 120, w=36, h=24, sw=DSW, seal=True)
    envelope(d, 250, 90, w=40, h=26, sw=DSW, seal=True)


@scene(49)
def s049(d):
    d.rect(40, 36, 360, 210, stroke=INK, fill=IVORY, sw=MSW)
    d.path("M60 190 C140 160 180 120 250 130 C320 140 350 80 390 70", stroke=INK, sw=MSW + 0.8)
    d.path("M70 200 C150 180 190 150 260 150 C330 150 360 120 400 100", stroke=TEAL, sw=DSW, dash="7 6")
    d.circ(60, 190, 4, stroke=COPPER, fill=COPPER, sw=1)
    d.circ(390, 70, 4, stroke=COPPER, fill=COPPER, sw=1)


@scene(50)
def s050(d):
    table_top(d, 30, 120, w=380, depth=90)
    cup(d, 90, 78, s=0.8)
    key(d, 150, 100, s=0.85, rot=-15)
    book(d, 210, 70, w=48, h=58)
    spoon(d, 300, 86, s=0.8, rot=12)
    stone(d, 360, 108, s=0.7, fill=GOLD)


@scene(51)
def s051(d):
    frame_rect(d, 110, 30, 220, 210)
    profile(d, 230, 170, s=1.5, face=1, sw=DSW)
    d.path("M150 70 Q180 40 230 60", stroke=LINE, sw=DSW, dash="5 6")
    d.path("M250 150 Q270 140 286 156", stroke=LINE, sw=DSW, dash="4 5")


@scene(52)
def s052(d):
    stone(d, 150, 150, s=2.4, fill=LINE)
    stone(d, 168, 132, s=1.1, fill=IVORY, stroke=COPPER)
    d.line(156, 80, 210, 150, stroke=INK, sw=MSW)


@scene(53)
def s053(d):
    d.path("M40 60 L400 60 L360 200 L80 200 Z", stroke=INK, fill=PARCHMENT, sw=MSW)
    for row, yy in enumerate((90, 120, 150)):
        for i in range(6):
            d.rect(100 + i * 40, yy, 24, 16, stroke=INK, sw=DSW * 0.7, fill=IVORY)
    d.rect(40, 200, 360, 16, stroke=COPPER, fill=COPPER, sw=1)
    d.circ(220, 168, 8, stroke=INK, fill=PARCHMENT, sw=DSW)
    d.line(220, 176, 220, 198, stroke=INK, sw=DSW)
    d.line(208, 186, 232, 186, stroke=INK, sw=DSW)


@scene(54)
def s054(d):
    page(d, 40, 36, w=250, h=210, lines=8)
    # Original margin beast: a small winged quadruped, not a known character.
    d.path(
        "M300 150 Q320 80 360 90 Q390 70 400 110 Q420 100 410 140 "
        "Q440 150 400 170 L360 188 L340 170 Q300 180 300 150 Z",
        stroke=TEAL, fill="none", sw=MSW,
    )
    d.path("M360 90 Q340 60 370 70", stroke=TEAL, sw=DSW)
    d.line(330, 188, 322, 210, stroke=TEAL, sw=DSW)
    d.line(360, 190, 366, 214, stroke=TEAL, sw=DSW)


@scene(55)
def s055(d):
    d.line(60, 40, 60, 250, stroke=COPPER, sw=MSW)
    for yy in (70, 120, 170, 220):
        d.line(60, yy, 200, yy, stroke=LINE, sw=DSW)
    mountain(d, 210, 130, s=0.7)
    plate(d, 300, 210, s=1.2)
    cup(d, 360, 176, s=0.6)


@scene(56)
def s056(d):
    question_constellation(d, 40, 30, s=0.9)
    question_constellation(d, 180, 70, s=0.75)
    question_constellation(d, 300, 24, s=0.85)


@scene(57)
def s057(d):
    book(d, 40, 50, w=120, h=160)
    d.rect(40, 50, 18, 36, stroke=COPPER, fill=COPPER, sw=1)
    kettle(d, 230, 200, s=1.2)
    blanket(d, 300, 80, s=1.3)


@scene(58)
def s058(d):
    speech(d, 30, 40, w=160, h=80, shape="round", tail="left")
    speech(d, 230, 70, w=170, h=90, shape="square", tail="right")
    pencil(d, 180, 210, s=1.3, rot=-30)


@scene(59)
def s059(d):
    floor_line(d, 40, 400, 230)
    d.group("translate(120 230) rotate(-18)")
    chair(d, 0, 0, s=1.2, face=1)
    d.end()
    d.group("translate(300 230) rotate(18)")
    chair(d, 0, 0, s=1.2, face=-1)
    d.end()


@scene(60)
def s060(d):
    d.rect(40, 150, 360, 18, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.line(70, 168, 60, 230, stroke=INK, sw=MSW)
    d.line(370, 168, 380, 230, stroke=INK, sw=MSW)
    spool(d, 120, 110, s=1.4)
    d.line(248, 108, 318, 154, stroke=INK, sw=MSW)
    d.ell(244, 104, 7, 4, stroke=COPPER, sw=DSW)


@scene(61)
def s061(d):
    # A joke's outline, with an empty cup as the need inside it. No words.
    d.path(
        "M78 48 H330 Q372 48 372 92 V156 Q372 198 330 198 "
        "H214 L186 246 L176 198 H78 Q36 198 36 156 V92 Q36 48 78 48 Z",
        stroke=INK, fill=IVORY, sw=MSW,
    )
    cup(d, 204, 90, s=1.15)


@scene(62)
def s062(d):
    d.rect(36, 30, 368, 220, stroke=INK, fill=IVORY, sw=MSW)
    d.line(200, 30, 200, 250, stroke=INK, sw=DSW)
    d.line(36, 130, 404, 130, stroke=INK, sw=DSW)
    weather(d, "sun", 110, 78, s=0.7)
    weather(d, "sun", 300, 190, s=0.65)
    weather(d, "wind", 110, 190, s=0.8)
    weather(d, "wind", 300, 80, s=0.8)


@scene(63)
def s063(d):
    d.poly([(40, 80), (200, 60), (210, 200), (50, 210)], stroke=INK, fill=PARCHMENT, sw=MSW)
    d.path("M70 120 L120 140 L90 160 L150 180", stroke=INK, sw=DSW)
    d.poly([(230, 70), (400, 90), (380, 210), (220, 190)], stroke=INK, fill=IVORY, sw=MSW)
    star(d, 310, 140, 18, stroke=COPPER, fill="none", sw=DSW)
    d.line(200, 80, 230, 90, stroke=COPPER, sw=MSW)


@scene(64)
def s064(d):
    jar(d, 180, 120, s=1.6)
    for i, (xx, yy) in enumerate(((150, 150), (175, 160), (200, 148), (190, 175), (210, 168))):
        coin(d, xx, yy, r=7, sw=DSW)
    coin(d, 300, 80, r=10)
    d.path("M250 70 C280 40 310 50 300 80", stroke=COPPER, sw=DSW)
    for xx, yy in ((120, 70), (140, 48)):
        coin(d, xx, yy, r=8)
        d.path(f"M{xx} {yy+10} C{xx+10} {yy+30} 170 90 180 110", stroke=COPPER, sw=1.6)


@scene(65)
def s065(d):
    door(d, 120, 26, w=200, h=226, sw=MSW)
    # One lever. The door knob sits under the rose.
    d.rect(175, 142, 160, 16, rx=8, stroke=INK, fill=COPPER, sw=MSW)
    d.circ(304, 150, 11, stroke=INK, fill=IVORY, sw=MSW)
    # Forearms enter from opposite sides, then two separate hands.
    d.path(
        "M28 176 L28 152 L146 142 L152 164 L28 186 Z",
        stroke=INK, fill=PARCHMENT, sw=MSW,
    )
    d.path(
        "M412 180 L412 156 L362 146 L356 168 L412 190 Z",
        stroke=INK, fill=PARCHMENT, sw=MSW,
    )
    hand_side(d, 142, 146, s=1.25, face=1)
    hand_side(d, 358, 144, s=1.25, face=-1)


@scene(66)
def s066(d):
    # A bill folded once. Portrait, seal, and crease. No hull and no sail.
    d.rect(78, 64, 284, 62, rx=2, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.rect(58, 118, 324, 96, rx=3, stroke=INK, fill=IVORY, sw=MSW)
    d.line(58, 122, 382, 122, stroke=COPPER, sw=MSW)
    d.rect(74, 136, 292, 64, stroke=LINE, sw=1.6, fill="none")
    d.ell(186, 168, 28, 34, stroke=INK, fill=PARCHMENT, sw=DSW)
    d.circ(286, 162, 16, stroke=COPPER, sw=DSW, fill="none")
    d.circ(286, 162, 7, stroke=COPPER, sw=1.6, fill="none")
    d.rect(86, 142, 24, 16, stroke=COPPER, sw=1.6, fill="none")
    d.rect(330, 174, 24, 16, stroke=COPPER, sw=1.6, fill="none")


@scene(67)
def s067(d):
    d.circ(150, 140, 70, stroke=INK, sw=MSW, fill="none")
    d.circ(230, 150, 64, stroke=INK, sw=MSW, fill="none")
    d.circ(340, 80, 42, stroke=COPPER, sw=MSW, fill="none")


@scene(68)
def s068(d):
    die(d, 50, 80, s=1.8)
    veto(d, 120, 70, s=1.2)
    coin(d, 210, 120, r=28, sw=MSW)
    veto(d, 250, 80, s=1.2)
    card(d, 300, 70, w=80, h=110, face="blank")
    veto(d, 370, 60, s=1.2)


@scene(69)
def s069(d):
    for i, (xx, yy) in enumerate(((40, 60), (70, 100), (50, 140), (90, 160))):
        d.rect(xx, yy, 28, 16, stroke=INK, sw=DSW, fill=IVORY)
    for i, (xx, yy) in enumerate(((330, 70), (360, 110), (340, 150), (380, 170))):
        d.circ(xx, yy, 10, stroke=INK, sw=DSW, fill=PARCHMENT)
    # One built stool in the middle, parts still loose on either side.
    d.rect(170, 120, 90, 12, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.line(182, 132, 176, 200, stroke=COPPER, sw=MSW)
    d.line(248, 132, 256, 200, stroke=COPPER, sw=MSW)
    d.rect(196, 70, 36, 50, stroke=INK, fill=IVORY, sw=MSW)


@scene(70)
def s070(d):
    spectacles(d, 70, 130, s=1.8)
    mountain(d, 78, 150, s=0.42)
    d.path("M150 140 Q170 150 190 138", stroke=TEAL, sw=DSW)


@scene(71)
def s071(d):
    calendar(d, 70, 36, cols=7, rows=5, cw=40, ch=32, marks={(2, 2): "seal"})
    draw_word(d, "TUE", 168, 30, 16, stroke=INK, sw=1.8)


@scene(72)
def s072(d):
    d.poly([(40, 150), (400, 150), (400, 176), (40, 176)], stroke=INK, fill=PARCHMENT, sw=MSW)
    d.line(40, 150, 400, 150, stroke=COPPER, sw=MSW)
    # Two people stepping over, shown as legs only.
    d.path("M90 210 L110 150 L130 100", stroke=INK, sw=MSW)
    d.path("M150 210 L140 150 L160 96", stroke=INK, sw=MSW)
    d.path("M300 210 L280 148 L250 100", stroke=INK, sw=MSW)
    d.path("M340 210 L320 150 L300 98", stroke=INK, sw=MSW)
    d.circ(128, 92, 3, stroke=COPPER, fill=COPPER, sw=1)
    d.circ(252, 92, 3, stroke=COPPER, fill=COPPER, sw=1)


@scene(73)
def s073(d):
    page(d, 40, 40, w=160, h=200, lines=6)
    page(d, 230, 48, w=160, h=200, lines=5)
    draw_word(d, "1", 96, 78, 28, sw=2.4)
    draw_word(d, "1", 292, 86, 28, sw=2.4)


@scene(74)
def s074(d):
    cup(d, 90, 150, s=0.45)
    hand_side(d, 48, 150, s=0.55, face=1)
    d.circ(250, 130, 78, stroke=COPPER, fill=IVORY, sw=MSW)
    d.line(318, 176, 380, 230, stroke=COPPER, sw=MSW)
    cup(d, 250, 150, s=0.9)
    hand_side(d, 200, 150, s=0.7, face=1)


@scene(75)
def s075(d):
    d.path("M30 80 Q120 120 220 70 T410 100", stroke=COPPER, sw=MSW)
    ticket(d, 70, 96, w=60, h=32, rot=-8)
    speech(d, 180, 110, w=80, h=48, tail="left")
    frame_rect(d, 310, 120, 70, 54, sw=DSW)


@scene(76)
def s076(d):
    frame_rect(d, 30, 40, 170, 190)
    frame_rect(d, 230, 40, 170, 190)
    profile(d, 120, 160, s=1.15, face=1)
    profile(d, 320, 160, s=1.15, face=1, changed=True)


@scene(77)
def s077(d):
    d.path("M30 150 C80 140 100 170 150 160 C210 146 230 120 290 140 C340 156 370 120 410 130", stroke=INK, sw=MSW)
    for xx, yy in ((80, 146), (160, 158), (250, 132), (340, 150)):
        d.circ(xx, yy, 6, stroke=COPPER, fill=COPPER, sw=1)
        d.circ(xx, yy, 2, stroke=PARCHMENT, fill=PARCHMENT, sw=0.5)


@scene(78)
def s078(d):
    card(d, 80, 40, w=200, h=140, face="blank")
    d.line(100, 70, 240, 70, stroke=INK, sw=DSW)
    d.line(100, 92, 210, 92, stroke=INK, sw=DSW)
    d.line(100, 114, 180, 114, stroke=INK, sw=DSW)
    d.rect(230, 52, 32, 36, stroke=COPPER, sw=DSW)
    pencil(d, 300, 200, s=1.2, rot=-40)


@scene(79)
def s079(d):
    for i, xx in enumerate((60, 140, 220, 300, 380)):
        d.line(xx, 180, xx, 210, stroke=COPPER, sw=DSW)
    d.path(
        "M40 150 Q80 80 120 140 T200 120 T280 150 T360 90 T420 130",
        stroke=INK, sw=MSW,
    )
    for xx, yy in ((90, 112), (160, 128), (230, 118), (310, 108)):
        d.ell(xx, yy, 8, 6, stroke=GOLD, fill=GOLD, sw=0.8)
        d.line(xx + 8, yy, xx + 18, yy - 16, stroke=GOLD, sw=DSW)


@scene(80)
def s080(d):
    calendar(d, 40, 36, cols=7, rows=5, cw=36, ch=32, marks={(3, 2): "ring"})
    weather(d, "sun", 360, 70, s=1.1)
    weather(d, "rain", 360, 170, s=1.15)


@scene(81)
def s081(d):
    d.rect(50, 70, 160, 120, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.rect(80, 48, 100, 28, stroke=COPPER, fill=IVORY, sw=MSW)
    for i in range(4):
        d.line(70, 96 + i * 18, 180, 96 + i * 18, stroke=LINE, sw=DSW)
    card(d, 250, 120, w=50, h=36, face="blank", tilt=12)
    hand_side(d, 300, 110, s=1.1, face=1)


@scene(82)
def s082(d):
    scale(d, 220, 220, s=1.35, tilt=-12)


@scene(83)
def s083(d):
    d.path(
        "M160 40 H280 V150 Q270 210 220 220 Q160 210 150 150 Z",
        stroke=INK, fill=PARCHMENT, sw=MSW,
    )
    d.path("M150 150 Q120 180 150 210 Q190 190 170 160", stroke=INK, fill=IVORY, sw=MSW)
    d.circ(154, 196, 10, stroke=TEAL, fill=TEAL, sw=1)
    d.path("M150 190 Q158 186 156 198", stroke=IVORY, sw=1.4)


@scene(84)
def s084(d):
    d.line(40, 40, 40, 240, stroke=INK, sw=MSW)
    d.line(40, 240, 400, 240, stroke=INK, sw=DSW)
    d.path(
        "M120 240 L120 120 Q110 70 140 64 Q168 78 160 120 L160 240",
        stroke=INK, sw=MSW, fill="none",
    )
    d.circ(140, 62, 16, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.path(
        "M230 240 L250 130 Q270 80 320 100 Q340 140 300 160 L280 240 Z",
        stroke=INK, fill=MIDNIGHT, sw=MSW,
    )
    d.path("M286 124 Q292 120 298 126", stroke=PARCHMENT, sw=DSW)
    d.path("M284 146 Q296 150 308 144", stroke=PARCHMENT, sw=DSW)


@scene(85)
def s085(d):
    # A loose handwritten "if", legible as two letters, not a font.
    d.circ(168, 28, 4, stroke=INK, fill=INK, sw=1)
    d.path("M168 40 Q160 70 170 96", stroke=INK, sw=MSW)
    d.path("M210 96 Q200 20 250 18 Q270 40 236 58", stroke=INK, sw=MSW)
    d.line(214, 62, 258, 54, stroke=INK, sw=MSW)
    for i in range(3):
        door(d, 40 + i * 130, 110, w=100, h=140, sw=DSW)


@scene(86)
def s086(d):
    d.circ(80, 80, 28, stroke=COPPER, fill=IVORY, sw=MSW)
    d.line(68, 80, 92, 80, stroke=COPPER, sw=MSW)
    d.line(80, 68, 80, 92, stroke=COPPER, sw=MSW)
    d.line(80, 108, 80, 130, stroke=INK, sw=DSW)
    cup(d, 200, 120, s=1.4)
    cup(d, 320, 130, s=1.25)


@scene(87)
def s087(d):
    for i in range(4):
        y = 40 + i * 52
        x = 60 + i * 36
        d.poly([(x, y + 40), (x + 180 - i * 20, y + 40), (x + 160 - i * 20, y), (x + 20, y)], stroke=INK, fill=PARCHMENT, sw=MSW)
        d.path(
            f"M{x+70:.0f} {y+14:.0f} q14 -16 28 0 q8 18 0 22",
            stroke=COPPER, sw=DSW,
        )
        d.circ(x + 84, y + 40, 3, stroke=COPPER, fill=COPPER, sw=1)


@scene(88)
def s088(d):
    d.poly([(80, 40), (360, 70), (320, 230), (40, 190)], stroke=INK, fill=IVORY, sw=MSW)
    draw_word(d, "X", 120, 140, 36, sw=2.6)
    d.line(190, 100, 210, 140, stroke=INK, sw=MSW)
    d.line(170, 120, 230, 120, stroke=INK, sw=MSW)
    d.line(250, 130, 310, 130, stroke=COPPER, sw=MSW)
    d.line(250, 146, 310, 146, stroke=COPPER, sw=MSW)
    d.line(340, 150, 390, 160, stroke=LINE, sw=DSW, dash="4 6")


@scene(89)
def s089(d):
    page(d, 50, 30, w=230, h=210, blank=True)
    d.circ(250, 60, 16, stroke=COPPER, sw=DSW)
    pen(d, 300, 80, s=1.2, rot=-60)
    pen(d, 330, 150, s=1.15, rot=-40, color=COPPER)


@scene(90)
def s090(d):
    postcard(d, 80, 70, w=260, h=150, sw=MSW)
    d.circ(250, 150, 18, stroke=LINE, sw=DSW, fill="none")
    d.path("M120 120 Q180 100 230 130", stroke=COPPER, sw=DSW)


@scene(91)
def s091(d):
    d.rect(70, 30, 280, 220, stroke=INK, fill=IVORY, sw=MSW)
    draw_word(d, "MORE OF", 96, 78, 26, sw=2.2)
    d.line(96, 90, 300, 90, stroke=COPPER, sw=MSW)
    for yy in (120, 150, 180, 210):
        d.line(96, yy, 280, yy, stroke=LINE, sw=DSW)


@scene(92)
def s092(d):
    kite(d, 140, 90, s=1.3, string_to=(80, 250), accent=COPPER)
    kite(d, 300, 70, s=1.15, string_to=(360, 250), accent=TEAL)


@scene(93)
def s093(d):
    suitcase(d, 80, 80, s=2.0, open_=True)
    page(d, 120, 120, w=70, h=40, lines=3, sw=DSW)
    ticket(d, 200, 130, w=40, h=22, sw=DSW)


@scene(94)
def s094(d):
    door(d, 160, 30, w=120, h=210, ajar=0.45, sw=MSW)
    d.path("M70 80 Q90 140 70 200", stroke=INK, sw=DSW)
    d.path("M330 60 Q360 120 340 200", stroke=TEAL, sw=MSW)
    leaf(d, 348, 120, s=1.2)
    leaf(d, 360, 160, s=0.9)


@scene(95)
def s095(d):
    card(d, 120, 70, w=160, h=100, face="blank")
    d.line(146, 118, 230, 118, stroke=INK, sw=MSW)
    d.path("M250 78 Q270 60 262 96 Q250 110 268 120", stroke=COPPER, sw=MSW)


@scene(96)
def s096(d):
    d.poly([(40, 50), (200, 36), (210, 230), (50, 240)], stroke=INK, fill=IVORY, sw=MSW)
    for yy in (80, 110, 140, 170):
        d.line(70, yy, 180, yy - 6, stroke=LINE, sw=DSW)
    d.poly([(210, 36), (380, 50), (370, 240), (210, 230)], stroke=INK, fill=PARCHMENT, sw=MSW)
    d.line(250, 80, 340, 86, stroke=LINE, sw=1.2, dash="3 8")
    for i, xx in enumerate((400, 412)):
        d.line(xx, 70, xx - 6, 220, stroke=LINE, sw=DSW)


@scene(97)
def s097(d):
    d.rect(40, 80, 250, 140, stroke=INK, fill=PARCHMENT, sw=MSW)
    d.rect(70, 110, 120, 36, stroke=COPPER, fill=IVORY, sw=DSW)
    d.path("M150 110 L190 70 L230 86 L176 128 Z", stroke=COPPER, fill=IVORY, sw=MSW)
    # Fan brush
    d.line(300, 200, 360, 80, stroke=INK, sw=MSW)
    for i in range(-3, 4):
        d.line(360, 80, 360 + i * 8, 48, stroke=COPPER, sw=DSW)


@scene(98)
def s098(d):
    cup(d, 90, 80, s=1.5, worn=True)
    cup(d, 190, 90, s=1.35, worn=True)
    card(d, 280, 40, w=50, h=70, face="blank", tilt=-4)
    card(d, 320, 90, w=50, h=70, face="blank", tilt=3)
    card(d, 300, 160, w=50, h=70, face="blank")


@scene(99)
def s099(d):
    table_top(d, 30, 80, w=380, depth=130)
    cup(d, 120, 70, s=1.3)
    book(d, 220, 60, w=80, h=60)
    # Small enough to miss beside the cup and the book. Every stroke
    # is at least 1.6 units, about half a point at the 2.20 in placement.
    def small_postcard(x, y, w, h, tilt):
        d.group(f"translate({x:.2f} {y:.2f}) rotate({tilt:.1f})")
        d.rect(0, 0, w, h, stroke=INK, fill=IVORY, sw=1.6)
        d.rect(w - 14, 3, 10, 8, stroke=COPPER, sw=1.6)
        d.line(4, h * 0.62, w * 0.55, h * 0.62, stroke=INK, sw=1.6)
        d.end()

    small_postcard(58, 148, 40, 26, -4)
    small_postcard(236, 158, 36, 24, 7)
    small_postcard(328, 142, 34, 22, -6)


@scene(100)
def s100(d):
    d.path(
        "M40 80 Q120 40 200 90 Q280 40 360 100 Q400 160 340 200 Q220 240 80 190 Q20 150 40 80 Z",
        stroke=INK, fill=IVORY, sw=MSW,
    )
    weather(d, "sun", 120, 110, s=0.6)
    weather(d, "cloud", 220, 120, s=0.6)
    weather(d, "rain", 300, 140, s=0.55)
    umbrella_closed(d, 380, 230, s=0.85)


@scene(101)
def s101(d):
    hat(d, 130, 90, kind="brim", s=1.4)
    hat(d, 280, 86, kind="cap", s=1.5)
    card(d, 150, 140, w=140, h=90, face="lines")


@scene(102)
def s102(d):
    d.rect(30, 40, 180, 190, stroke=INK, fill=IVORY, sw=MSW)
    d.rect(230, 40, 180, 190, stroke=INK, fill=PARCHMENT, sw=MSW)
    clock(d, 120, 110, r=28, sw=DSW, hour=3, minute=0)
    d.path("M300 90 Q330 70 350 100 Q340 130 310 120 Q290 110 300 90 Z", stroke=COPPER, sw=DSW)
    d.circ(328, 100, 4, stroke=INK, sw=DSW)
    for yy in (160, 184):
        d.line(50, yy, 180, yy, stroke=LINE, sw=DSW)
        d.line(250, yy, 380, yy, stroke=LINE, sw=DSW)


@scene(103)
def s103(d):
    d.rect(30, 30, 250, 210, stroke=INK, fill=IVORY, sw=MSW)
    d.rect(50, 50, 90, 70, stroke=COPPER, sw=DSW)
    d.line(150, 50, 150, 120, stroke=COPPER, sw=DSW)
    d.rect(160, 50, 90, 70, stroke=COPPER, sw=DSW, dash="5 4")
    d.circ(250, 180, 16, stroke=INK, sw=MSW)
    key(d, 300, 150, s=1.0, rot=-10)
    key(d, 360, 170, s=1.0, rot=15)
    d.path("M330 168 Q300 200 262 186", stroke=COPPER, sw=DSW)


@scene(104)
def s104(d):
    d.rect(30, 40, 250, 190, stroke=INK, fill=IVORY, sw=MSW)
    d.path("M50 150 H120 V100 H170 V160 H250", stroke=COPPER, sw=DSW)
    d.rect(70, 70, 28, 22, stroke=INK, sw=DSW)
    d.rect(180, 80, 36, 26, stroke=INK, sw=DSW)
    d.poly([(300, 70), (400, 60), (410, 120), (360, 170), (290, 140)], stroke=TEAL, fill=IVORY, sw=MSW)
    for xx in (320, 345, 370):
        d.line(xx, 90, xx - 6, 130, stroke=TEAL, sw=DSW)


@scene(105)
def s105(d):
    codes = ("dots", "bars", "star", "key", "ring")
    for i, kind in enumerate(codes):
        y = 24 + i * 50
        ticket(d, 40, y, w=360, h=40, sw=DSW)
        if kind == "dots":
            for k in range(3):
                d.circ(80 + k * 16, y + 20, 3, stroke=INK, fill=INK, sw=1)
        elif kind == "bars":
            d.line(80, y + 12, 80, y + 28, stroke=INK, sw=DSW)
            d.line(92, y + 8, 92, y + 32, stroke=INK, sw=DSW)
        elif kind == "star":
            star(d, 90, y + 20, 8, sw=1.2)
        elif kind == "key":
            key(d, 80, y + 20, s=0.45, rot=0, sw=DSW)
        else:
            d.circ(90, y + 20, 8, stroke=COPPER, sw=DSW)


@scene(106)
def s106(d):
    bowl(d, 124, 178, s=1.55)
    bowl(d, 318, 182, s=1.45)
    # One hundred beads. Stroke 1.6 so the rings hold at the 2.20 in placement.
    spots = []
    for i in range(40):
        col, row = i % 8, i // 8
        spots.append((76 + col * 12 + (5 if row % 2 else 0), 146 + row * 10))
    for i in range(40):
        col, row = i % 8, i // 8
        spots.append((270 + col * 12 + (5 if row % 2 else 0), 150 + row * 10))
    for i in range(20):
        col, row = i % 10, i // 10
        spots.append((148 + col * 15, 72 + row * 18))
    for i, (x, y) in enumerate(spots):
        bead(d, x, y, r=3.5, sw=1.6, fill=IVORY if i % 3 else PARCHMENT)


@scene(107)
def s107(d):
    page(d, 70, 36, w=280, h=210, lines=7)
    star(d, 300, 120, 14)


@scene(108)
def s108(d):
    # Corridor of doors, keys that can be offered or kept.
    hallway(d, 30, 40, w=200, h=200, sw=DSW)
    door(d, 250, 36, w=50, h=100, sw=DSW)
    door(d, 320, 50, w=50, h=110, sw=DSW, ajar=0.35)
    door(d, 386, 70, w=40, h=90, sw=DSW)
    key(d, 70, 200, s=0.8, rot=-25)
    hand_palm(d, 150, 230, s=0.5)
    key(d, 300, 200, s=0.7, rot=20)
    d.path("M360 210 Q400 190 410 220 Q390 240 370 228", stroke=INK, fill=PARCHMENT, sw=DSW)


assert len(SCENES) == 108, len(SCENES)


# --- part openers: places, not enlarged chapter motifs -------------------

def part_frame(d: Draw):
    d.rect(8, 8, 524, 424, stroke=COPPER, fill=PARCHMENT, sw=1.1)


def part_01(d: Draw):
    part_frame(d)
    # Midnight window behind a library table seen from one end.
    d.rect(70, 28, 400, 150, stroke=INK, fill=MIDNIGHT, sw=PSW)
    d.line(270, 28, 270, 178, stroke=CHARCOAL, sw=PSW)
    d.line(70, 100, 470, 100, stroke=CHARCOAL, sw=1.4)
    star(d, 140, 62, 7, sw=1.2)
    star(d, 360, 54, 6, sw=1.1)
    star(d, 400, 90, 5, sw=1.0)
    d.line(120, 48, 168, 130, stroke=COPPER, sw=1.3)
    # Table receding from the near edge.
    d.poly([(48, 400), (492, 400), (360, 188), (180, 188)], stroke=INK, fill=PARCHMENT, sw=PSW)
    # Blank pages down the center, growing toward the viewer.
    for i in range(5):
        t = i / 4
        cx = 270
        cy = 210 + t * 150
        pw = 18 + t * 54
        ph = 10 + t * 22
        d.rect(cx - pw / 2, cy - ph / 2, pw, ph, stroke=INK, fill=IVORY, sw=1.4)
    # Uneven book stacks.
    def stack(x, y, widths, heights):
        yy = y
        for w, h in zip(widths, heights):
            yy -= h
            d.rect(x, yy, w, h, stroke=INK, fill=IVORY, sw=1.5)
            d.line(x + 4, yy, x + 4, yy + h, stroke=COPPER, sw=1.1)
    stack(86, 360, [54, 62, 48, 70], [12, 16, 10, 14])
    stack(360, 300, [46, 58], [14, 11])
    # Two lamps of unequal height.
    lamp(d, 130, 332, s=1.15, sw=PSW, stem=78)
    lamp(d, 400, 268, s=0.85, sw=PSW, stem=42)


def part_02(d: Draw):
    part_frame(d)
    # Tall window. Shade hem sits at the sill; the lower pane is solid night.
    d.rect(150, 28, 240, 360, stroke=INK, sw=PSW, fill="none")
    d.rect(162, 248, 216, 128, stroke=INK, fill=MIDNIGHT, sw=PSW)
    d.rect(162, 40, 216, 208, stroke=INK, fill=PARCHMENT, sw=1.6)
    for yy in (70, 110, 150, 190):
        d.path(f"M174 {yy} Q270 {yy+8} 366 {yy}", stroke=LINE, sw=1.3)
    d.line(162, 248, 378, 248, stroke=COPPER, sw=PSW)  # sill / hem
    d.rect(230, 28, 80, 16, stroke=INK, fill=CHARCOAL, sw=1.4)  # roller
    d.path("M300 36 C330 36 328 120 336 248", stroke=COPPER, sw=1.6)
    d.circ(336, 248, 3, stroke=COPPER, fill=COPPER, sw=0.8)
    lamp(d, 110, 360, s=0.9, sw=PSW, stem=48)
    chair(d, 420, 390, s=0.85, face=-1, sw=PSW)


def part_03(d: Draw):
    part_frame(d)
    d.rect(36, 36, 160, 120, stroke=INK, fill=MIDNIGHT, sw=PSW)
    d.line(116, 36, 116, 156, stroke=CHARCOAL, sw=1.4)
    table(d, 70, 250, w=400, h=16, sw=PSW)
    cup(d, 180, 196, s=1.3, sw=PSW)
    cup(d, 340, 200, s=1.2, sw=PSW)
    # Open pocket watch between the cups.
    d.circ(260, 214, 28, stroke=INK, fill=IVORY, sw=PSW)
    d.circ(214, 200, 26, stroke=INK, fill=PARCHMENT, sw=PSW)
    d.rect(236, 196, 10, 8, stroke=COPPER, fill=COPPER, sw=0.8)
    d.line(260, 214, 260, 196, stroke=INK, sw=1.6)
    d.line(260, 214, 274, 222, stroke=COPPER, sw=1.6)
    d.path("M250 250 C250 300 230 320 210 340", stroke=COPPER, sw=1.4)
    d.path("M150 150 Q260 70 370 150", stroke=TEAL, sw=PSW)


def part_04(d: Draw):
    part_frame(d)
    d.line(36, 300, 500, 300, stroke=INK, sw=PSW)
    door(d, 360, 70, w=120, h=230, sw=PSW)
    d.line(78, 214, 78, 300, stroke=INK, sw=PSW)
    hook(d, 78, 120, s=1.15, sw=PSW)
    # Two different keys on one ring.
    d.circ(78, 168, 10, stroke=COPPER, sw=PSW, fill="none")
    key(d, 96, 176, s=1.15, rot=70, sw=PSW)
    key(d, 58, 188, s=0.85, rot=110, sw=PSW)
    wall_lamp(d, 180, 100, s=1.35, sw=PSW, lit=True)


def part_05(d: Draw):
    part_frame(d)
    # Hall floor and a dark room beyond the threshold.
    d.poly([(0, 440), (540, 440), (420, 200), (120, 200)], stroke=INK, fill=PARCHMENT, sw=1.2)
    d.rect(150, 36, 240, 180, stroke=INK, fill=MIDNIGHT, sw=PSW)
    d.line(150, 200, 120, 440, stroke=INK, sw=PSW)
    d.line(390, 200, 420, 440, stroke=INK, sw=PSW)
    # Burgundy drape, half drawn.
    d.poly([(150, 36), (250, 36), (250, 300), (168, 320), (150, 200)], stroke=INK, fill=BURGUNDY, sw=PSW)
    d.path("M250 80 Q270 140 248 200", stroke=BURGUNDY, sw=1.5)
    # Two empty pairs. Stacked heel, sole, toe cap, open collar.
    def shoe(px, py, face=1):
        def X(v):
            return px + face * v
        def Y(v):
            return py + v
        d.path(
            f"M{X(4):.1f} {Y(0):.1f} L{X(4):.1f} {Y(-18):.1f} L{X(18):.1f} {Y(-20):.1f} "
            f"L{X(24):.1f} {Y(-38):.1f} L{X(54):.1f} {Y(-38):.1f} L{X(60):.1f} {Y(-26):.1f} "
            f"L{X(78):.1f} {Y(-28):.1f} Q{X(108):.1f} {Y(-26):.1f} {X(106):.1f} {Y(-8):.1f} "
            f"L{X(98):.1f} {Y(0):.1f} L{X(22):.1f} {Y(2):.1f} Z",
            stroke=INK, fill=IVORY, sw=PSW,
        )
        d.path(
            f"M{X(0):.1f} {Y(2):.1f} L{X(26):.1f} {Y(2):.1f} L{X(24):.1f} {Y(12):.1f} L{X(2):.1f} {Y(12):.1f} Z",
            stroke=INK, fill=PARCHMENT, sw=PSW,
        )
        d.line(X(22), Y(2), X(22), Y(-18), stroke=INK, sw=1.6)
        d.line(X(60), Y(-26), X(90), Y(-12), stroke=INK, sw=1.6)
        d.path(
            f"M{X(26):.1f} {Y(-34):.1f} Q{X(40):.1f} {Y(-28):.1f} {X(52):.1f} {Y(-34):.1f}",
            stroke=COPPER, sw=1.8,
        )

    shoe(118, 336, 1)
    shoe(140, 388, 1)
    shoe(286, 332, 1)
    shoe(308, 384, 1)
    lamp(d, 470, 400, s=0.7, sw=PSW, stem=36, lit=True)


def part_06(d: Draw):
    part_frame(d)
    d.poly([(20, 300), (520, 280), (500, 400), (40, 420)], stroke=INK, fill=PARCHMENT, sw=PSW)
    # Chessboard at the edge of the table.
    ox, oy, cw = 180, 150, 28
    for r in range(8):
        for c in range(8):
            fill = CHARCOAL if (r + c) % 2 == 0 else IVORY
            d.rect(ox + c * cw, oy + r * cw * 0.55, cw, cw * 0.55, stroke=INK, fill=fill, sw=0.6)
    # Pawn on the board with a paper crown.

    def pawn(px, py, scale=1.0):
        d.poly(
            [
                (px - 10 * scale, py),
                (px + 10 * scale, py),
                (px + 7 * scale, py - 16 * scale),
                (px - 7 * scale, py - 16 * scale),
            ],
            stroke=INK, fill=PARCHMENT, sw=PSW,
        )
        d.circ(px, py - 26 * scale, 8 * scale, stroke=INK, fill=IVORY, sw=PSW)

    pawn(180 + 4 * 28 + 14, 150 + 5 * 28 * 0.55, 1.0)
    hat(d, 180 + 4 * 28 + 14, 150 + 5 * 28 * 0.55 - 40, kind="crown", s=0.7, sw=1.6)
    # Knight off the board: plinth, mane, ear, and snout. No eye, no smile.
    d.path("M42 372 H156 L146 356 H52 Z", stroke=INK, fill=PARCHMENT, sw=PSW)
    d.path("M58 356 H140 L130 342 H68 Z", stroke=INK, fill=IVORY, sw=PSW)
    d.path(
        "M78 342 C70 300 64 268 70 236 C74 214 66 196 80 184 "
        "L64 162 L94 188 C112 166 140 168 160 178 L176 196 L164 210 "
        "C146 216 128 228 118 252 C112 288 120 322 128 342 Z",
        stroke=INK, fill=IVORY, sw=PSW,
    )
    d.path("M74 230 C88 248 84 280 92 312", stroke=COPPER, sw=1.6)
    d.path("M86 210 C98 232 94 268 102 300", stroke=COPPER, sw=1.6)


def part_07(d: Draw):
    part_frame(d)
    page(d, 140, 250, w=260, h=150, sw=PSW, lines=0, blank=True)
    d.line(270, 250, 270, 150, stroke=INK, sw=PSW)
    d.circ(270, 150, 8, stroke=COPPER, fill=COPPER, sw=1)
    arms = [
        (-70, -20, "stair"),
        (20, -80, "seed"),
        (90, -10, "eye"),
        (-10, 40, "lamp"),
    ]
    # Four teal arms, different lengths, ending in the four "planets".
    specs = [
        (180, 90, "stair"),
        (270, 46, "seed"),
        (380, 110, "eye"),
        (330, 200, "lamp"),
    ]
    for x, y, kind in specs:
        d.line(270, 150, x, y, stroke=TEAL, sw=PSW)
        if kind == "stair":
            d.poly([(x - 16, y + 10), (x - 4, y + 10), (x - 4, y), (x + 8, y), (x + 8, y - 10), (x + 20, y - 10), (x + 20, y - 18), (x - 16, y - 18)], stroke=INK, fill=IVORY, sw=1.5)
        elif kind == "seed":
            d.path(f"M{x} {y+12} Q{x+14} {y} {x} {y-14} Q{x-14} {y} {x} {y+12} Z", stroke=INK, fill=IVORY, sw=1.5)
        elif kind == "eye":
            d.path(f"M{x-18} {y} Q{x} {y-12} {x+18} {y} Q{x} {y+12} {x-18} {y} Z", stroke=INK, fill=IVORY, sw=1.5)
            d.path(f"M{x-18} {y} Q{x} {y-6} {x+18} {y}", stroke=INK, sw=1.3)
        else:
            lamp(d, x, y + 28, s=0.4, sw=1.5, stem=22)


def part_08(d: Draw):
    part_frame(d)
    # Rain outside the porch, dry boards under the eave.
    d.rect(8, 8, 524, 200, stroke="none", fill=CHARCOAL, sw=0)
    for i in range(18):
        x = 20 + i * 28
        d.line(x, 16, x - 18, 190, stroke=TEAL, sw=1.5)
    d.poly([(8, 150), (540, 130), (540, 168), (8, 190)], stroke=INK, fill=CHARCOAL, sw=PSW)  # eave
    d.rect(8, 190, 524, 242, stroke=INK, fill=PARCHMENT, sw=0)
    d.line(40, 168, 40, 420, stroke=INK, sw=PSW)
    d.line(500, 150, 500, 420, stroke=INK, sw=PSW)
    for yy in (300, 330, 360, 390):
        d.line(20, yy, 520, yy - 8, stroke=LINE, sw=1.2)
    door(d, 70, 200, w=90, h=160, ajar=0.4, sw=PSW)
    cup(d, 230, 300, s=1.1, sw=PSW)
    cup(d, 400, 292, s=1.0, sw=PSW)
    # Copper lantern on the dry boards.
    d.rect(300, 300, 36, 28, stroke=COPPER, fill=IVORY, sw=PSW)
    d.line(318, 300, 318, 286, stroke=COPPER, sw=1.6)
    d.path("M306 286 H330", stroke=COPPER, sw=1.6)
    d.line(306, 314, 330, 314, stroke=GOLD, sw=1.2)


def part_09(d: Draw):
    part_frame(d)
    d.rect(8, 8, 524, 180, stroke="none", fill=CHARCOAL, sw=0)
    d.rect(8, 188, 524, 244, fill=PARCHMENT, stroke="none", sw=0)
    d.line(8, 188, 532, 188, stroke=INK, sw=PSW)
    d.line(8, 300, 532, 300, stroke=COPPER, sw=PSW)  # platform edge
    for i in range(8):
        d.line(30 + i * 64, 300, 30 + i * 64, 420, stroke=LINE, sw=1.3)
    # Destination board, place-name only half written.
    d.rect(300, 40, 200, 110, stroke=INK, fill=IVORY, sw=PSW)
    d.line(300, 70, 500, 70, stroke=COPPER, sw=1.4)
    draw_word(d, "KA", 318, 100, 22, sw=2.0)
    d.path("M390 78 L410 96", stroke=INK, sw=2.2)
    d.line(416, 88, 470, 88, stroke=LINE, sw=1.4, dash="4 5")
    suitcase(d, 60, 214, s=1.3, sw=PSW)
    hand_side(d, 180, 230, s=1.3, face=1, sw=PSW)
    ticket(d, 230, 214, w=48, h=26, sw=1.6, fill=COPPER, stroke=INK, accent=INK)
    ticket(d, 248, 228, w=48, h=26, rot=-8, sw=1.6, fill=COPPER, stroke=INK, accent=INK)


def part_10(d: Draw):
    part_frame(d)
    d.rect(36, 28, 468, 250, stroke=INK, fill=IVORY, sw=PSW)
    d.line(36, 278, 504, 278, stroke=COPPER, sw=PSW)  # sill
    d.rect(36, 278, 468, 28, stroke=INK, fill=PARCHMENT, sw=PSW)
    # Photograph turned toward the glass, thin gold edge, faded image.
    d.group("translate(90 150) rotate(-8)")
    d.rect(0, 0, 120, 90, stroke=GOLD, fill=PARCHMENT, sw=1.6)
    d.path("M16 70 L40 40 L60 58 L80 30 L104 70", stroke=LINE, sw=1.6)
    d.circ(78, 28, 6, stroke=LINE, sw=1.4)
    d.end()
    cup(d, 280, 230, s=1.15, sw=PSW)
    d.ell(280, 270, 26, 6, stroke=COPPER, sw=1.3)  # heat ring
    page(d, 350, 200, w=110, h=70, sw=1.6, blank=True)
    pencil(d, 400, 196, s=1.0, rot=8, sw=1.6)


def part_11(d: Draw):
    part_frame(d)
    d.rect(170, 24, 200, 392, stroke=INK, fill=PARCHMENT, sw=PSW)
    for i in range(7):
        y = 40 + i * 52
        open_drawer = i == 3
        if open_drawer:
            d.rect(150, y, 240, 40, stroke=INK, fill=IVORY, sw=PSW)
            shell(d, 270, y + 22, s=1.1, sw=1.6)
        else:
            d.rect(186, y, 168, 40, stroke=INK, fill=IVORY, sw=1.5)
        d.rect(258, y + 16, 28, 8, stroke=COPPER, fill=COPPER, sw=0.8)


def part_12(d: Draw):
    part_frame(d)
    d.rect(36, 24, 468, 300, stroke=INK, fill=IVORY, sw=PSW)
    d.rect(36, 250, 468, 74, stroke="none", fill=GOLD, sw=0)  # horizon band
    d.circ(400, 250, 28, stroke=GOLD, fill=GOLD, sw=1)
    d.line(36, 324, 504, 324, stroke=COPPER, sw=PSW)  # sill
    # Pencil path on the glass from the sill toward the sun.
    d.path("M180 324 C240 280 300 260 390 250", stroke=COPPER, sw=PSW)
    pencil(d, 150, 340, s=1.15, rot=6, sw=PSW)
    chair(d, 80, 420, s=1.0, face=1, sw=PSW)
    chair(d, 230, 420, s=1.0, face=1, sw=PSW)


def part_13(d: Draw):
    part_frame(d)
    d.rect(30, 250, 480, 22, stroke=INK, fill=PARCHMENT, sw=PSW)
    d.line(60, 272, 40, 410, stroke=INK, sw=PSW)
    d.line(480, 272, 500, 410, stroke=INK, sw=PSW)
    d.poly([(40, 410), (500, 410), (480, 272), (60, 272)], stroke="none", fill=MIDNIGHT, sw=0)
    # Screw press.
    d.line(80, 250, 80, 90, stroke=INK, sw=PSW)
    d.line(180, 250, 180, 90, stroke=INK, sw=PSW)
    d.line(70, 90, 190, 90, stroke=INK, sw=PSW)
    d.line(130, 90, 130, 160, stroke=COPPER, sw=PSW)
    d.line(100, 120, 160, 120, stroke=COPPER, sw=PSW)
    d.rect(96, 160, 68, 12, stroke=INK, fill=IVORY, sw=1.6)
    # Tray of blank cards.
    d.rect(230, 200, 140, 50, stroke=INK, fill=IVORY, sw=PSW)
    for i in range(4):
        d.rect(242 + i * 28, 208, 22, 32, stroke=LINE, fill=PARCHMENT, sw=1.2)
    # Stick of copper type.
    d.poly([(230, 170), (400, 170), (392, 188), (238, 188)], stroke=INK, fill=PARCHMENT, sw=1.5)
    for i in range(8):
        d.rect(246 + i * 18, 158, 12, 14, stroke=COPPER, fill=COPPER, sw=0.7)
    # One finished card standing to dry.
    d.rect(430, 140, 70, 110, stroke=INK, fill=IVORY, sw=PSW)
    d.line(444, 168, 486, 168, stroke=LINE, sw=1.3)
    d.line(444, 186, 470, 186, stroke=LINE, sw=1.3)


PARTS = [
    ("assets/parts/01-opener.svg", part_01,
     "Part opener for The Art of Really Knowing Someone: a library table with two unequal lamps, two book stacks, and blank pages running down the center."),
    ("assets/parts/02-opener.svg", part_02,
     "Part opener for Vulnerability and the Courage to Be Seen: a night window with the shade raised to the sill, a lamp, and an empty chair."),
    ("assets/parts/03-opener.svg", part_03,
     "Part opener for The Science and Experience of Closeness: two cups on a kitchen table, an open pocket watch, and an arc between the cups."),
    ("assets/parts/04-opener.svg", part_04,
     "Part opener for Love, Affection, and Feeling Chosen: two different keys on one hall hook beneath a lit lamp."),
    ("assets/parts/05-opener.svg", part_05,
     "Part opener for Desire, Attraction, and Sensual Intimacy: shoes at a hallway threshold, a half-drawn burgundy drape, and a low lamp."),
    ("assets/parts/06-opener.svg", part_06,
     "Part opener for Playfulness, Laughter, and a Little Mischief: a chessboard with a knight off the board and a paper crown on a pawn."),
    ("assets/parts/07-opener.svg", part_07,
     "Part opener for The Inner World: an orrery of a stair, a seed, a closed eye, and a lamp above a blank journal."),
    ("assets/parts/08-opener.svg", part_08,
     "Part opener for Trust, Communication, and Emotional Safety: a covered porch in the rain, an open door, two mugs, and a lantern."),
    ("assets/parts/09-opener.svg", part_09,
     "Part opener for Shared Adventures and New Experiences: a dusk platform, two tickets, one suitcase, and a half-written destination board."),
    ("assets/parts/10-opener.svg", part_10,
     "Part opener for The Past, the Present, and the Story of Us: a windowsill with a faded photograph, a warm cup, and a blank page."),
    ("assets/parts/11-opener.svg", part_11,
     "Part opener for Radical Curiosity and the Surprising Stuff: a cabinet of unlabeled drawers, one open to reveal a single seashell."),
    ("assets/parts/12-opener.svg", part_12,
     "Part opener for Building a Closer Future Together: two chairs at a dawn window and a pencil path drawn on the glass toward the sun."),
    ("assets/parts/13-opener.svg", part_13,
     "Part opener for The Inventor\u2019s Workshop: a workbench with a screw press, blank cards, copper type, and one card drying."),
]


# --- signature heroes -----------------------------------------------------

def hero_s01(d: Draw):
    d.rect(0, 0, 540, 360, fill=MIDNIGHT, stroke="none", sw=0)
    # Long table, near end wide, far end deep.
    d.poly([(70, 300), (470, 300), (330, 70), (210, 70)], stroke=PARCHMENT, fill=CHARCOAL, sw=PSW)
    d.line(270, 300, 270, 78, stroke=PARCHMENT, sw=1.2)
    # Lamps lower and smaller toward the far end.
    lamp(d, 180, 280, s=0.85, sw=1.7, stem=48, stroke=IVORY)
    lamp(d, 250, 200, s=0.62, sw=1.5, stem=36, stroke=IVORY)
    lamp(d, 290, 130, s=0.42, sw=1.3, stem=24, stroke=IVORY)
    # Place cards: near ones plain, farther ones more particular, far one face down.
    card(d, 120, 250, w=46, h=28, sw=1.3, face="blank")
    for yy in (257, 265, 273):
        d.line(128, yy, 156, yy, stroke=INK, sw=1.15)
    card(d, 360, 246, w=44, h=26, sw=1.3, face="blank")
    for yy in (252, 259, 266):
        d.line(368, yy, 394, yy, stroke=INK, sw=1.15)
    card(d, 200, 180, w=40, h=24, sw=1.2, face="blank")
    key(d, 214, 186, s=0.28, rot=-20, sw=1.2)
    card(d, 300, 150, w=36, h=22, sw=1.2, face="blank")
    cup(d, 318, 146, s=0.22, sw=1.1)
    card(d, 246, 86, w=34, h=22, sw=1.2, face="back")
    # Two chairs at the near end, turned slightly toward each other.
    d.group("translate(150 330) rotate(-12)")
    chair(d, 0, 0, s=0.7, face=1, sw=1.6, stroke=IVORY, accent=COPPER)
    d.end()
    d.group("translate(390 330) rotate(12)")
    chair(d, 0, 0, s=0.7, face=-1, sw=1.6, stroke=IVORY, accent=COPPER)
    d.end()


def hero_s02(d: Draw):
    d.rect(0, 0, 540, 360, fill=MIDNIGHT, stroke="none", sw=0)
    d.rect(0, 188, 540, 172, fill=PARCHMENT, stroke="none", sw=0)
    d.rect(300, 24, 200, 140, stroke=IVORY, fill=MIDNIGHT, sw=PSW)  # black window
    d.line(400, 24, 400, 164, stroke=CHARCOAL, sw=1.4)
    # Parchment pool of the one lamp, flat, not a gradient.
    d.ell(160, 250, 150, 46, stroke="none", fill=PARCHMENT, sw=0)
    lamp(d, 120, 230, s=1.05, sw=PSW, stem=70)
    # Record waiting on the player.
    d.rect(200, 200, 110, 16, stroke=INK, fill=CHARCOAL, sw=PSW)
    d.rect(214, 188, 82, 12, stroke=INK, fill=CHARCOAL, sw=1.4)
    record(d, 255, 184, r=22, sw=1.4)
    # Chair and burgundy throw.
    armchair(d, 400, 300, s=1.15, face=-1, sw=PSW)
    cloth(d, 400, 230, s=1.4, sw=1.6, fill=BURGUNDY)
    # Low table, two glasses, one gold rim.
    d.rect(180, 270, 160, 12, stroke=INK, fill=PARCHMENT, sw=PSW)
    glass(d, 220, 268, s=1.0, sw=1.5, rim=GOLD)
    glass(d, 290, 268, s=1.05, sw=1.5)


def hero_s03(d: Draw):
    d.rect(0, 0, 540, 360, fill=PARCHMENT, stroke="none", sw=0)
    d.rect(330, 24, 180, 120, stroke=INK, fill=TEAL, sw=PSW)
    d.line(420, 24, 420, 144, stroke=CHARCOAL, sw=1.3)
    armchair(d, 40, 300, s=1.2, face=1, sw=PSW)
    armchair(d, 180, 310, s=1.15, face=-1, sw=PSW)
    coat(d, 250, 175, s=0.7, hem=60, sw=1.5)
    # Teapot between the chairs: round copper body, lid, spout, handle, foot.
    d.ell(148, 246, 36, 7, stroke=INK, fill=PARCHMENT, sw=PSW)
    d.path(
        "M110 240 C102 208 116 180 148 174 C180 180 194 208 186 240 Z",
        stroke=INK, fill=COPPER, sw=PSW,
    )
    d.ell(148, 172, 20, 6, stroke=INK, fill=IVORY, sw=PSW)
    d.circ(148, 160, 5, stroke=INK, fill=GOLD, sw=1.6)
    d.path("M182 202 C204 194 212 176 206 162", stroke=INK, sw=PSW)
    d.path("M184 216 C200 210 208 194 202 178", stroke=INK, sw=PSW)
    d.path("M206 162 Q214 170 202 178", stroke=INK, fill=IVORY, sw=PSW)
    d.path("M114 198 C86 192 84 232 116 236", stroke=INK, sw=PSW)
    # Charcoal calendar, Tuesday parchment and blank.
    d.rect(360, 180, 150, 110, stroke=INK, fill=CHARCOAL, sw=PSW)
    draw_word(d, "TUE", 392, 206, 18, stroke=IVORY, sw=1.6)
    for c in range(4):
        for r in range(2):
            x = 372 + c * 34
            y = 210 + r * 34
            if c == 1 and r == 0:
                d.rect(x, y, 28, 28, stroke=PARCHMENT, fill=PARCHMENT, sw=1.2)
            else:
                d.rect(x, y, 28, 28, stroke=CHARCOAL, fill=MIDNIGHT, sw=1.0)
                d.line(x + 6, y + 20, x + 20, y + 8, stroke=LINE, sw=1.0)
    # Single receipt on the table.
    d.rect(70, 270, 36, 48, stroke=INK, fill=IVORY, sw=1.4)
    for yy in (282, 292, 302):
        d.line(76, yy, 98, yy, stroke=LINE, sw=1.1)


def hero_s04(d: Draw):
    d.rect(0, 0, 540, 360, fill=MIDNIGHT, stroke="none", sw=0)
    # Empty hall floor, room to turn around.
    d.poly([(40, 360), (500, 360), (420, 180), (120, 180)], stroke=PARCHMENT, fill=CHARCOAL, sw=PSW)
    # Lit kitchen, copper.
    d.rect(24, 30, 160, 160, stroke=IVORY, fill=PARCHMENT, sw=PSW)
    d.rect(40, 130, 80, 16, stroke=INK, fill=COPPER, sw=1.4)
    d.circ(80, 120, 14, stroke=INK, fill=IVORY, sw=1.4)
    d.path("M150 50 Q170 80 150 120", stroke=COPPER, sw=1.5)
    # Dark walk with a coat.
    d.rect(190, 20, 150, 170, stroke=IVORY, fill=MIDNIGHT, sw=PSW)
    d.path("M230 40 Q280 50 270 140", stroke=TEAL, sw=1.4)
    hook(d, 250, 50, s=0.7, sw=1.4)
    coat(d, 246, 62, s=0.65, hem=70, sw=1.4, fill="none", stroke=IVORY)
    # Quiet chair under a small lamp.
    d.rect(360, 40, 160, 150, stroke=IVORY, fill=CHARCOAL, sw=PSW)
    chair(d, 420, 170, s=0.75, face=1, sw=1.5, stroke=IVORY, accent=GOLD)
    lamp(d, 470, 160, s=0.45, sw=1.4, stem=30)


def hero_s05(d: Draw):
    d.rect(0, 0, 540, 360, fill=PARCHMENT, stroke="none", sw=0)
    d.rect(360, 20, 150, 90, stroke=INK, fill=MIDNIGHT, sw=PSW)
    d.rect(40, 200, 460, 16, stroke=INK, fill=PARCHMENT, sw=PSW)
    d.line(70, 216, 60, 300, stroke=INK, sw=PSW)
    d.line(470, 216, 480, 300, stroke=INK, sw=PSW)
    # Sealed capsule: a small casket with a copper clasp. Date is scratches plus a gold line.
    d.rect(70, 140, 150, 60, rx=4, stroke=INK, fill=IVORY, sw=PSW)
    d.line(70, 162, 220, 162, stroke=COPPER, sw=1.6)
    d.rect(132, 150, 22, 16, stroke=COPPER, fill=COPPER, sw=0.8)
    d.line(90, 128, 120, 128, stroke=GOLD, sw=1.5)
    for i, xx in enumerate((96, 108, 122, 136)):
        d.line(xx, 112, xx + 4, 122, stroke=INK, sw=1.3)
    frame_rect(d, 250, 120, 70, 54, sw=1.5)
    d.path("M262 158 L278 136 L292 150 L308 132", stroke=LINE, sw=1.3)
    envelope(d, 340, 130, w=70, h=48, sw=1.4, flap="closed", seal=False)
    d.line(350, 150, 390, 150, stroke=LINE, sw=1.2)
    key(d, 450, 160, s=0.9, rot=-15, sw=1.6)


def hero_s06(d: Draw):
    d.rect(0, 0, 540, 200, fill=MIDNIGHT, stroke="none", sw=0)
    d.rect(0, 200, 540, 160, fill=PARCHMENT, stroke="none", sw=0)
    d.rect(24, 28, 200, 120, stroke=IVORY, fill=MIDNIGHT, sw=PSW)
    d.line(24, 200, 516, 200, stroke=INK, sw=PSW)  # sideboard
    # Unmatched glasses in a row. One burgundy. A few gold rims. One raised.
    specs = [
        (50, 200, 1.0, "none", INK, False),
        (100, 200, 1.35, "none", GOLD, False),
        (160, 200, 0.8, BURGUNDY, INK, False),
        (210, 168, 1.15, "none", GOLD, True),  # raised
        (270, 200, 1.5, "none", INK, False),
        (330, 200, 0.7, "none", INK, False),
        (380, 200, 1.2, "none", INK, False),
        (440, 200, 0.95, "none", GOLD, False),
    ]
    for x, y, s, fill, rim, _raised in specs:
        glass(d, x, y, s=s, sw=1.6, fill=fill, rim=rim)
    # Blank card at the far end.
    card(d, 470, 150, w=48, h=64, sw=1.5, face="blank")


HEROES = [
    ("assets/signatures/S01-hero.svg", hero_s01,
     "Hero for The Long Table: a long table receding into a dark room, lowering lamps, deepening place cards, and one card left face down."),
    ("assets/signatures/S02-hero.svg", hero_s02,
     "Hero for The Night With the Lights Low: a dim sitting room, one lamp, a waiting record, a burgundy throw, and a dark window."),
    ("assets/signatures/S03-hero.svg", hero_s03,
     "Hero for The Case of the Missing Tuesday: a parlor, two armchairs, a teapot, and a calendar with Tuesday left blank."),
    ("assets/signatures/S04-hero.svg", hero_s04,
     "Hero for The Branching Evening: a night hall opening onto a kitchen, a dark walk, and a quiet chair, with room to turn around."),
    ("assets/signatures/S05-hero.svg", hero_s05,
     "Hero for The Capsule We Open Later: a sealed capsule on a table, dated, with a photograph, a letter, and a key beside it."),
    ("assets/signatures/S06-hero.svg", hero_s06,
     "Hero for The Long Toast: a row of unmatched glasses like years, one glass raised, a night window, and a blank card at the far end."),
]


# --- covers, textures, icons ----------------------------------------------

def emblem(d: Draw, cx, cy, s=1.0, sw=1.6, on_dark=True):
    ring = IVORY if on_dark else INK
    d.circ(cx - 18 * s, cy, 32 * s, stroke=ring, sw=sw, fill="none")
    d.circ(cx + 18 * s, cy, 32 * s, stroke=ring, sw=sw, fill="none")
    key(d, cx - 10 * s, cy + 4 * s, s=0.85 * s, rot=-20, sw=sw, stroke=COPPER)
    for px, py, r in ((-52, -28, 5), (48, -24, 4), (40, 30, 3.5), (-46, 26, 3), (0, -40, 4)):
        star(d, cx + px * s, cy + py * s, r * s, sw=max(0.8, sw * 0.6))


def cover_front(d: Draw):
    d.rect(0, 0, 522, 738, fill=MIDNIGHT, stroke="none", sw=0)
    d.rect(48.6, 48.6, 424.8, 640.8, stroke=COPPER, fill="none", sw=0.5)
    d.rect(54.6, 54.6, 412.8, 628.8, stroke=COPPER, fill="none", sw=0.5)
    emblem(d, 261, 168, s=1.35, sw=1.8, on_dark=True)
    d.raw(
        '<text x="261" y="360" text-anchor="middle" fill="#FBF8F2" '
        'font-family="Palatino Linotype, Palatino, \'Book Antiqua\', serif" '
        'font-size="40" font-weight="700">The Closer Project</text>'
    )
    d.raw(
        '<text x="261" y="392" text-anchor="middle" fill="#F6F1E7" '
        'font-family="Palatino Linotype, Palatino, \'Book Antiqua\', serif" '
        'font-size="13" font-style="italic">A library of closeness, play, and the story of us</text>'
    )


def cover_back(d: Draw):
    d.rect(0, 0, 522, 738, fill=MIDNIGHT, stroke="none", sw=0)
    d.rect(48.6, 48.6, 424.8, 640.8, stroke=COPPER, fill="none", sw=0.5)
    d.rect(54.6, 54.6, 412.8, 628.8, stroke=COPPER, fill="none", sw=0.5)
    emblem(d, 261, 92, s=0.55, sw=1.3, on_dark=True)
    lines = [
        "A library of experiences for two adults",
        "who already like each other. Skip freely.",
        "Write what you want to keep.",
    ]
    y = 150
    for line in lines:
        d.raw(
            f'<text x="72" y="{y}" fill="#FBF8F2" '
            f'font-family="Georgia, \'Times New Roman\', serif" font-size="12">{xml(line)}</text>'
        )
        y += 16
    parts = [
        "01  The Art of Really Knowing Someone",
        "02  Vulnerability and the Courage to Be Seen",
        "03  The Science and Experience of Closeness",
        "04  Love, Affection, and Feeling Chosen",
        "05  Desire, Attraction, and Sensual Intimacy",
        "06  Playfulness, Laughter, and a Little Mischief",
        "07  The Inner World: Dreams, Meaning, and Identity",
        "08  Trust, Communication, and Emotional Safety",
        "09  Shared Adventures and New Experiences",
        "10  The Past, the Present, and the Story of Us",
        "11  Radical Curiosity and the Surprising Stuff",
        "12  Building a Closer Future Together",
        "13  The Inventor\u2019s Workshop: Original Proposals",
    ]
    y = 230
    for line in parts:
        d.raw(
            f'<text x="72" y="{y}" fill="#F6F1E7" '
            f'font-family="Calibri, \'Segoe UI\', sans-serif" font-size="9">{xml(line)}</text>'
        )
        y += 22
    # Empty barcode box. 2.00 by 1.20 in, inside the 0.45 in safe area.
    d.rect(318, 560, 144, 86.4, stroke=PARCHMENT, fill="none", sw=0.75)
    d.raw(
        '<text x="390" y="552" text-anchor="middle" fill="#F6F1E7" '
        'font-family="Calibri, \'Segoe UI\', sans-serif" font-size="9">barcode reserved</text>'
    )


def title_page(d: Draw):
    d.rect(0, 0, 504, 720, fill=PARCHMENT, stroke="none", sw=0)
    emblem(d, 252, 250, s=1.6, sw=1.7, on_dark=False)
    d.raw(
        '<text x="252" y="400" text-anchor="middle" fill="#241F1C" '
        'font-family="Palatino Linotype, Palatino, \'Book Antiqua\', serif" '
        'font-size="32">The Closer Project</text>'
    )
    d.line(212, 418, 292, 418, stroke=COPPER, sw=0.75)
    d.raw(
        '<text x="252" y="442" text-anchor="middle" fill="#2C3544" '
        'font-family="Calibri, \'Segoe UI\', sans-serif" font-size="9">Illustrated workbook edition</text>'
    )


def texture_constellation(d: Draw):
    stars = [
        (30, 36, 5), (92, 70, 4), (150, 28, 6), (210, 64, 4),
        (48, 120, 4), (120, 150, 5), (186, 132, 3.5), (70, 200, 5),
        (160, 196, 4), (214, 176, 5), (24, 214, 3), (200, 220, 3.5),
    ]
    links = [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (7, 8), (8, 9), (1, 5), (6, 9)]
    for a, b in links:
        x1, y1, _ = stars[a]
        x2, y2, _ = stars[b]
        d.line(x1, y1, x2, y2, stroke=GOLD, sw=0.8, opacity=0.85)
    for x, y, r in stars:
        star(d, x, y, r, sw=0.7)


def texture_grain(d: Draw):
    d.raw(
        "<defs><filter id=\"grain\" x=\"0\" y=\"0\" width=\"100%\" height=\"100%\">"
        "<feTurbulence type=\"fractalNoise\" baseFrequency=\"0.85\" numOctaves=\"4\" "
        "seed=\"14\" stitchTiles=\"stitch\"/>"
        "<feColorMatrix type=\"matrix\" values=\"0 0 0 0 0.141  0 0 0 0 0.122  "
        "0 0 0 0 0.110  0 0 0 0.06 0\"/>"
        "</filter></defs>"
    )
    d.rect(0, 0, 240, 240, fill=PARCHMENT, stroke="none", sw=0)
    d.rect(0, 0, 240, 240, fill=PARCHMENT, stroke="none", sw=0)
    d.raw('<rect width="240" height="240" filter="url(#grain)"/>')
    d.path("M12 40 C40 36 70 48 100 42", stroke=LINE, sw=0.4, opacity=0.5)
    d.path("M20 180 C80 176 140 188 210 174", stroke=LINE, sw=0.35, opacity=0.4)


def icon_pause(d: Draw):
    d.circ(28, 28, 18, stroke=TEAL, sw=2.4, fill="none")
    d.rect(20, 16, 5, 24, rx=1, stroke=TEAL, fill=TEAL, sw=0.6)
    d.rect(31, 16, 5, 24, rx=1, stroke=TEAL, fill=TEAL, sw=0.6)
    d.raw(
        '<text x="56" y="36" fill="#241F1C" '
        'font-family="Calibri, \'Segoe UI\', sans-serif" font-size="22">Pause</text>'
    )


def icon_pass(d: Draw):
    door(d, 8, 8, w=28, h=40, sw=1.6, ajar=0.35)
    d.raw(
        '<text x="52" y="36" fill="#241F1C" '
        'font-family="Calibri, \'Segoe UI\', sans-serif" font-size="22">Pass</text>'
    )


def icon_key(d: Draw):
    key(d, 22, 40, s=1.15, rot=-40, sw=2.4)


def hexes_in(text: str) -> set[str]:
    return {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}", text)}


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def check_svg(text: str, viewbox: str, label: str):
    if f'viewBox="{viewbox}"' not in text:
        raise SystemExit(f"{label} missing viewBox {viewbox}")
    bad = hexes_in(text) - {h.upper() for h in ALLOWED_HEX}
    if bad:
        raise SystemExit(f"{label} uses colors outside the palette: {sorted(bad)}")
    lowered = text.lower().replace("http://www.w3.org/2000/svg", "")
    for banned in ("<script", "<image", "lineargradient", "radialgradient", "watermark", "http://", "https://"):
        if banned in lowered:
            raise SystemExit(f"{label} contains {banned}")


def main():
    raise SystemExit(
        "Phase 4 stopped this script. It only writes the rejected SVG line art. "
        "Finished plates are painted image files. Do not run this in their place."
    )
    art = json.loads(ART_MAP.read_text(encoding="utf-8"))
    chapters = art["chapters"]
    if [c["id"] for c in chapters] != [f"{i:03d}" for i in range(1, 109)]:
        raise SystemExit("ART_MAP.json is not a clean 001-108 list")
    missing = [c["id"] for c in chapters if c["id"] not in SCENES]
    if missing:
        raise SystemExit(f"No drawing for {missing}")

    rows = []
    bodies = {}
    motif_paths = []
    for ch in chapters:
        d = Draw()
        SCENES[ch["id"]](d)
        body = "\n".join(d.buf)
        bodies[ch["id"]] = body
        label = ch["alt"]
        svg = wrapped("0 0 440 280", 440, 280, label, f'<g data-motif="{xml(ch["motif"])}">\n{body}\n</g>')
        check_svg(svg, "0 0 440 280", ch["id"])
        rel = ch["svg"].replace("\\", "/")
        write(ROOT / rel, svg)
        motif_paths.append(rel)
        rows.append((rel, "motif", 440, 280, LICENSE, "original procedural SVG from the ART_MAP motif sentence", label))

    seen = {}
    for cid, body in bodies.items():
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if digest in seen:
            raise SystemExit(f"Motifs {seen[digest]} and {cid} are identical")
        seen[digest] = cid

    for rel, fn, alt in PARTS:
        d = Draw()
        fn(d)
        d.rect(8, 8, 524, 424, fill="none", stroke=COPPER, sw=1.1)
        svg = wrapped("0 0 540 440", 540, 440, alt, "\n".join(d.buf))
        check_svg(svg, "0 0 540 440", rel)
        write(ROOT / rel, svg)
        rows.append((rel, "part-opener", 540, 440, LICENSE, "original SVG scene from PART_OPENERS.md", alt))

    for rel, fn, alt in HEROES:
        d = Draw()
        fn(d)
        svg = wrapped("0 0 540 360", 540, 360, alt, "\n".join(d.buf))
        check_svg(svg, "0 0 540 360", rel)
        write(ROOT / rel, svg)
        rows.append((rel, "signature", 540, 360, LICENSE, "original SVG scene from SIGNATURE_ART.md", alt))

    plates = [
        ("assets/covers/cover-front.svg", "0 0 522 738", 522, 738, cover_front, "cover",
         "Front cover of The Closer Project on a midnight ground: an emblem of two circles, a key, and gold stars, with the title and subtitle.",
         "original SVG cover from the Night Library design system"),
        ("assets/covers/cover-back.svg", "0 0 522 738", 522, 738, cover_back, "cover",
         "Back cover with a short invitation, the thirteen part names, and an empty box labeled barcode reserved.",
         "original SVG cover from the Night Library design system"),
        ("assets/covers/title-page.svg", "0 0 504 720", 504, 720, title_page, "cover",
         "Title page on parchment with the night-library emblem, the title The Closer Project, and an edition line.",
         "original SVG title page from the Night Library design system"),
        ("assets/styles/texture-constellation.svg", "0 0 240 240", 240, 240, texture_constellation, "texture",
         "Decorative repeating field of gold stars linked by fine lines.",
         "original procedural SVG texture"),
        ("assets/styles/icon-pause.svg", "0 0 180 56", 180, 56, icon_pause, "icon",
         "Pause control: a teal ring and two bars beside the word Pause.",
         "original SVG icon"),
        ("assets/styles/icon-pass.svg", "0 0 160 56", 160, 56, icon_pass, "icon",
         "Pass control: an open door beside the word Pass.",
         "original SVG icon"),
        ("assets/styles/icon-key.svg", "0 0 80 80", 80, 80, icon_key, "icon",
         "A copper key drawn in the Night Library line.",
         "original SVG icon"),
    ]
    for rel, vb, w, h, fn, kind, alt, method in plates:
        d = Draw()
        fn(d)
        svg = wrapped(vb, w, h, alt, "\n".join(d.buf))
        check_svg(svg, vb, rel)
        write(ROOT / rel, svg)
        rows.append((rel, kind, w, h, LICENSE, method, alt))

    grain = Draw()
    texture_grain(grain)
    grain_svg = wrapped("0 0 240 240", 240, 240, "", "\n".join(grain.buf), decorative=True)
    check_svg(grain_svg, "0 0 240 240", "texture-grain")
    write(ROOT / "assets/styles/texture-grain.svg", grain_svg)
    rows.append(("assets/styles/texture-grain.svg", "texture", 240, 240, LICENSE,
                  "original procedural SVG paper grain", ""))

    # Remove superseded filenames if an earlier pass wrote them.
    parts_dir = ROOT / "assets" / "parts"
    sig_dir = ROOT / "assets" / "signatures"
    if parts_dir.exists():
        for old in parts_dir.glob("part-*.svg"):
            old.unlink()
    if sig_dir.exists():
        for old in sig_dir.glob("S0?.svg"):
            old.unlink()

    manifest = ROOT / "assets" / "ASSET_MANIFEST.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "kind", "width", "height", "license", "method", "alt"])
        writer.writerows(rows)

    motif_count = len(list((ROOT / "assets" / "chapters").glob("*/motif.svg")))
    part_count = len(list((ROOT / "assets" / "parts").glob("*-opener.svg")))
    hero_count = len(list((ROOT / "assets" / "signatures").glob("S*-hero.svg")))
    pause = (ROOT / "assets" / "styles" / "icon-pause.svg").read_text(encoding="utf-8")
    if ">Pause<" not in pause:
        raise SystemExit("Pause icon is missing the word Pause")
    print(f"motifs {motif_count}")
    print(f"part-openers {part_count}")
    print(f"signature-heroes {hero_count}")
    print(f"manifest-rows {len(rows)}")
    print(f"unique-motifs {len(seen)}")
    if motif_count != 108 or part_count != 13 or hero_count != 6 or len(rows) != 108 + 13 + 6 + 3 + 2 + 3:
        raise SystemExit("Count mismatch")
    print("PASS")


if __name__ == "__main__":
    main()
