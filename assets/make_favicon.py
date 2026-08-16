"""Build favicon.svg — the ink tile and paper monogram every pitch shares.

The seal cannot do this job: it is traced line art and turns to mush below
~24px, which is exactly where a favicon lives. So the tab mark is typographic
instead, and the seal stays in the colophon.

Glyph outlines are baked into a path on purpose. A favicon does not get to
load a webfont, so a <text> element would render in whatever the browser felt
like, or not at all.

Usage: python3 make_favicon.py   (writes ../favicon.svg)
"""
import os
import re
import urllib.request

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONT_URL = (
    "https://raw.githubusercontent.com/google/fonts/main/"
    "ofl/fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf"
)
CACHE = os.path.join(os.environ.get("TMPDIR", "/tmp"), "pitch-fraunces.ttf")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "favicon.svg")

LETTERS = "nt"
BOX = 32          # viewBox units
INK = "#22262E"
PAPER = "#F4F5F8"

# Tuned by eye at 16px, which is the size that actually decides this. Heavier
# than the page display weight and tracked apart, or the n and t merge into
# one blob at tab size.
WEIGHT, X_HEIGHT, TRACKING = 900, 0.46, 60


def font():
    if not os.path.exists(CACHE):
        urllib.request.urlretrieve(FONT_URL, CACHE)
    return instancer.instantiateVariableFont(
        TTFont(CACHE), {"wght": WEIGHT, "opsz": 144, "SOFT": 0, "WONK": 0}
    )


def monogram(f, letters=LETTERS):
    """The letters, centred on the tile, as one baked SVG path."""
    glyphs, cmap, metrics = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]

    advance, placed = 0, []
    for ch in letters:
        name = cmap[ord(ch)]
        placed.append((name, advance))
        advance += metrics[name][0] + TRACKING
    advance -= TRACKING

    target = BOX * X_HEIGHT
    scale = target / (f["OS/2"].sxHeight or f["head"].unitsPerEm * 0.5)
    dx = (BOX - advance * scale) / 2
    dy = BOX / 2 + target / 2          # baseline; font units are y-up, SVG y-down

    out = []
    for name, offset in placed:
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(
            TransformPen(pen, Transform(scale, 0, 0, -scale, dx + offset * scale, dy))
        )
        out.append(pen.getCommands())
    return "".join(out)


def svg(d):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BOX} {BOX}">'
        f"<style>"
        f".tile{{fill:{INK}}}.mark{{fill:{PAPER}}}"
        f"@media(prefers-color-scheme:dark){{.tile{{fill:{PAPER}}}.mark{{fill:{INK}}}}}"
        f"</style>"
        f'<rect class="tile" width="{BOX}" height="{BOX}" rx="4"/>'
        f'<path class="mark" d="{d}"/>'
        f"</svg>\n"
    )


def demo():
    """The path must be real baked geometry, and it must sit inside the tile."""
    d = monogram(font())
    assert d.startswith("M") and len(d) > 100, "glyph outlines did not bake"
    # every command in a glyph outline takes coordinate pairs, so x is every other number
    nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", d)]
    xs, ys = nums[0::2], nums[1::2]
    assert 0 <= min(xs) and max(xs) <= BOX, f"mark overflows the tile: {min(xs)}-{max(xs)}"
    assert 0 <= min(ys) and max(ys) <= BOX, f"mark overflows the tile: {min(ys)}-{max(ys)}"
    print("demo ok")


if __name__ == "__main__":
    demo()
    with open(OUT, "w") as fh:
        fh.write(svg(monogram(font())))
    print(f"{os.path.normpath(OUT)}  {os.path.getsize(OUT)} bytes")
