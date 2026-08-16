"""Extraction déterministe de texte et d’indices depuis un CV (sans LLM)."""

from __future__ import annotations

import json
import logging
import re
from io import BytesIO

logger = logging.getLogger("talendus.parse")

_EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
_PHONE = re.compile(r"(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}")
_SKILLS = (
    "chariot", "wms", "mig", "tig", "cnc", "soudure", "soudeur", "cariste",
    "électromécanicien", "electromecanicien", "hydraulique", "pneumatique",
    "lean", "5s", "sst", "cadenassage", "fanuc", "siemens", "plc", "automate",
    "manutention", "préparation", "preparation", "expédition", "expedition",
    "mécanicien", "mecanicien", "usinage", "set-up", "setup",
)


def parse_resume_bytes(data: bytes, mime_type: str, filename: str) -> dict:
    text = ""
    status = "done"
    try:
        if mime_type == "application/pdf" or (filename or "").lower().endswith(".pdf"):
            text = _pdf_text(data)
        elif "wordprocessingml" in (mime_type or "") or (filename or "").lower().endswith(".docx"):
            text = _docx_text(data)
        else:
            status = "unsupported"
    except Exception:
        logger.exception("parse resume failed")
        status = "failed"
        text = ""
    emails = sorted({m.group(0).lower() for m in _EMAIL.finditer(text)})
    phones = sorted({re.sub(r"\s+", " ", m.group(0)).strip() for m in _PHONE.finditer(text)})
    lower = text.lower()
    skills = [skill for skill in _SKILLS if skill in lower]
    excerpt = re.sub(r"\s+", " ", text).strip()[:4000]
    return {
        "status": status,
        "filename": filename,
        "char_count": len(text),
        "emails": emails[:5],
        "phones": phones[:5],
        "skills": skills,
        "excerpt": excerpt,
    }


def parse_json_dump(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _pdf_text(data: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(data))
    parts: list[str] = []
    for page in reader.pages[:12]:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _docx_text(data: bytes) -> str:
    import zipfile

    with zipfile.ZipFile(BytesIO(data)) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
    return re.sub(r"<[^>]+>", " ", xml)
