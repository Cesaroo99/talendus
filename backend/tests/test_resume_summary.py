from app.services.resume_parse import build_cv_summary, parse_resume_bytes, summary_from_storage


def test_build_cv_summary_uses_skills_and_excerpt():
    summary = build_cv_summary(
        {
            "status": "done",
            "skills": ["cariste", "wms"],
            "emails": ["karine@example.com"],
            "phones": ["514-555-0101"],
            "excerpt": "Karine Tremblay cariste Laval cinq ans WMS chariot elevateur.",
            "char_count": 60,
        }
    )
    assert "cariste" in summary
    assert "wms" in summary
    assert "karine@example.com" in summary
    assert "Karine Tremblay" in summary


def test_summary_from_storage_recomputes_legacy_parse():
    raw = '{"status":"done","skills":["cnc"],"excerpt":"Machiniste CNC a Saint-Jerome.","emails":[],"phones":[],"char_count":28}'
    summary = summary_from_storage(raw)
    assert "cnc" in summary
    assert "Machiniste" in summary


def test_parse_resume_bytes_includes_summary():
    parsed = parse_resume_bytes(b"%PDF-1.4 unused", "application/pdf", "cv.pdf")
    assert "summary" in parsed
    assert parsed["summary"]
