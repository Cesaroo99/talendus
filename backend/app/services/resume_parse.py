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
    parsed = {
        "status": status,
        "filename": filename,
        "char_count": len(text),
        "emails": emails[:5],
        "phones": phones[:5],
        "skills": skills,
        "excerpt": excerpt,
    }
    parsed["summary"] = build_cv_summary(parsed)
    return parsed


def parsed_from_storage(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            data = json.loads(raw)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}


def build_cv_summary(parsed: dict) -> str:
    status = (parsed or {}).get("status") or ""
    if status == "unsupported":
        return "Format non analysé automatiquement. Ouvrez le fichier pour consulter le CV."
    if status == "failed":
        return "Le CV n’a pas pu être lu automatiquement. Ouvrez le fichier pour le consulter."
    skills = parsed.get("skills") or []
    excerpt = re.sub(r"\s+", " ", str(parsed.get("excerpt") or "")).strip()
    emails = parsed.get("emails") or []
    phones = parsed.get("phones") or []
    bits: list[str] = []
    if skills:
        bits.append("Compétences relevées : " + ", ".join(skills[:8]) + ".")
    contact = []
    if emails:
        contact.append(emails[0])
    if phones:
        contact.append(phones[0])
    if contact:
        bits.append("Coordonnées dans le CV : " + " · ".join(contact) + ".")
    if excerpt:
        snippet = excerpt[:420].rstrip()
        if len(excerpt) > 420:
            snippet = snippet.rsplit(" ", 1)[0] + "…"
        bits.append(snippet)
    if bits:
        return " ".join(bits)
    if int(parsed.get("char_count") or 0) == 0:
        return "Aucun texte extractible. Ouvrez le fichier pour le consulter."
    return "CV enregistré. Ouvrez le fichier pour le consulter."


def summary_from_storage(raw) -> str:
    parsed = parsed_from_storage(raw)
    existing = str(parsed.get("summary") or "").strip()
    if existing:
        return existing
    return build_cv_summary(parsed)


def is_previewable(mime: str | None, filename: str | None = None) -> bool:
    mime = (mime or "").lower()
    name = (filename or "").lower()
    return mime.startswith("application/pdf") or mime.startswith("image/") or name.endswith((".pdf", ".png", ".jpg", ".jpeg", ".webp"))


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
