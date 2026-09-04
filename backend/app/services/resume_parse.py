"""Extraction déterministe de texte et d’indices depuis un CV (sans LLM)."""

from __future__ import annotations

import html
import json
import logging
import re
from io import BytesIO

logger = logging.getLogger("talendus.parse")

_EMAIL = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
_PHONE = re.compile(r"(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}")
_URL = re.compile(r"https?://\S+|www\.\S+", re.I)
_YEARS = re.compile(
    r"(\d{1,2})\s*(?:ans?|années?|years?)\b|(?:plus de|environ|près de)\s+(\d{1,2})\s*(?:ans?|années?)",
    re.I,
)
_YEARS_WORD = {
    "un": 1,
    "une": 1,
    "deux": 2,
    "trois": 3,
    "quatre": 4,
    "cinq": 5,
    "six": 6,
    "sept": 7,
    "huit": 8,
    "neuf": 9,
    "dix": 10,
    "quinze": 15,
    "vingt": 20,
}
_WORD_YEARS = re.compile(
    r"\b(" + "|".join(_YEARS_WORD) + r")\s+(?:ans?|années?)\b",
    re.I,
)

_SKILL_LABELS = (
    ("électromécanicien", "électromécanique"),
    ("electromecanicien", "électromécanique"),
    ("mécanicien industriel", "mécanique industrielle"),
    ("mecanicien industriel", "mécanique industrielle"),
    ("chariot élévateur", "chariot élévateur"),
    ("chariot elevateur", "chariot élévateur"),
    ("préparation de commandes", "préparation de commandes"),
    ("preparation de commandes", "préparation de commandes"),
    ("cadenassage", "cadenassage"),
    ("hydraulique", "hydraulique"),
    ("pneumatique", "pneumatique"),
    ("manutention", "manutention"),
    ("expédition", "expédition"),
    ("expedition", "expédition"),
    ("soudeur", "soudure"),
    ("soudure", "soudure"),
    ("cariste", "chariot élévateur"),
    ("chariot", "chariot élévateur"),
    ("usinage", "usinage"),
    ("automate", "automates"),
    ("fanuc", "Fanuc"),
    ("siemens", "Siemens"),
    ("setup", "set-up CNC"),
    ("set-up", "set-up CNC"),
    ("cnc", "CNC"),
    ("wms", "WMS"),
    ("mig", "MIG"),
    ("tig", "TIG"),
    ("plc", "PLC"),
    ("lean", "Lean"),
    ("5s", "5S"),
    ("sst", "SST"),
)

_TITLES = (
    ("électromécanicien", "électromécanicien"),
    ("electromecanicien", "électromécanicien"),
    ("mécanicien industriel", "mécanicien industriel"),
    ("mecanicien industriel", "mécanicien industriel"),
    ("machiniste cnc", "machiniste CNC"),
    ("machiniste", "machiniste"),
    ("superviseur de production", "superviseur de production"),
    ("soudeur-monteur", "soudeur-monteur"),
    ("soudeur", "soudeur"),
    ("coordonnateur logistique", "coordonnateur logistique"),
    ("opérateur de production", "opérateur de production"),
    ("operateur de production", "opérateur de production"),
    ("journalier", "journalier d’usine"),
    ("cariste", "cariste"),
    ("chauffeur", "chauffeur"),
    ("manutentionnaire", "manutentionnaire"),
    ("préposé", "préposé d’entrepôt"),
    ("prepose", "préposé d’entrepôt"),
)

_CITIES = (
    "montréal",
    "montreal",
    "laval",
    "longueuil",
    "québec",
    "quebec",
    "gatineau",
    "sherbrooke",
    "trois-rivières",
    "trois-rivieres",
    "saguenay",
    "lévis",
    "levis",
    "terrebonne",
    "saint-jérôme",
    "saint-jerome",
    "brossard",
    "repentigny",
    "boucherville",
    "drummondville",
    "granby",
    "saint-hyacinthe",
    "shawinigan",
    "joliette",
    "victoriaville",
    "rimouski",
    "rouyn-noranda",
    "anjou",
    "blainville",
    "boisbriand",
    "châteauguay",
    "chateauguay",
    "saint-jean-sur-richelieu",
)

_NOISE = re.compile(
    r"^(curriculum\s*vitae|curriculum|resume|résumé|cv|coordonn[ée]es|profil|profile|page\s+\d+|confidentiel)\b",
    re.I,
)
_PERSON_NAME = re.compile(
    r"^([A-ZÉÈÊÀÂÎÏÙÔÜ][a-zàâäéèêëïîôùûüç'’-]+(?:\s+[A-ZÉÈÊÀÂÎÏÙÔÜ][a-zàâäéèêëïîôùûüç'’-]+){1,2})\b"
)

