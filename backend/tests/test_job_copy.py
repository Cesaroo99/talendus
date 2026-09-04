from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_catalog_stories_cover_every_site_job():
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from job_copy import STORIES, job_story
    from app.site_jobs import SITE_JOBS

    for spec in SITE_JOBS:
        story = job_story(spec["slug"], "fr")
        assert spec["slug"] in STORIES
        assert story.get("role")
        assert story.get("duties")
        assert story.get("profile")
        assert story.get("offer")


def test_public_job_page_is_complete():
    html = (ROOT / "emploi-cariste.html").read_text(encoding="utf-8")
    assert "Ce que vous ferez" in html
    assert "Permis de chariot élévateur" in html
    assert "Comment postuler" in html
    en = (ROOT / "en" / "job-cariste.html").read_text(encoding="utf-8")
    assert "What you will do" in en
    assert "Forklift" in en or "forklift" in en
