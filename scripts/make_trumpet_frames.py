#!/usr/bin/env python3
"""Render the 36-frame turntable sequence for OBJECT No. 013 — the trumpet.

Source: userDocs/image_c53cbcb5.png (3000×3000 studio shot, flat dark-green
background RGB(71,112,76)). The trumpet is keyed out, then each of 36 frames
composites the cutout onto the house cream stage (240,234,218) with a soft
warm contact shadow — the same presentation as every other object of the
collection. Rotation is simulated: apparent width follows |cos| of the angle,
a subtle elliptical squash and lateral shift give turntable perspective, and
a travelling specular sheen keeps consecutive frames distinct.

Idempotent: regenerates all 36 frames whenever any frame is missing.

Usage: python3 scripts/make_trumpet_frames.py [--force]
"""
import math
import os
import sys

from PIL import Image, ImageEnhance, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "userDocs", "image_c53cbcb5.png")
OUT_DIR = os.path.join(BASE, "static", "img", "objects", "013")
FRAMES = 36
OUT_SIZE = 1000

STAGE = (240, 234, 218)      # house cream — matches generate_frames.py
SHADOW = (74, 64, 50, 110)   # warm umber, soft


def load_cutout():
    """Key the trumpet off its flat green studio background."""
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    bg = im.getpixel((4, 4))
    bg_lab = _rgb_to_lab(bg)

    small = im.resize((500, 500), Image.BILINEAR)
    sw, sh = small.size
    mask = Image.new("L", (sw, sh), 0)
    mp = mask.load()
    sp = small.load()
    for y in range(sh):
        for x in range(sw):
            d = _deltae(sp[x, y], bg_lab)
            if d > 26:
                mp[x, y] = 255
            elif d > 14:
                mp[x, y] = int((d - 14) / 12.0 * 255)

    # Clean speckles, close pinholes, soften the edge.
    mask = mask.filter(ImageFilter.MedianFilter(3))
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    mask = mask.resize(im.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(2.0))

    rgba = im.convert("RGBA")
    rgba.putalpha(mask)

    # Tight bbox around the subject.
    bbox = rgba.getbbox()
    if not bbox:
        raise SystemExit("Could not find the trumpet — background key failed.")
    return rgba.crop(bbox)


def _rgb_to_lab(rgb):
    r, g, b = [v / 255.0 for v in rgb]
    def f(c):
        return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92
    r, g, b = f(r), f(g), f(b)
    x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    y = (r * 0.2126 + g * 0.7152 + b * 0.0722)
    z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883
    def g_(t):
        return t ** (1 / 3.0) if t > 0.008856 else (7.787 * t) + 16 / 116.0
    x, y, z = g_(x), g_(y), g_(z)
    return (116 * y - 16, 500 * (x - y), 200 * (y - z))


def _deltae(rgb1, lab2):
    return _lab_d(_rgb_to_lab(rgb1), lab2)


