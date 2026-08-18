import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", data[16:24])


def test_web_manifest_is_installable(client):
    res = client.get("/manifest.webmanifest")
    assert res.status_code == 200, res.text
    assert "manifest" in (res.headers.get("content-type") or "")
    data = json.loads(res.text)
    assert data["name"] == "Talendus"
    assert data["display"] == "standalone"
    assert data["start_url"].startswith("/")
    assert data["scope"] == "/"
    sizes = {icon["sizes"]: icon for icon in data["icons"]}
    assert "192x192" in sizes
    assert "512x512" in sizes
    assert any(icon.get("purpose") == "any" for icon in data["icons"])
    assert any(icon.get("purpose") == "maskable" for icon in data["icons"])
    for icon in data["icons"]:
        src = ROOT / icon["src"].lstrip("/")
        assert src.exists(), icon["src"]
        width, height = _png_size(src)
        declared_w, declared_h = (int(part) for part in icon["sizes"].split("x"))
        assert (width, height) == (declared_w, declared_h)
        assert "tel:" not in json.dumps(data.get("shortcuts") or [])


def test_service_worker_allows_root_scope(client):
    res = client.get("/sw.js")
    assert res.status_code == 200, res.text
    assert "javascript" in (res.headers.get("content-type") or "")
    assert res.headers.get("service-worker-allowed") == "/"
    assert "talendus-app-v2" in res.text
    assert "/offline.html" in res.text


def test_apple_touch_icon_is_square(client):
    icon = ROOT / "assets" / "img" / "logo" / "apple-touch-icon.png"
    assert icon.exists()
    assert _png_size(icon) == (180, 180)
    res = client.get("/favicon.ico")
    assert res.status_code == 200
    assert "image/png" in (res.headers.get("content-type") or "")


def test_app_page_is_a_simple_install_canvas():
    page = (ROOT / "app.html").read_text(encoding="utf-8")
    assert 'id="tl-install-board"' in page
    assert "Trois petits gestes" in page
    assert "Ajouter à l'écran d'accueil" in page
    assert "Sur l'écran d'accueil" in page
    for banned in ("Xcode", "WKWebView", "mobile/android", "APK", "Google Play", "App Store"):
        assert banned not in page
    en = (ROOT / "en" / "app.html").read_text(encoding="utf-8")
    assert 'id="tl-install-board"' in en
    assert "Three small steps" in en
    for banned in ("Xcode", "WKWebView", "mobile/android", "APK"):
        assert banned not in en


def test_dockerfile_ships_pwa_files():
    docker = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "manifest.webmanifest" in docker
    assert " sw.js" in docker or docker.endswith("sw.js") or "sw.js /app/" in docker
    assert (ROOT / "manifest.webmanifest").exists()
    assert (ROOT / "sw.js").exists()
