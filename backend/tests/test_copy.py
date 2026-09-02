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


def test_employer_pages_sound_like_a_recruiting_firm():
    page = (ROOT / "entreprises.html").read_text(encoding="utf-8")
    assert "Concrètement" not in page
    assert "Ce que ça donne" not in page
    assert "consultation gratuite" in page.lower()
    assert "chasse" in page.lower()
    assert "première entrevue" in page.lower() or "premiere entrevue" in page.lower()
    assert "Processus de recrutement" in page
    assert "Prise de besoins" in page
    assert "Recrutement actif" in page
    chasse = (ROOT / "chasse-de-tetes.html").read_text(encoding="utf-8")
    assert "consultation gratuite" in chasse.lower()
    assert "Recrutement actif" in chasse
    en = (ROOT / "en" / "employers.html").read_text(encoding="utf-8")
    assert "In practice" not in en
    assert "What that looks like" not in en
    assert "free consultation" in en.lower()
    assert "headhunt" in en.lower()


def test_public_pages_use_source_sans_and_distinct_footer():
    page = (ROOT / "contact.html").read_text(encoding="utf-8")
    assert "Source+Sans+3" in page
    assert "Source+Serif+4" in page
    assert "tl-site-footer" in page
    assert 'role="contentinfo"' in page
    css = (ROOT / "assets/css/talendus.css").read_text(encoding="utf-8")
    assert "--tl-font" in css
    assert "--tl-display" in css
    assert ".tl-site-footer" in css


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
