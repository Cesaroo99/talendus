import logging
import uuid
from pathlib import Path
from urllib.parse import urlparse

from app.config import get_settings
from app.deps import safe_filename
from app.errors import AppError

logger = logging.getLogger("talendus.storage")

ALLOWED_EXT = {".pdf": "application/pdf", ".doc": "application/msword", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
ALLOWED_IMAGE_EXT = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
MAGIC = {
    b"%PDF": "application/pdf",
    b"PK": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    b"\xd0\xcf\x11\xe0": "application/msword",
}
IMAGE_MAGIC = (
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"RIFF", "image/webp"),
)
CATEGORIES = {"resumes", "documents", "avatars", "logos", "attachments"}


def detect_mime(data: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise AppError(400, "Formats autorisés : PDF, DOC, DOCX.", "INVALID_FILE_TYPE")
    for magic, mime in MAGIC.items():
        if data.startswith(magic):
            if ext == ".doc" and magic == b"PK":
                raise AppError(400, "Le fichier ne correspond pas à son extension.", "INVALID_FILE_TYPE")
            return mime
    if ext == ".doc":
        return ALLOWED_EXT[ext]
    raise AppError(400, "Impossible de valider le type du fichier.", "INVALID_FILE_TYPE")


def detect_image_mime(data: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXT:
        raise AppError(400, "Formats image autorisés : JPG, PNG, WEBP.", "INVALID_FILE_TYPE")
    for magic, mime in IMAGE_MAGIC:
        if data.startswith(magic):
            if mime == "image/webp" and b"WEBP" not in data[:16]:
                raise AppError(400, "Le fichier ne correspond pas à son extension.", "INVALID_FILE_TYPE")
            if mime != ALLOWED_IMAGE_EXT[ext] and not (ext in {".jpg", ".jpeg"} and mime == "image/jpeg"):
                raise AppError(400, "Le fichier ne correspond pas à son extension.", "INVALID_FILE_TYPE")
            return mime
    raise AppError(400, "Impossible de valider le type du fichier.", "INVALID_FILE_TYPE")


def _category_dir(category: str) -> Path:
    if category not in CATEGORIES:
        raise AppError(400, "Catégorie de fichier invalide.", "INVALID_PATH")
    return get_settings().storage_subdir(category)


def save_bytes(
    data: bytes,
    filename: str,
    *,
    category: str,
    kind: str = "document",
    max_mb: int | None = None,
) -> tuple[str, str, str, int, str]:
    settings = get_settings()
    limit = (max_mb or settings.max_resume_mb) * 1024 * 1024
    if len(data) > limit:
        raise AppError(400, f"Le fichier dépasse {max_mb or settings.max_resume_mb} Mo.", "FILE_TOO_LARGE")
    if len(data) < 16:
        raise AppError(400, "Fichier vide ou illisible.", "INVALID_FILE")
    if kind == "image":
        mime = detect_image_mime(data, filename)
    else:
        mime = detect_mime(data, filename)
    ext = Path(filename).suffix.lower()
    stored = f"{uuid.uuid4().hex}{ext}"
    original = safe_filename(filename)
    if _use_s3():
        key = f"{(settings.s3_prefix or 'talendus').strip('/')}/{category}/{stored}"
        _s3_client().put_object(
            Bucket=settings.s3_bucket,
            Key=key,
            Body=data,
            ContentType=mime,
            ContentDisposition=f'attachment; filename="{original}"',
        )
        url = f"s3://{settings.s3_bucket}/{key}"
        logger.info("file uploaded s3 key=%s", key)
        return original, stored, mime, len(data), url
    dest = _category_dir(category) / stored
    dest.write_bytes(data)
    return original, stored, mime, len(data), f"{category}/{stored}"


def file_path(stored_name: str, category: str) -> Path:
    folder = _category_dir(category)
    path = (folder / Path(stored_name).name).resolve()
    if not str(path).startswith(str(folder.resolve())):
        raise AppError(400, "Chemin de fichier invalide.", "INVALID_PATH")
    return path


def open_stored(stored_name: str, storage_url: str | None, category: str = "resumes") -> tuple[str | None, Path | None]:
    settings = get_settings()
    url = storage_url or ""
    if url.startswith("http://") or url.startswith("https://"):
        return url, None
    if url.startswith("s3://") or _use_s3():
        parsed = urlparse(url) if url.startswith("s3://") else None
        bucket = parsed.netloc if parsed else settings.s3_bucket
        prefix = (settings.s3_prefix or "talendus").strip("/")
        key = parsed.path.lstrip("/") if parsed else f"{prefix}/{category}/{Path(stored_name).name}"
        signed = _s3_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=900,
        )
        return signed, None
    return None, file_path(stored_name, category)


def delete_stored(stored_name: str, storage_url: str | None, category: str = "resumes") -> None:
    url = storage_url or ""
    settings = get_settings()
    if url.startswith("s3://") or (_use_s3() and not url.startswith("http")):
        parsed = urlparse(url) if url.startswith("s3://") else None
        bucket = parsed.netloc if parsed else settings.s3_bucket
        prefix = (settings.s3_prefix or "talendus").strip("/")
        key = parsed.path.lstrip("/") if parsed else f"{prefix}/{category}/{Path(stored_name).name}"
        try:
            _s3_client().delete_object(Bucket=bucket, Key=key)
        except Exception:
            logger.warning("s3 delete failed key=%s", key)
        return
    path = file_path(stored_name, category)
    if path.exists():
        path.unlink()


def _use_s3() -> bool:
    settings = get_settings()
    return (settings.storage_backend or "local").lower() == "s3" and bool(settings.s3_bucket)


def _s3_client():
    settings = get_settings()
    try:
        import boto3
    except ImportError as exc:
        raise AppError(503, "Le stockage S3 n'est pas disponible (boto3 manquant).", "STORAGE_UNAVAILABLE") from exc
    kwargs: dict = {}
    if settings.s3_region:
        kwargs["region_name"] = settings.s3_region
    if settings.s3_endpoint_url:
        kwargs["endpoint_url"] = settings.s3_endpoint_url
    if settings.s3_access_key:
        kwargs["aws_access_key_id"] = settings.s3_access_key
        kwargs["aws_secret_access_key"] = settings.s3_secret_key
    return boto3.client("s3", **kwargs)


def save_resume(data: bytes, filename: str) -> tuple[str, str, str, int, str]:
    return save_bytes(data, filename, category="resumes")


def resume_path(stored_name: str) -> Path:
    return file_path(stored_name, "resumes")


def open_resume(stored_name: str, storage_url: str | None) -> tuple[str | None, Path | None]:
    """Retourne (url_presignee, chemin_local). L'un des deux est défini."""
    return open_stored(stored_name, storage_url, "resumes")
