from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN = (
    "aucun contact",
    "unmediated",
    "n'écrivez pas",
    "n’écrivez pas",
    "jamais vos coordonnées",
    "never receive your",
    "never get your contact",
    "stay on their own side",
    "jamais l'employeur",
    "never the employer",
    "not to the employer",
    "pas chez l'employeur",
    "pas chez les employeurs",
    "ne se contactent jamais",
    "cannot write to them",
    "you do not write to the employer",
)

SKIP_PARTS = (
    "/assets/js/plugins/",
    "/docs/js/",
    "/node_modules/",
    "/.git/",
)

PUBLIC = (
    "index.html",
    "app.html",
    "m.html",
    "candidats.html",
    "entreprises.html",
    "comment-ca-fonctionne.html",
    "emplois.html",
    "a-propos.html",
    "services.html",
    "en/index.html",
    "en/app.html",
    "en/m.html",
    "en/candidates.html",
    "en/employers.html",
    "en/how-it-works.html",
    "en/jobs.html",
    "en/about.html",
    "assets/js/mobile-app.js",
    "assets/js/account.js",
)


def test_site_and_app_invite_contact_instead_of_no_contact():
    haystacks = []
    for rel in PUBLIC:
        text = (ROOT / rel).read_text(encoding="utf-8")
        haystacks.append((rel, text.lower()))
        for needle in FORBIDDEN:
            assert needle.lower() not in text.lower(), f"{rel} still has {needle!r}"
    joined = "\n".join(text for _, text in haystacks)
    assert "un conseiller vous suit" in joined or "déposez votre cv, on vous rappelle" in joined
    assert "confiez-nous un besoin" in joined
    assert "a consultant follows you" in joined
    assert "hand us a hiring need" in joined


def test_generated_pages_drop_no_contact_copy():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".js", ".py", ".md"}:
            continue
        rel = "/" + str(path.relative_to(ROOT)).replace("\\", "/")
        if any(part in rel for part in SKIP_PARTS):
            continue
        if path.name == "test_copy.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for needle in FORBIDDEN:
            assert needle.lower() not in text, f"{rel} still has {needle!r}"
