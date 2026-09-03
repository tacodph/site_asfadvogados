#!/usr/bin/env python3
"""Generate favicon files from the ASF logo."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "uploads" / "WhatsApp Image 2026-07-17 at 18.06.26.jpeg"
BG = (22, 20, 15)  # #16140F — site theme color


def square_logo(path: Path, size: int) -> Image.Image:
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    cropped = img.crop((left, top, left + side, top + side))

    # Composite on brand background for consistent tab appearance.
    canvas = Image.new("RGBA", (side, side), BG + (255,))
    canvas.paste(cropped, (0, 0), cropped)
    return canvas.resize((size, size), Image.Resampling.LANCZOS)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Logo not found: {SOURCE}")

    sizes = {
        ROOT / "favicon-32x32.png": 32,
        ROOT / "apple-touch-icon.png": 180,
    }
    for out, px in sizes.items():
        square_logo(SOURCE, px).convert("RGB").save(out, optimize=True)
        print(f"Wrote {out.name} ({px}x{px})")

    ico_sizes = [16, 32, 48]
    images = [square_logo(SOURCE, px) for px in ico_sizes]
    images[0].save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(px, px) for px in ico_sizes],
        append_images=images[1:],
    )
    print("Wrote favicon.ico")


if __name__ == "__main__":
    main()
