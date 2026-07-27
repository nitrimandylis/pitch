"""Turn the seal avatar into an alpha mask for CSS mask-image.

The drawing separates cleanly by tone: main outlines, whiskers, glasses,
flipper and coffee are pure black, while the knit ribbing, sweater folds
and skin spots are all light grey (180-235). So the ink layer takes only
true black, and everything grey is either flattened to one faint tone or
dropped. No morphology needed.

Usage: python3 make_mask.py   (expects avatar-hi.png beside it)
"""
from PIL import Image
import numpy as np

SRC = "avatar-hi.png"
OUT = "seal-mask.png"

# Ink: fully opaque below INK_FULL, fading out by INK_NONE. Set above the
# grey detail so knit lines and spots never enter the ink layer.
INK_FULL, INK_NONE = 60, 110

# The seal's head fill, flattened to one alpha so the spots vanish into it.
# Measured: head core runs 162-180, while knit ribbing and sweater folds run
# 185-220, so 182 splits them. Anything above stays outline-only.
TONE_LO, TONE_HI, TONE = 140, 182, 0.12


def mask(lum):
    ink = np.clip((INK_NONE - lum) / (INK_NONE - INK_FULL), 0, 1)
    tone = np.where((lum >= TONE_LO) & (lum < TONE_HI), TONE, 0.0)
    return np.maximum(ink, tone)


def main():
    lum = np.asarray(Image.open(SRC).convert("L")).astype(float)
    alpha = mask(lum)

    # Trim the padding around the drawing so the mark fills its box.
    rows, cols = np.where(alpha > 0.05)
    alpha = alpha[rows.min():rows.max() + 1, cols.min():cols.max() + 1]

    h, w = alpha.shape
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., :3] = 255  # colour is irrelevant, mask reads alpha
    out[..., 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(OUT)
    print(f"{OUT} {w}x{h}  ratio {w / h:.3f}")


def demo():
    """Black is solid, grey detail is gone, head grey is faint."""
    probe = np.array([[0.0, 190.0, 171.0, 240.0]])  # ink, knit line, head, sweater
    got = mask(probe)[0]
    assert got[0] == 1.0, "black outlines must be solid"
    assert got[1] == 0.0, "knit/fold/spot grey must drop out"
    assert got[2] == TONE, "head grey must flatten to one faint tone"
    assert got[3] == 0.0, "sweater must be outline-only"
    print("demo ok")


if __name__ == "__main__":
    demo()
    main()