_TEXT_EXTS = {".txt", ".rtf", ".md", ".text"}
_PREVIEW_EXTS = (
    ".pdf",
    ".docx",
    ".doc",
    ".txt",
    ".rtf",
    ".md",
    ".text",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
)


def parse_resume_bytes(data: bytes, mime_type: str, filename: str) -> dict:
    text = ""
    paragraphs: list[str] = []
    status = "done"
    try:
        paragraphs = extract_paragraphs(data, mime_type, filename)
        text = "\n".join(paragraphs)
        if not text.strip() and not _is_image(mime_type, filename):
            status = "failed"
    except ValueError:
        status = "unsupported"
        text = ""
        paragraphs = []
    except Exception:
        logger.exception("parse resume failed")
        status = "failed"
        text = ""
        paragraphs = []
    paragraphs = _unique_blocks(paragraphs)
    text = _collapse_repeats("\n".join(paragraphs))
    emails = sorted({m.group(0).lower() for m in _EMAIL.finditer(text)})
    phones = sorted({re.sub(r"\s+", " ", m.group(0)).strip() for m in _PHONE.finditer(text)})
    lower = text.lower()
    skills = []
    seen: set[str] = set()
    for key, label in _SKILL_LABELS:
        if key in lower and label not in seen:
            skills.append(label)
            seen.add(label)
    excerpt = re.sub(r"\s+", " ", text).strip()[:4000]
    parsed = {
        "status": status,
        "filename": filename,
        "char_count": len(text),
        "emails": emails[:5],
        "phones": phones[:5],
        "skills": skills,
        "excerpt": excerpt,
        "paragraphs": paragraphs[:40],
    }
    parsed["summary"] = build_cv_summary(parsed)
    return parsed


def extract_paragraphs(data: bytes, mime_type: str, filename: str) -> list[str]:
    mime = (mime_type or "").lower()
    name = (filename or "").lower()
    if mime == "application/pdf" or name.endswith(".pdf"):
        return _split_blocks(_pdf_text(data))
    if "wordprocessingml" in mime or name.endswith(".docx"):
        return _docx_paragraphs(data)
    if mime in {"text/plain", "text/markdown"} or name.endswith((".txt", ".md", ".text")):
        return _split_blocks(data.decode("utf-8", errors="ignore"))
    if "rtf" in mime or name.endswith(".rtf"):
        return _split_blocks(_rtf_text(data))
    if mime == "application/msword" or name.endswith(".doc"):
        if data[:2] == b"PK":
            return _docx_paragraphs(data)
        return _split_blocks(_doc_text(data))
    if _is_image(mime, name):
        return []
    if _looks_text(data):
        return _unique_blocks(_split_blocks(data.decode("utf-8", errors="ignore")))
    raise ValueError("unsupported")


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


def build_cv_summary(parsed: dict, profile=None) -> str:
    status = (parsed or {}).get("status") or ""
    if status == "unsupported":
        return "Ce fichier n’a pas encore pu être lu. Ouvrez-le dans le dossier pour le consulter."
    if status == "failed":
        return "Le fichier n’a pas livré de texte lisible. Ouvrez-le pour le parcourir."
    excerpt = _collapse_repeats(re.sub(r"\s+", " ", str(parsed.get("excerpt") or "")).strip())
    paragraphs = _unique_blocks(
        [re.sub(r"\s+", " ", p).strip() for p in (parsed.get("paragraphs") or []) if p and str(p).strip()]
    )
    blob = _collapse_repeats(" ".join(paragraphs) or excerpt)
    if not blob and int(parsed.get("char_count") or 0) == 0:
        return "Aucun texte extractible. Ouvrez le fichier pour le consulter."

    name = _detect_name(blob, profile)
    title = _detect_title(blob, profile)
    city = _detect_city(blob, profile)
    years = _detect_years(blob, profile)
    skills = _skill_labels(parsed.get("skills") or [], blob)

    parts: list[str] = []
    who = name or "Ce profil"
    if title and city:
        parts.append(f"{who} vise un {_poste_de(title)} à {city}.")
    elif title:
        parts.append(f"{who} vise un {_poste_de(title)}.")
    elif city:
        parts.append(f"{who} est établi à {city}.")
    elif name:
        parts.append(f"{name} a déposé un CV à l’étude.")
    else:
        parts.append("Profil candidat à qualifier.")
    if years:
        parts.append(f"L’expérience affichée est de {years} ans.")
    if skills:
        parts.append("Les compétences qui ressortent sont " + _join_fr(skills[:5]) + ".")
    extra = _context_sentence(blob, title, city, skills)
    if extra and extra.rstrip(".") not in " ".join(parts):
        parts.append(extra if extra.endswith(".") else extra + ".")
    return " ".join(parts)


