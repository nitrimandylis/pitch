"""Trace the seal mask into a real vector SVG.

Two layers, both filled with currentColor so the mark inherits page text
colour: a faint flat tone for the head, and the black linework on top.
Contours come from marching squares, then get simplified so the file stays
small. Holes are handled by fill-rule="evenodd" within each layer.

Usage: python3 make_svg.py   (expects avatar-hi.png beside it)
"""
import numpy as np
from PIL import Image
from skimage import measure

from make_mask import mask, TONE

SRC = "avatar-hi.png"
OUT = "seal.svg"

TOLERANCE = 0.7   # polygon simplification, in source pixels
MIN_AREA = 12     # drop specks smaller than this


def layer_paths(binary):
    """Marching-squares contours of a binary mask, simplified, as SVG 'd'.

    The mask is padded first: a region touching the array edge would otherwise
    get closed along the border, filling everything inside it.
    """
    out = []
    padded = np.pad(binary, 1)
    for contour in measure.find_contours(padded.astype(float), 0.5):
        contour = contour - 1  # undo the pad offset
        poly = measure.approximate_polygon(contour, tolerance=TOLERANCE)
        if len(poly) < 3:
            continue
        ys, xs = poly[:, 0], poly[:, 1]
        # Shoelace area, to drop specks that only add file size.
        if abs(np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1))) / 2 < MIN_AREA:
            continue
        d = f"M{xs[0]:.1f},{ys[0]:.1f}" + "".join(
            f"L{x:.1f},{y:.1f}" for x, y in zip(xs[1:], ys[1:])
        )
        out.append(d + "Z")
    return out


def main():
    lum = np.asarray(Image.open(SRC).convert("L")).astype(float)
    alpha = mask(lum)

    rows, cols = np.where(alpha > 0.05)
    top, left = rows.min(), cols.min()
    alpha = alpha[top:rows.max() + 1, left:cols.max() + 1]
    h, w = alpha.shape

    tone = layer_paths(alpha > 0.05)   # whole silhouette, sits underneath
    ink = layer_paths(alpha > 0.5)     # the linework, on top

    svg = (
        # currentColor works because this gets pasted inline into the page.
        # Referencing it externally through mask-image instead would fail over
        # file://, which is how every pitch gets reviewed before it ships.
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" fill="currentColor" role="img" aria-label="seal">'
        f'<path fill-rule="evenodd" opacity="{TONE}" d="{"".join(tone)}"/>'
        f'<path fill-rule="evenodd" d="{"".join(ink)}"/>'
        f"</svg>\n"
    )
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"{OUT} {w}x{h}  {len(tone)}+{len(ink)} contours  {len(svg) / 1024:.1f} KB")


def demo():
    """A filled square traces to one contour; a square with a hole traces to two."""
    solid = np.zeros((40, 40), bool)
    solid[10:30, 10:30] = True
    assert len(layer_paths(solid)) == 1, "solid square is one contour"

    holed = solid.copy()
    holed[16:24, 16:24] = False
    assert len(layer_paths(holed)) == 2, "square with a hole is two contours"
    print("demo ok")


if __name__ == "__main__":
    demo()
    main()
