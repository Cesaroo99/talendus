from datetime import datetime, timedelta, timezone

from conftest import auth_header, register

from app.services.seo import job_posting_schema, robots_txt, tracking_public_config


def _promote(client, email: str, role: str = "ADMIN") -> dict:
    from app.database import SessionLocal
    from app.models import User
    from app.models.enums import UserRole

    data = register(client, email, "EMPLOYER", first_name="Alex", last_name="Editeur")
    db = SessionLocal()
    user = db.get(User, data["user"]["id"])
    user.role = UserRole[role]
    db.commit()
    db.close()
    res = client.post("/api/auth/login", json={"email": email, "password": "Password1!"})
    assert res.status_code == 200
    return res.json()["data"]


def test_robots_txt_blocks_private_paths(client):
    res = client.get("/robots.txt")
    assert res.status_code == 200
    text = res.text
    assert "Sitemap: https://talendus.ca/sitemap.xml" in text
    assert "Disallow: /admin/" in text
    assert "Disallow: /api/" in text
    assert "Disallow: /espace.html" in text
    assert "Disallow: /espace-employeur.html" in text
    assert "Disallow: /projects-left.html" in text
    assert "Disallow: /service-left.html" in text


def test_sitemap_excludes_private_and_includes_public(client):
    res = client.get("/sitemap.xml")
    assert res.status_code == 200
    xml = res.text
    assert "<urlset" in xml
    assert "https://talendus.ca/" in xml
    assert "recrutement-industriel.html" in xml
    assert "recrutement-industriel-montreal.html" in xml
    assert "espace.html" not in xml
    assert "espace-employeur.html" not in xml
    assert "/admin/" not in xml


def test_tracking_config_disabled_by_default(client):
    res = client.get("/api/tracking/config")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["enabled"] is False
    assert data["ga_measurement_id"] == ""
    assert data["meta_pixel_id"] == ""
    assert data["consent_required"] is True
    assert "generate_lead" in data["conversions"]
    assert "submit_application" in data["conversions"]
    assert tracking_public_config()["enabled"] is False


def test_legacy_urls_redirect_301(client):
    res = client.get("/about.html", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == "/a-propos.html"
    res = client.get("/service.html", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == "/services.html"
    res = client.get("/employeurs.html", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == "/entreprises.html"
    res = client.get("/index1.html", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == "/"
    res = client.get("/projects.html", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == "/"
    res = client.get("/team.html", follow_redirects=False)
    assert res.status_code == 301
    assert res.headers["location"] == "/"
    for path, target in (
        ("/projects-left.html", "/"),
        ("/projects-right.html", "/"),
        ("/projects-single.html", "/"),
        ("/service-left.html", "/services.html"),
        ("/service-right.html", "/services.html"),
    ):
        res = client.get(path, follow_redirects=False)
        assert res.status_code == 301, path
        assert res.headers["location"] == target


def test_blog_draft_not_public_then_publish(client):
    tokens = _promote(client, "editor.seo@example.com", "EDITOR")
    headers = auth_header(tokens)
    created = client.post(
        "/api/admin/blog",
        headers=headers,
        json={
            "title": "Salaires en usine au Québec",
            "excerpt": "Repères pour employeurs industriels.",
            "body": "Le salaire affiché doit coller au quart et au métier.",
            "category": "Conseils employeurs",
            "tags": "salaires, industrie",
            "seo_title": "Salaires dans l'industrie au Québec | Talendus",
            "seo_description": "Repères salariaux pour le recrutement industriel au Québec.",
            "status": "DRAFT",
        },
    )
    assert created.status_code == 200, created.text
    post = created.json()["data"]
    assert post["status"] == "DRAFT"
    assert post["slug"]
    public = client.get("/api/blog")
    assert all(item["id"] != post["id"] for item in public.json()["data"])
    missing = client.get("/api/blog/" + post["slug"])
    assert missing.status_code == 404
    published = client.patch(
        "/api/admin/blog/" + post["id"],
        headers=headers,
        json={"status": "PUBLISHED"},
    )
    assert published.status_code == 200
    listed = client.get("/api/blog")
    assert any(item["id"] == post["id"] for item in listed.json()["data"])
    html = client.get("/blog/" + post["slug"])
    assert html.status_code == 200
    assert "Salaires en usine" in html.text
    assert 'application/ld+json' in html.text
    assert '"@type": "Article"' in html.text or '"@type":"Article"' in html.text
    sitemap = client.get("/sitemap.xml").text
    assert "/blog/" + post["slug"] in sitemap


def test_scheduled_blog_not_public_yet(client):
    tokens = _promote(client, "editor.plan@example.com", "EDITOR")
    future = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    created = client.post(
        "/api/admin/blog",
        headers=auth_header(tokens),
        json={
            "title": "Tendances du marché de l'emploi industriel",
            "body": "Article programmé.",
            "status": "SCHEDULED",
            "scheduled_at": future,
        },
    )
    assert created.status_code == 200
    slug = created.json()["data"]["slug"]
    assert client.get("/api/blog/" + slug).status_code == 404


def test_candidate_cannot_manage_blog(client):
    tokens = register(client, "cand.blog@example.com")
    res = client.post(
        "/api/admin/blog",
        headers=auth_header(tokens),
        json={"title": "Interdit", "body": "Non"},
    )
    assert res.status_code == 403


def test_job_posting_schema_hides_client_name():
    class Fake:
        slug = "cariste"
        title = "Cariste"
        description = "Quai de réception"
        published_at = datetime(2026, 7, 20, tzinfo=timezone.utc)
        expires_at = None
        contract_type = "Permanent"
        location = "Laval"
        sector = "Entrepôt"
        company = object()
        salary_min = 22
        salary_max = 26
        salary_display = "22 à 26 $/h"
        currency = "CAD"
        id = "abc"

    payload = job_posting_schema(Fake())
    assert payload["@type"] == "JobPosting"
    assert payload["hiringOrganization"]["name"] == "Talendus"
    assert payload["identifier"]["value"] == "cariste"


def test_robots_helper_mentions_sitemap():
    assert "Sitemap: https://talendus.ca/sitemap.xml" in robots_txt()


def test_gsc_verification_file_404_when_unset(client):
    res = client.get("/googleabc123.html")
    assert res.status_code == 404


def test_gsc_verification_file_when_configured(client, monkeypatch):
    from app.config import get_settings

    monkeypatch.setenv("GOOGLE_SITE_VERIFICATION", "abc123xyz")
    get_settings.cache_clear()
    try:
        res = client.get("/googleabc123xyz.html")
        assert res.status_code == 200, res.text
        assert "google-site-verification: abc123xyz" in res.text
        assert "noindex" in (res.headers.get("x-robots-tag") or "")
        assert client.get("/googleother.html").status_code == 404
    finally:
        monkeypatch.delenv("GOOGLE_SITE_VERIFICATION", raising=False)
        get_settings.cache_clear()