def summary_from_storage(raw, profile=None) -> str:
    return build_cv_summary(parsed_from_storage(raw), profile=profile)


def is_previewable(mime: str | None, filename: str | None = None) -> bool:
    mime = (mime or "").lower()
    name = (filename or "").lower()
    if mime.startswith("application/pdf") or mime.startswith("image/") or mime.startswith("text/"):
        return True
    if "word" in mime or "rtf" in mime:
        return True
    return name.endswith(_PREVIEW_EXTS)


def preview_html(data: bytes, mime_type: str, filename: str) -> str:
    try:
        paragraphs = _unique_blocks(extract_paragraphs(data, mime_type, filename))
    except Exception:
        logger.exception("preview extract failed")
        paragraphs = []
    if not paragraphs:
        body = "<p>Aucun texte extractible dans ce fichier. Téléchargez-le pour le consulter dans un autre logiciel.</p>"
    else:
        body = "".join(f"<p>{html.escape(_collapse_repeats(p))}</p>" for p in paragraphs if p.strip())
    title = html.escape(filename or "Document")
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        f"<title>{title}</title>"
        "<style>body{margin:0;padding:28px 32px;font:16px/1.55 'Source Sans 3',system-ui,sans-serif;"
        "color:#122033;background:#fff}p{margin:0 0 12px}</style></head><body>"
        f"{body}</body></html>"
    )


def parse_json_dump(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _is_image(mime: str, filename: str) -> bool:
    return (mime or "").startswith("image/") or (filename or "").lower().endswith((".png", ".jpg", ".jpeg", ".webp"))


def _looks_text(data: bytes) -> bool:
    sample = data[:2048] if data else b""
    if not sample or b"\x00" in sample:
        return False
    try:
        sample.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _split_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    for raw in re.split(r"\n{2,}|\r\n{2,}", text or ""):
        line = re.sub(r"[ \t]+", " ", raw.replace("\r", "\n")).strip()
        line = re.sub(r"\n+", " ", line).strip()
        if line:
            blocks.append(_collapse_repeats(line))
    if blocks:
        return _unique_blocks(blocks)
    compact = _collapse_repeats(re.sub(r"\s+", " ", text or "").strip())
    return [compact] if compact else []


def _unique_blocks(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in items or []:
        line = re.sub(r"\s+", " ", str(raw or "")).strip()
        if not line:
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(line)
    return out


def _collapse_repeats(text: str) -> str:
    compact = re.sub(r"\s+", " ", text or "").strip()
    if not compact:
        return ""
    sentences = [part.strip() for part in re.split(r"(?<=[\.\!\?])\s+", compact) if part.strip()]
    if len(sentences) >= 2 and len(set(s.rstrip(".!?") for s in sentences)) == 1:
        return sentences[0]
    if len(compact) < 48:
        return compact
    for copies in (3, 2, 4):
        size = len(compact) // copies
        if size < 24:
            continue
        chunk = compact[:size].strip()
        if not chunk:
            continue
        rebuilt = " ".join([chunk] * copies)
        if rebuilt == compact or compact.replace(" ", "") == chunk.replace(" ", "") * copies:
            return chunk
    return compact


def _pdf_text(data: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(data))
    parts: list[str] = []
    for page in reader.pages[:12]:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _docx_paragraphs(data: bytes) -> list[str]:
    import zipfile

    with zipfile.ZipFile(BytesIO(data)) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
    paras: list[str] = []
    for part in re.split(r"</w:p>", xml):
        chunk = re.sub(r"<w:tab\b[^>]*/>", " ", part)
        chunk = re.sub(r"</w:tr>", "\n", chunk)
        chunk = re.sub(r"<[^>]+>", "", chunk)
        chunk = html.unescape(chunk)
        chunk = re.sub(r"\s+", " ", chunk).strip()
        if chunk:
            paras.append(chunk)
    return _unique_blocks(paras)


def _rtf_text(data: bytes) -> str:
    raw = data.decode("latin-1", errors="ignore")
    raw = re.sub(r"\\'[0-9a-fA-F]{2}", " ", raw)
    raw = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", raw)
    raw = re.sub(r"[{}]", " ", raw)
    return raw


def _doc_text(data: bytes) -> str:
    text = data.decode("latin-1", errors="ignore")
    pieces = re.findall(r"[\x20-\x7e\x80-\xff]{5,}", text)
    cleaned = []
    for piece in pieces:
        piece = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]+", " ", piece)
        piece = re.sub(r"\s+", " ", piece).strip()
        if len(piece) >= 8 and not re.fullmatch(r"[A-Z0-9 ._-]{5,}", piece):
            cleaned.append(piece)
    return "\n".join(cleaned[:80])


def _norm(value: str | None) -> str:
    return (value or "").strip().lower()


def _person_name(profile) -> str:
    if profile is None:
        return ""
    user = getattr(profile, "user", None)
    first = str(getattr(user, "first_name", "") or "").strip()
    last = str(getattr(user, "last_name", "") or "").strip()
    return (first + " " + last).strip()


def _detect_name(text: str, profile) -> str:
    named = _person_name(profile)
    if named:
        return named
    match = _PERSON_NAME.search((text or "").strip())
    if not match:
        return ""
    value = match.group(1).strip()
    if _NOISE.match(value) or len(value) < 5:
        return ""
    return value


def _poste_de(title: str) -> str:
    label = (title or "").strip()
    if not label:
        return "poste"
    if label[0].lower() in "aeiouéèêàâîïùôü":
        return f"poste d’{label}"
    return f"poste de {label}"


def _join_fr(items: list[str]) -> str:
    values = [item for item in items if item]
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} et {values[1]}"
    return ", ".join(values[:-1]) + " et " + values[-1]