def _lab_d(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def make_frame(cut, angle_deg):
    """One view of the object on the cream stage."""
    theta = math.radians(angle_deg)
    cosv = abs(math.cos(theta))
    width_k = 0.44 + 0.56 * cosv            # 1.0 face-on → 0.44 edge-on
    squash_k = 1.0 - 0.045 * (1.0 - cosv)   # subtle vertical squash
    shift = math.sin(theta) * 0.035          # lateral turntable drift

    w, h = cut.size
    scale = (OUT_SIZE * 0.80) / max(w, h)
    base_w, base_h = int(w * scale), int(h * scale)

    nw = max(2, int(base_w * width_k))
    nh = max(2, int(base_h * squash_k))
    frame = cut.resize((nw, nh), Image.LANCZOS)

    cx = OUT_SIZE / 2 + shift * OUT_SIZE
    ground = OUT_SIZE * 0.905                # where the shadow ellipse sits
    bottom = ground
    x = int(cx - nw / 2)
    y = int(bottom - nh)

    stage = Image.new("RGB", (OUT_SIZE, OUT_SIZE), STAGE)

    # Soft warm contact shadow — widest at face-on, narrower edge-on.
    sw = int(nw * 1.12)
    sh_h = max(10, int(nh * 0.10))
    shadow = Image.new("RGBA", (OUT_SIZE, OUT_SIZE), (0, 0, 0, 0))
    ell = Image.new("RGBA", (sw, sh_h), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(ell).ellipse((0, 0, sw - 1, sh_h - 1), fill=SHADOW)
    ell = ell.filter(ImageFilter.GaussianBlur(14))
    shadow.alpha_composite(ell, (int(cx - sw / 2), int(ground - sh_h / 2)))
    stage = Image.alpha_composite(stage.convert("RGBA"), shadow).convert("RGB")

    stage.paste(frame, (x, y), frame)

    # travelling specular sheen — subtle, keeps frames distinguishable
    stage = _sheen(stage, angle_deg)
    return stage


def _sheen(stage, angle_deg):
    theta = math.radians(angle_deg)
    out = stage.convert("RGBA")
    overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
    px = overlay.load()
    w, h = out.size
    cx = w * (0.5 + 0.30 * math.sin(theta))
    band = max(18, int(w * 0.05))
    step = 2  # coarse pass then blur — fast and still smooth
    for y in range(0, h, step):
        row_offset = (y - h // 2) * 0.18
        for x in range(0, w, step):
            if abs(x + row_offset - cx) < band:
                k = 1.0 - abs(x + row_offset - cx) / band
                for yy in range(y, min(y + step, h)):
                    for xx in range(x, min(x + step, w)):
                        px[xx, yy] = (255, 248, 230, int(26 * k))
    overlay = overlay.filter(ImageFilter.GaussianBlur(3))
    return Image.alpha_composite(out, overlay).convert("RGB")


def render_hero(cut):
    """Dedicated cinematic hero plate — trumpet on deep charcoal, 1920×1080.

    The catalogue frames stay on cream (collection consistency); the hero is
    its own museum-plate composition: object right of centre, warm key light,
    long soft shadow, quiet vignette. Text sits over the left darkness.
    """
    W, H = 1920, 1080
    stage = Image.new("RGB", (W, H), (12, 10, 8))  # house ink

    # Very subtle radial warmth behind the object — not a gradient banner,
    # a studio wall catching a little of the key light.
    glow = Image.new("L", (W, H), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(glow).ellipse(
        (W * 0.62, -H * 0.25, W * 1.45, H * 1.2), fill=26)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    warm = Image.new("RGB", (W, H), (64, 52, 34))
    stage = Image.composite(
        Image.blend(stage, warm, 0.5), stage, glow.point(lambda v: v))

    # Object — tall enough to command, right of centre.
    target_h = int(H * 0.78)
    scale = target_h / cut.size[1]
    obj = cut.resize((max(2, int(cut.size[0] * scale)), target_h), Image.LANCZOS)
    ox = int(W * 0.64)
    oy = int(H * 0.5 - target_h / 2)

    # Long soft shadow to the right, low and warm.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ell_w = int(obj.size[0] * 2.1)
    ell = Image.new("RGBA", (ell_w, 56), (0, 0, 0, 0))
    ImageDraw.Draw(ell).ellipse((0, 0, ell_w - 1, 55), fill=(0, 0, 0, 120))
    ell = ell.filter(ImageFilter.GaussianBlur(22))
    shadow.alpha_composite(ell, (int(ox + obj.size[0] * 0.42), int(oy + target_h * 0.86)))
    stage = Image.alpha_composite(stage.convert("RGBA"), shadow).convert("RGB")

    stage.paste(obj, (ox, oy), obj)

    # Gentle vignette so the plate's edges fall dark and the type stays legible.
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).rectangle((0, 0, W, H), fill=88)
    ImageDraw.Draw(vig).ellipse((-W * 0.25, -H * 0.6, W * 1.25, H * 1.6), fill=0)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), (5, 4, 3))
    stage = Image.composite(Image.blend(stage, dark, 0.72), stage, vig)

    out = os.path.join(BASE, "static", "img", "hero")
    os.makedirs(out, exist_ok=True)
    stage.save(os.path.join(out, "013.webp"), "WEBP", quality=88, method=6)
    print("Hero plate → static/img/hero/013.webp")


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)
    existing = [f for f in os.listdir(OUT_DIR) if f.endswith(".webp")]
    if not force and len(existing) == FRAMES:
        print("013 frames already present (%d) — skipping." % FRAMES)
        return 0

    cut = load_cutout()
    check = os.path.join(OUT_DIR, "_cutout_check.png")
    cut.save(check)
    render_hero(cut)

    for i in range(FRAMES):
        angle = (i / FRAMES) * 360.0
        frame = make_frame(cut, angle)
        frame.save(os.path.join(OUT_DIR, "%02d.webp" % i), "WEBP", quality=88, method=6)
    print("Done — %d frames in %s" % (FRAMES, OUT_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
