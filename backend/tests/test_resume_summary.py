import io
import zipfile

from app.services.resume_parse import build_cv_summary, parse_resume_bytes, preview_html, summary_from_storage


def _mini_docx(text: str) -> bytes:
    body = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>"
        + "".join(f"<w:p><w:r><w:t>{line}</w:t></w:r></w:p>" for line in text.split("\n"))
        + "</w:body></w:document>"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"></Types>',
        )
        zf.writestr("word/document.xml", body)
    return buf.getvalue()


def test_build_cv_summary_is_written_once_without_contacts():
    excerpt = "Karine Tremblay cariste Laval cinq ans WMS chariot elevateur. " * 3
    summary = build_cv_summary(
        {
            "status": "done",
            "skills": ["cariste", "wms"],
            "emails": ["karine@example.com"],
            "phones": ["514-555-0101"],
            "excerpt": excerpt,
            "char_count": len(excerpt),
        }
    )
    assert "Karine Tremblay" in summary
    assert summary.count("Karine Tremblay") == 1
    assert "vise un poste" in summary
    assert "chariot élévateur" in summary
    assert "WMS" in summary
    assert "karine@example.com" not in summary
    assert "514-555-0101" not in summary
    assert excerpt.strip() not in summary


def test_summary_from_storage_recomputes_legacy_parse():
    raw = '{"status":"done","skills":["cnc"],"excerpt":"Machiniste CNC a Saint-Jerome.","emails":[],"phones":[],"char_count":28}'
    summary = summary_from_storage(raw)
    assert "CNC" in summary or "cnc" in summary.lower()
    assert "vise un poste" in summary
    assert "Saint-Jérôme" in summary or "Saint-Jerome" in summary


def test_parse_resume_bytes_includes_summary():
    parsed = parse_resume_bytes(b"%PDF-1.4 unused", "application/pdf", "cv.pdf")
    assert "summary" in parsed
    assert parsed["summary"]


def test_preview_html_reads_docx_once():
    data = _mini_docx("Karine Tremblay\nCariste a Laval\nKarine Tremblay\nCariste a Laval")
    parsed = parse_resume_bytes(
        data,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "cv.docx",
    )
    assert parsed["status"] == "done"
    assert "Karine Tremblay" in parsed["summary"]
    html = preview_html(
        data,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "cv.docx",
    )
    assert "Karine Tremblay" in html
    assert html.count("Karine Tremblay") == 1
    assert html.count("<p>") >= 1


def test_preview_html_reads_plain_text():
    html = preview_html("Disponible jour, Laval, chariot elevateur.".encode("utf-8"), "text/plain", "notes.txt")
    assert "Disponible jour" in html
    assert "<p>" in html
