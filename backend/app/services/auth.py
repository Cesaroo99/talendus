from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.errors import AppError
from app.models import Candidate, Company, EmailToken, Recruiter, RefreshToken, User
from app.models.enums import EmailType, NotificationType, UserRole, utcnow
from app.schemas import LoginIn, RegisterIn
from app.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    token_expired,
    verify_password,
)
from app.services.audit import audit
from app.services.email import send_email
from app.services.notifications import notify

settings = get_settings()

ALLOWED_SELF_ROLES = {UserRole.CANDIDATE, UserRole.EMPLOYER}


def _issue_tokens(db: Session, user: User) -> dict:
    access = create_access_token(user.id, user.role.value)
    refresh = create_refresh_token()
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh),
            expires_at=utcnow() + timedelta(days=settings.refresh_token_days),
        )
    )
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.access_token_minutes * 60,
    }


def _make_email_token(db: Session, user: User, purpose: str, hours: int) -> str:
    raw = create_refresh_token()
    db.add(
        EmailToken(
            user_id=user.id,
            purpose=purpose,
            token_hash=hash_token(raw),
            expires_at=utcnow() + timedelta(hours=hours),
        )
    )
    return raw


def register(db: Session, data: RegisterIn, ip: str | None = None) -> tuple[User, dict]:
    if data.role not in ALLOWED_SELF_ROLES:
        raise AppError(403, "Ce rôle ne peut pas s'inscrire publiquement.", "ROLE_NOT_ALLOWED")
    existing = db.scalar(select(User).where(User.email == data.email.lower()))
    if existing:
        raise AppError(409, "Un compte existe déjà avec ce courriel.", "EMAIL_TAKEN")
    user = User(
        email=data.email.lower(),
        password_hash=hash_password(data.password),
        first_name=data.first_name.strip(),
        last_name=data.last_name.strip(),
        phone=data.phone,
        role=data.role,
    )
    db.add(user)
    db.flush()
    if user.role == UserRole.CANDIDATE:
        db.add(Candidate(user_id=user.id))
    elif user.role == UserRole.EMPLOYER:
        db.add(Company(name=f"{user.last_name} Inc.", owner_user_id=user.id, contact_name=user.full_name, email=user.email))
    elif user.role == UserRole.RECRUITER:
        db.add(Recruiter(user_id=user.id))
    token = _make_email_token(db, user, "verify", 24)
    send_email(
        db, user.email, EmailType.WELCOME, "welcome",
        name=user.first_name, link=f"{settings.frontend_url}/#/verify?token={token}",
    )
    send_email(
        db, user.email, EmailType.VERIFY_EMAIL, "verify",
        name=user.first_name, link=f"{settings.frontend_url}/#/verify?token={token}",
    )
    notify(db, user, NotificationType.ACCOUNT_CREATED, "Compte créé", "Bienvenue chez Talendus.")
    audit(db, "account.register", user, "user", user.id, ip)
    tokens = _issue_tokens(db, user)
    db.commit()
    db.refresh(user)
    return user, tokens


def login(db: Session, data: LoginIn, ip: str | None = None) -> tuple[User, dict]:
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise AppError(401, "Identifiants incorrects.", "INVALID_CREDENTIALS")
    if not user.is_active:
        raise AppError(403, "Ce compte est désactivé.", "ACCOUNT_DISABLED")
    user.last_login_at = utcnow()
    tokens = _issue_tokens(db, user)
    audit(db, "auth.login", user, "user", user.id, ip)
    db.commit()
    return user, tokens


def refresh(db: Session, raw: str) -> dict:
    row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw)))
    if not row or row.revoked or token_expired(row.expires_at):
        raise AppError(401, "Session expirée. Reconnectez-vous.", "INVALID_REFRESH")
    user = db.get(User, row.user_id)
    if not user or not user.is_active:
        raise AppError(401, "Compte indisponible.", "ACCOUNT_DISABLED")
    row.revoked = True
    tokens = _issue_tokens(db, user)
    db.commit()
    return tokens


def logout(db: Session, raw: str | None, user: User, ip: str | None = None) -> None:
    if raw:
        row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw)))
        if row and row.user_id == user.id:
            row.revoked = True
    audit(db, "auth.logout", user, "user", user.id, ip)
    db.commit()


def request_password_reset(db: Session, email: str) -> None:
    user = db.scalar(select(User).where(User.email == email.lower()))
    if not user:
        return
    token = _make_email_token(db, user, "reset", 2)
    send_email(
        db, user.email, EmailType.PASSWORD_RESET, "reset",
        name=user.first_name or "Bonjour",
        link=f"{settings.frontend_url}/#/reset?token={token}",
    )
    db.commit()


def reset_password(db: Session, token: str, new_password: str) -> None:
    row = db.scalar(select(EmailToken).where(EmailToken.token_hash == hash_token(token), EmailToken.purpose == "reset"))
    if not row or row.used_at or token_expired(row.expires_at):
        raise AppError(400, "Lien de réinitialisation invalide ou expiré.", "INVALID_TOKEN")
    user = db.get(User, row.user_id)
    user.password_hash = hash_password(new_password)
    row.used_at = utcnow()
    audit(db, "auth.password_reset", user, "user", user.id)
    db.commit()


def change_password(db: Session, user: User, current: str, new: str) -> None:
    if not verify_password(current, user.password_hash):
        raise AppError(400, "Mot de passe actuel incorrect.", "INVALID_PASSWORD")
    user.password_hash = hash_password(new)
    audit(db, "auth.password_change", user, "user", user.id)
    db.commit()


def verify_email(db: Session, token: str) -> None:
    row = db.scalar(select(EmailToken).where(EmailToken.token_hash == hash_token(token), EmailToken.purpose == "verify"))
    if not row or row.used_at or token_expired(row.expires_at):
        raise AppError(400, "Lien de vérification invalide ou expiré.", "INVALID_TOKEN")
    user = db.get(User, row.user_id)
    user.is_email_verified = True
    user.email_verified_at = utcnow()
    row.used_at = utcnow()
    db.commit()


def resend_verification(db: Session, user: User) -> None:
    if user.is_email_verified:
        return
    token = _make_email_token(db, user, "verify", 24)
    send_email(
        db, user.email, EmailType.VERIFY_EMAIL, "verify",
        name=user.first_name, link=f"{settings.frontend_url}/#/verify?token={token}",
    )
    db.commit()


def ensure_candidate(db: Session, user: User) -> Candidate:
    if user.role != UserRole.CANDIDATE:
        raise AppError(403, "Un compte candidat est requis.", "FORBIDDEN")
    profile = db.scalar(select(Candidate).where(Candidate.user_id == user.id))
    if not profile:
        profile = Candidate(user_id=user.id)
        db.add(profile)
        db.flush()
    return profile
