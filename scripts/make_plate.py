#!/usr/bin/env python3
"""
make_plate.py — Convert the 18th-century palace elevation engraving into a
subtle ivory-on-transparent background plate for VOLGO.

Pipeline:
  1. Load the source engraving (dark ink on aged ivory paper).
  2. Crop away the caption strip (architect credits / scale note) so only the
     architecture remains.
  3. Extract the ink: ink strength = 1 - (paper-normalised luminance), so the
     darkest engraved lines carry the most ink and blank paper carries none.
  4. Multiply ink strength by the paper's own warm ivory colour (per-channel),
     giving warm ivory ink instead of dead-grey ink.
  5. Convert to a transparent RGBA plate: alpha = ink strength (paper fully
     transparent). Colour = warm ivory constant so lines tint uniformly.
  6. Letterbox onto a true 16:9 transparent canvas (2048x1152) with gentle
     symmetric margins so `background-size: cover` never crops the roofline.

Output: static/img/plate-palace.webp  (transparent, ivory linework)
"""
from PIL import Image, ImageOps

SRC = "userDocs/image_db33dd73.png"
OUT = "static/img/plate-palace.webp"

# Plate canvas — true 16:9
CANVAS_W, CANVAS_H = 2048, 1152

# Ivory ink tint (matches --ivory #F2EDE3 family, slightly warmer for glow)
INK_RGB = (244, 238, 222)

src = Image.open(SRC).convert("RGB")
w, h = src.size

# ---------------------------------------------------------------- crop ------
# Crop the bottom caption strip (credits: architect / delin / sculpt, scale).
# From inspection the plate's engraved frame + credits occupy roughly the
# bottom 7% of the source. Keep everything above it.
crop_bottom = int(h * 0.07)
engraving = src.crop((0, 0, w, h - crop_bottom))

# Autocontrast on greyscale luminance to normalise paper tone variation
# (foxing, vignetting) so blank paper reads as uniform white before ink
# extraction. cutoff=2 trims the extremes (stains) toward white.
grey = ImageOps.grayscale(engraving)
grey = ImageOps.autocontrast(grey, cutoff=2)

# ---------------------------------------------------------------- ink -------
# Ink strength per pixel: 0 on blank paper, 1 in the darkest engraved line.
ink = ImageOps.invert(grey)          # dark ink -> bright
ink = ImageOps.autocontrast(ink, cutoff=1)  # stretch ink range
px = ink.load()

ew, eh = ink.size
plate = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
pp = plate.load()
ir, ig, ib = INK_RGB
for y in range(eh):
    for x in range(ew):
        a = px[x, y]
        # Gentle curve: keep only the top 45% of ink strength (paper noise /
        # plate tone fully transparent), then ease the surviving ink so the
        # plate is naturally low-contrast — it will sit at 5-8% page opacity.
        if a < 115:            # below ~45% ink: drop entirely
            continue
        # map 115..255 -> 0..1 then square-ease for a quiet plate
        t = (a - 115) / 140.0
        t = t * t
        pp[x, y] = (ir, ig, ib, int(t * 255))

# ---------------------------------------------------------------- canvas ----
canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
# Letterbox: fit engraving inside canvas with 4% margin, centre it.
margin = 0.04
avail_w = int(CANVAS_W * (1 - 2 * margin))
avail_h = int(CANVAS_H * (1 - 2 * margin))
scale = min(avail_w / plate.width, avail_h / plate.height)
new_w = max(1, int(plate.width * scale))
new_h = max(1, int(plate.height * scale))
fitted = plate.resize((new_w, new_h), Image.LANCZOS)
canvas.paste(fitted, ((CANVAS_W - new_w) // 2, (CANVAS_H - new_h) // 2), fitted)

canvas.save(OUT, "WEBP", lossless=True, method=6)
print(f"wrote {OUT} {canvas.size} src={src.size} crop_bottom={crop_bottom}")
