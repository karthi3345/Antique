import sys
import os
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter

def add_gold_frame(
    input_path: Path,
    output_path: Path,
    border_width: int = 30,
    gold_color: tuple = (212, 175, 55),  # classic gold
    glass_opacity: int = 30,  # 0‑255 for subtle glass effect
    glass_blur_radius: int = 2,
) -> None:
    """Add a gold border and a subtle glass overlay to an image.

    Parameters
    ----------
    input_path: Path
        Source image file.
    output_path: Path
        Destination file for the framed image.
    border_width: int, default 30
        Width of the gold frame in pixels.
    gold_color: tuple, default (212,175,55)
        RGB colour of the gold border.
    glass_opacity: int, default 30
        Opacity of the glass overlay (0‑255). Lower is more subtle.
    glass_blur_radius: int, default 2
        Blur radius applied to the glass overlay.
    """
    # Load original image
    with Image.open(input_path).convert("RGBA") as im:
        # Add gold border
        framed = ImageOps.expand(im, border=border_width, fill=gold_color)

        # Create a semi‑transparent white overlay for the glass effect
        overlay = Image.new("RGBA", im.size, (255, 255, 255, glass_opacity))
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=glass_blur_radius))

        # Paste overlay onto centre of the framed image
        frame_w, frame_h = framed.size
        im_w, im_h = im.size
        top_left = ((frame_w - im_w) // 2, (frame_h - im_h) // 2)
        framed.paste(overlay, top_left, overlay)

        # Ensure output directory exists and save
        os.makedirs(output_path.parent, exist_ok=True)
        framed.convert("RGB").save(output_path, format="JPEG")
        print(f"Saved framed image to {output_path}")

def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python golden_frame.py <input_image> <output_image> [border_width]")
        sys.exit(1)
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    border = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    add_gold_frame(input_file, output_file, border_width=border)

if __name__ == "__main__":
    main()