def _detect_title(text: str, profile) -> str:
    if profile is not None and getattr(profile, "title", None):
        title = str(profile.title).strip()
        if title:
            return title[0].lower() + title[1:] if len(title) > 1 else title.lower()
    lower = _norm(text)
    for key, label in _TITLES:
        if key in lower:
            return label
    return ""


def _pretty_city(raw: str) -> str:
    mapping = {
        "montreal": "Montréal",
        "montréal": "Montréal",
        "quebec": "Québec",
        "québec": "Québec",
        "trois-rivieres": "Trois-Rivières",
        "trois-rivières": "Trois-Rivières",
        "saint-jerome": "Saint-Jérôme",
        "saint-jérôme": "Saint-Jérôme",
        "levis": "Lévis",
        "lévis": "Lévis",
        "chateauguay": "Châteauguay",
        "châteauguay": "Châteauguay",
    }
    key = _norm(raw)
    if key in mapping:
        return mapping[key]
    return raw.strip().title() if raw else ""


def _detect_city(text: str, profile) -> str:
    if profile is not None and getattr(profile, "city", None):
        return _pretty_city(str(profile.city))
    lower = _norm(text)
    for city in _CITIES:
        if re.search(r"\b" + re.escape(city) + r"\b", lower):
            return _pretty_city(city)
    return ""


def _detect_years(text: str, profile) -> int | None:
    if profile is not None:
        years = getattr(profile, "years_experience", None)
        if isinstance(years, int) and years > 0:
            return years
    match = _YEARS.search(text or "")
    if match:
        return int(match.group(1) or match.group(2))
    word = _WORD_YEARS.search(text or "")
    if word:
        return _YEARS_WORD.get(word.group(1).lower())
    return None


def _skill_labels(skills: list, text: str) -> list[str]:
    seen: list[str] = []
    bag = set(skills or [])
    lower = _norm(text)
    for key, label in _SKILL_LABELS:
        if label in bag or key in lower:
            if label not in seen:
                seen.append(label)
    return seen


def _context_sentence(text: str, title: str, city: str, skills: list[str]) -> str:
    cleaned = _EMAIL.sub(" ", text or "")
    cleaned = _PHONE.sub(" ", cleaned)
    cleaned = _URL.sub(" ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    chunks = re.split(r"(?<=[\.\!\?])\s+|•|·|\|", cleaned)
    skip = {title.lower(), city.lower(), *(s.lower() for s in skills)}
    skip.update({"profil candidat", "curriculum vitae"})
    known = set()
    for token in (title, city, *skills):
        known.update(re.findall(r"[a-zàâäéèêëïîôùûüç0-9]+", _norm(token)))
    for chunk in chunks:
        line = chunk.strip(" -–—,;:")
        if len(line) < 36 or len(line) > 180:
            continue
        if _NOISE.match(line):
            continue
        low = line.lower()
        if any(token in low for token in ("@", "http", "linkedin", "page ")):
            continue
        if low in skip:
            continue
        if title and low.startswith(title.lower()) and len(line) < 40:
            continue
        words = re.findall(r"[a-zàâäéèêëïîôùûüç0-9]+", low)
        if not words:
            continue
        overlap = sum(1 for word in words if word in known or word in {"ans", "an", "cv", "poste"})
        if overlap >= max(2, int(len(words) * 0.5)):
            continue
        if not re.search(r"\b(a|à|en|pour|depuis|avec|dans|dont|qui|travaille|gère|responsable|expérience)\b", low):
            continue
        return line[0].upper() + line[1:] if line[0].islower() else line
    return ""
