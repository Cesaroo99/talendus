#!/usr/bin/env python3
"""Génère les icônes carrées de l'appli (écran d'accueil)."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "assets" / "img" / "logo"
NAVY = (11, 31, 58, 255)
WHITE = (255, 255, 255, 255)


def draw_mark(img: Image.Image, padding_ratio: float = 0.12) -> None:
    w, h = img.size
    img.paste(NAVY, (0, 0, w, h))
    draw = ImageDraw.Draw(img)
    pad = int(min(w, h) * padding_ratio)
    draw.ellipse([pad, pad, w - pad - 1, h - pad - 1], fill=WHITE)
    scale = (w - 2 * pad) / 36.0

    def p(x: float, y: float) -> tuple[float, float]:
        return (pad + x * scale, pad + y * scale)

    radius = max(2, int(1.75 * scale))
    draw.rounded_rectangle([p(10.75, 11.25), p(25.25, 14.75)], radius=radius, fill=NAVY)
    draw.rounded_rectangle([p(16.25, 14.5), p(19.75, 27.5)], radius=radius, fill=NAVY)


def save(size: int, name: str, padding: float) -> None:
    img = Image.new("RGBA", (size, size), NAVY)
    draw_mark(img, padding)
    path = ROOT / name
    img.save(path, "PNG", optimize=True)


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    save(192, "icon-192.png", 0.12)
    save(512, "icon-512.png", 0.12)
    save(192, "icon-192-maskable.png", 0.22)
    save(512, "icon-512-maskable.png", 0.22)
    save(180, "apple-touch-icon.png", 0.12)
    print("icons written in", ROOT)
