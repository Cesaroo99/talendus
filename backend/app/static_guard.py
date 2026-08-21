"""Refuse de servir le code, le stockage et les fichiers internes via le site statique."""

from __future__ import annotations

HIDDEN_PREFIXES = (
    "backend/",
    "mobile/",
    "scripts/",
    "alembic/",
    "storage/",
    "tests/",
    ".git/",
    ".github/",
    ".cursor/",
    ".venv/",
)
HIDDEN_NAMES = {
    "backend",
    "dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "alembic.ini",
    "pytest.ini",
    ".env",
    ".env.example",
    ".gitignore",
    ".dockerignore",
}
HIDDEN_SUFFIXES = (".py", ".pyc", ".pyo", ".db", ".sqlite", ".sqlite3")


def is_hidden_static_path(path: str | None) -> bool:
    raw = (path or "").replace("\\", "/").lstrip("/")
    if not raw or raw in {".", ".."}:
        return False
    parts = [part for part in raw.split("/") if part]
    if any(part == ".." for part in parts):
        return True
    lowered = "/".join(parts).lower()
    if lowered in HIDDEN_NAMES or parts[0].lower() in HIDDEN_NAMES:
        return True
    if any(lowered.startswith(prefix) for prefix in HIDDEN_PREFIXES):
        return True
    if parts[0].startswith(".") and parts[0] != ".well-known":
        return True
    return lowered.endswith(HIDDEN_SUFFIXES)
