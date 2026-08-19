#!/usr/bin/env python3
"""Génère le profil iPhone et les icônes Android de l'appli Talendus."""
from __future__ import annotations

import base64
import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://talendus.ca/m.html"
ICON_SRC = ROOT / "assets" / "img" / "logo" / "apple-touch-icon.png"
OUT_APP = ROOT / "assets" / "app"
ANDROID_RES = ROOT / "mobile" / "android" / "app" / "src" / "main" / "res"


def _png_bytes(path: Path, size: int) -> bytes:
    img = Image.open(path).convert("RGBA")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def write_android_icons() -> None:
    sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    for folder, size in sizes.items():
        dest_dir = ANDROID_RES / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        (dest_dir / "ic_launcher.png").write_bytes(_png_bytes(ICON_SRC, size))


def write_ios_profile() -> Path:
    OUT_APP.mkdir(parents=True, exist_ok=True)
    icon_b64 = base64.b64encode(_png_bytes(ICON_SRC, 180)).decode("ascii")
    profile_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, "ca.talendus.profile")).upper()
    clip_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, "ca.talendus.webclip")).upper()
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>PayloadContent</key>
  <array>
    <dict>
      <key>FullScreen</key>
      <true/>
      <key>Icon</key>
      <data>{icon_b64}</data>
      <key>IsRemovable</key>
      <true/>
      <key>Label</key>
      <string>Talendus</string>
      <key>PayloadDescription</key>
      <string>Ajoute Talendus à l'écran d'accueil</string>
      <key>PayloadDisplayName</key>
      <string>Talendus</string>
      <key>PayloadIdentifier</key>
      <string>ca.talendus.webclip</string>
      <key>PayloadOrganization</key>
      <string>Talendus</string>
      <key>PayloadType</key>
      <string>com.apple.webClip.managed</string>
      <key>PayloadUUID</key>
      <string>{clip_uuid}</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>Precomposed</key>
      <true/>
      <key>URL</key>
      <string>{SITE}</string>
    </dict>
  </array>
  <key>PayloadDescription</key>
  <string>Installe l'icône Talendus sur l'écran d'accueil</string>
  <key>PayloadDisplayName</key>
  <string>Talendus</string>
  <key>PayloadIdentifier</key>
  <string>ca.talendus.profile</string>
  <key>PayloadOrganization</key>
  <string>Talendus</string>
  <key>PayloadRemovalDisallowed</key>
  <false/>
  <key>PayloadType</key>
  <string>Configuration</string>
  <key>PayloadUUID</key>
  <string>{profile_uuid}</string>
  <key>PayloadVersion</key>
  <integer>1</integer>
</dict>
</plist>
"""
    dest = OUT_APP / "talendus.mobileconfig"
    dest.write_text(xml, encoding="utf-8")
    return dest


def main() -> None:
    if not ICON_SRC.exists():
        raise SystemExit(f"Icône introuvable: {ICON_SRC}")
    write_android_icons()
    path = write_ios_profile()
    print(f"Profil iPhone: {path}")
    print("Icônes Android écrites.")


if __name__ == "__main__":
    main()
