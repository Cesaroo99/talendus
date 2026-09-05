import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import get_settings
from app.models.enums import utcnow

settings = get_settings()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user_id: str, role: str, session_version: int = 0) -> str:
    exp = utcnow() + timedelta(minutes=settings.access_token_minutes)
    return jwt.encode(
        {
            "sub": user_id,
            "role": role,
            "exp": exp,
            "typ": "access",
            "ver": int(session_version or 0),
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        if payload.get("typ") != "access":
            raise JWTError("wrong type")
        return payload
    except JWTError as exc:
        raise ValueError("invalid token") from exc


def random_password(length: int = 12) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def token_expired(expires_at: datetime) -> bool:
    return aware(expires_at) < utcnow()


def hmac_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)
