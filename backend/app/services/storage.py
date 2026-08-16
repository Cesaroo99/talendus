import uuid
from pathlib import Path

from app.config import get_settings
from app.deps import safe_filename
from app.errors import AppError

settings = get_settings()

ALLOWED_EXT = {".pdf": "application/pdf", ".doc": "application/msword", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
MAGIC = {
    b"%PDF": "application/pdf",
    b"PK": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    b"\xd0\xcf\x11\xe0": "application/msword",
}


def detect_mime(data: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise AppError(400, "Formats autorisés : PDF, DOC, DOCX.", "INVALID_FILE_TYPE")
    for magic, mime in MAGIC.items():
        if data.startswith(magic):
            if ext == ".doc" and magic == b"PK":
                raise AppError(400, "Le fichier ne correspond pas à son extension.", "INVALID_FILE_TYPE")
            return mime
    # DOC files vary; trust extension after size check if no magic matched for .doc
    if ext == ".doc":
        return ALLOWED_EXT[ext]
    raise AppError(400, "Impossible de valider le type du fichier.", "INVALID_FILE_TYPE")


def save_resume(data: bytes, filename: str) -> tuple[str, str, str, int]:
    max_bytes = settings.max_resume_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise AppError(400, f"Le CV dépasse {settings.max_resume_mb} Mo.", "FILE_TOO_LARGE")
    if len(data) < 16:
        raise AppError(400, "Fichier vide ou illisible.", "INVALID_FILE")
    mime = detect_mime(data, filename)
    ext = Path(filename).suffix.lower()
    stored = f"{uuid.uuid4().hex}{ext}"
    dest = settings.resume_dir / stored
    dest.write_bytes(data)
    return safe_filename(filename), stored, mime, len(data)


def resume_path(stored_name: str) -> Path:
    path = (settings.resume_dir / Path(stored_name).name).resolve()
    if not str(path).startswith(str(settings.resume_dir.resolve())):
        raise AppError(400, "Chemin de fichier invalide.", "INVALID_PATH")
    return path
