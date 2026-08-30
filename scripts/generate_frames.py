#!/usr/bin/env python3
"""
Volgo — placeholder turntable photography.

Generates 36-frame turntable sequences per artifact: a stylised object
silhouette on the house charcoal stage, rotating in 10-degree steps.
WebP output via Pillow. Swap for real photography later — zero code change.

Usage: python3 scripts/generate_frames.py
"""
import math
import os
import sys

sys.path.insert(0, "/workspace")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from collection.models import Artifact  # noqa: E402

STAGE = (240, 234, 218)        # cream #F0EADA — French light theme
IVORY = (242, 237, 227)
BRASS = (154, 138, 92)
BRONZE = (111, 91, 69)
DARK = (14, 13, 11)

W, H = 1000, 1000
FRAMES = 36


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def shade(base, amount):
    """amount in [-1,1]: negative darkens, positive lightens."""
    if amount >= 0:
        return lerp(base, IVORY, amount * 0.5)
    return lerp(base, DARK, -amount * 0.5)


def hexrgb(hx):
    hx = hx.lstrip("#")
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))


def draw_object(draw, kind, base_rgb, angle_deg, cx, cy, scale):
    """Draw a stylised silhouette that visibly rotates with the angle."""
    ang = math.radians(angle_deg)

    def R(px, py, a):
        """Rotate point around origin."""
        c, s = math.cos(a), math.sin(a)
        return (px * c - py * s, px * s + py * c)

    def T(p):
        return (cx + p[0] * scale, cy + p[1] * scale)

    def E(p0, p1):
        return [(min(p0[0], p1[0]), min(p0[1], p1[1])), (max(p0[0], p1[0]), max(p0[1], p1[1]))]

    if kind == "sculpture":
        # Head-like form: cranium + neck + plinth
        draw.ellipse(E(T(R(-90, -240, ang)), T(R(90, -60, ang))), fill=shade(base_rgb, 0.10))
        draw.polygon([T(R(-34, -60, ang)), T(R(34, -60, ang)), T(R(44, 40, ang)), T(R(-44, 40, ang))], fill=shade(base_rgb, -0.12))
        draw.polygon([T(R(-90, 40, ang)), T(R(90, 40, ang)), T(R(80, 80, ang)), T(R(-80, 80, ang))], fill=shade(base_rgb, -0.28))
        # Face landmark that tracks rotation
        fx, fy = R(30, -170, ang)
        draw.ellipse(E(T((fx - 16, fy - 16)), T((fx + 16, fy + 16))), fill=shade(base_rgb, -0.35))
    elif kind == "vessel":
        # Amphora-ish body: ellipse waist + neck + foot
        draw.polygon([T(R(-40, -300, ang)), T(R(40, -300, ang)), T(R(46, -120, ang)), T(R(-46, -120, ang))], fill=shade(base_rgb, -0.10))
        draw.ellipse(E(T(R(-160, -170, ang)), T(R(160, 90, ang))), fill=shade(base_rgb, 0.08))
        draw.polygon([T(R(-60, 60, ang)), T(R(60, 60, ang)), T(R(80, 150, ang)), T(R(-80, 150, ang))], fill=shade(base_rgb, -0.15))
        draw.polygon([T(R(-110, 150, ang)), T(R(110, 150, ang)), T(R(100, 185, ang)), T(R(-100, 185, ang))], fill=shade(base_rgb, -0.3))
        # Rotating highlight band
        hx1, hy1 = R(-100, -40, ang)
        draw.ellipse(E(T((hx1 - 20, hy1 - 40)), T((hx1 + 20, hy1 + 40))), fill=shade(base_rgb, 0.22))
    elif kind == "desk":
        # Writing desk: top + body + legs, rotating footprint
        draw.polygon([T(R(-260, -170, ang)), T(R(260, -170, ang)), T(R(260, -120, ang)), T(R(-260, -120, ang))], fill=shade(base_rgb, 0.05))
        draw.polygon([T(R(-240, -120, ang)), T(R(240, -120, ang)), T(R(240, 120, ang)), T(R(-240, 120, ang))], fill=shade(base_rgb, -0.10))
        for lx in (-200, 200):
            draw.polygon([T(R(lx - 14, 120, ang)), T(R(lx + 14, 120, ang)), T(R(lx + 20, 210, ang)), T(R(lx - 20, 210, ang))], fill=shade(base_rgb, -0.3))
        # Drawer pull that tracks rotation
        px, py = R(120, -20, ang)
        draw.ellipse(E(T((px - 12, py - 12)), T((px + 12, py + 12))), fill=shade(BRASS, 0.0))
    else:  # panel / generic slab
        draw.polygon([T(R(-200, -260, ang)), T(R(200, -260, ang)), T(R(200, 260, ang)), T(R(-200, 260, ang))], fill=shade(base_rgb, 0.02))
        px, py = R(0, 0, ang)
        draw.ellipse(E(T((px - 30, py - 30)), T((px + 30, py + 30))), fill=shade(base_rgb, -0.25))


def render_frame(kind, base_rgb, angle_deg, out_path):
    from PIL import Image, ImageDraw, ImageFilter

    img = Image.new("RGB", (W, H), STAGE)
    draw = ImageDraw.Draw(img)

    # Floor shadow — soft ellipse beneath
    shadow = Image.new("RGB", (W, H), STAGE)
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([W * 0.30, H * 0.80, W * 0.70, H * 0.88], fill=(20, 19, 17))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    img = Image.composite(shadow, img, shadow.convert("L"))

    draw = ImageDraw.Draw(img)
    draw_object(draw, kind, base_rgb, angle_deg, W / 2, H * 0.52, 1.0)

    # Museum-key light: gentle top-left bias via overlay gradient
    overlay = Image.new("L", (W, H), 0)
    od = ImageDraw.Draw(overlay)
    for i in range(60):
        a = int(28 * (1 - i / 60))
        od.line([(0, i * 4), (W, i * 4)], fill=a)
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(dark, img, overlay.point(lambda v: v))

    img.save(out_path, "WEBP", quality=82, method=4)


def main():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("Pillow missing — installing")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "--break-system-packages", "Pillow"])
        print("Pillow installed")

    base = "/workspace/static/img/objects"
    os.makedirs(base, exist_ok=True)

    for artifact in Artifact.objects.all():
        kind = guess_kind(artifact)
        base_rgb = hexrgb(artifact.accent_hex or "#6F5B45")
        folder = os.path.join(base, f"{artifact.object_number:03d}")
        os.makedirs(folder, exist_ok=True)
        for i in range(FRAMES):
            angle = i * (360 / FRAMES)
            out = os.path.join(folder, f"{i:02d}.webp")
            if not os.path.exists(out):
                render_frame(kind, base_rgb, angle, out)
        print(f"OBJECT No. {artifact.object_number:03d} — {FRAMES} frames ({kind})")


def guess_kind(a):
    c = (a.category or "").lower()
    if "sculpture" in c or "figure" in c:
        return "sculpture"
    if "ceramic" in c or "vessel" in c or "glass" in c:
        return "vessel"
    if "furniture" in c:
        return "desk"
    return "panel"


if __name__ == "__main__":
    main()
