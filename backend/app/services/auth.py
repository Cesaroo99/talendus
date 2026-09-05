from datetime import timedelta
from collections import defaultdict
import time

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.errors import AppError
from app.models import Candidate, EmailToken, Recruiter, RefreshToken, User, UserPreference
from app.models.enums import AccountStatus, EmailType, NotificationType, UserRole, utcnow
from app.models.portal import LoginEvent
from app.schemas import LoginIn, RegisterIn
from app.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    random_password,
    token_expired,
    verify_password,
)
from app.services.audit import audit
from app.services.email import send_email
from app.services.notifications import notify

settings = get_settings()

ALLOWED_SELF_ROLES = {UserRole.CANDIDATE, UserRole.EMPLOYER}
PUBLIC_EMAIL_GATE_ROLES = {UserRole.CANDIDATE, UserRole.EMPLOYER}


def email_gate_enabled(db: Session | None = None) -> bool:
    """Le gate suit un override SMTP explicite, sinon EMAIL_ENABLED.

    Les identifiants SMTP seuls n’activent pas le gate. Un stub qui force
    `runtime_email_config().enabled` sans `smtp.enabled` en base ne le change pas.
    """
    if db is not None:
        try:
            from app.services.email import _truthy, load_smtp_overrides

            override = _truthy(load_smtp_overrides(db).get("smtp.enabled"))
            if override is not None:
                return bool(override)
        except Exception:  # noqa: BLE001
            pass
    return bool(get_settings().email_enabled)


def user_needs_email_gate(user: User | None) -> bool:
    return bool(user and user.role in PUBLIC_EMAIL_GATE_ROLES)
_ROLE_ACCOUNT_LABEL = {
    UserRole.CANDIDATE: "talent",
    UserRole.EMPLOYER: "employeur",
    UserRole.RECRUITER: "recruteur",
    UserRole.ADMIN: "administrateur",
    UserRole.SUPER_ADMIN: "administrateur",
    UserRole.FINANCE: "finance",
    UserRole.EDITOR: "éditeur",
}
_LOGIN_FAILS: dict[str, list[float]] = defaultdict(list)


def _login_key(email: str, ip: str | None = None) -> str:
    return (email or "").strip().lower()


def _failed_login_count(db: Session, email: str, ip: str | None = None) -> int:
    minutes = get_settings().login_lockout_minutes or 15
    since = utcnow() - timedelta(minutes=minutes)
    return int(
        db.scalar(
            select(func.count())
            .select_from(LoginEvent)
            .where(
                LoginEvent.email == (email or "").strip().lower(),
                LoginEvent.success.is_(False),
                LoginEvent.created_at >= since,
            )
        )
        or 0
    )


def _assert_not_locked(email: str, ip: str | None, db: Session | None = None) -> None:
    max_attempts = get_settings().login_max_attempts or 5
    lock_minutes = get_settings().login_lockout_minutes or 15
    key = _login_key(email, ip)
    now = time.time()
    window = lock_minutes * 60
    hits = [ts for ts in _LOGIN_FAILS.get(key, []) if now - ts < window]
    if hits:
        _LOGIN_FAILS[key] = hits
    else:
        _LOGIN_FAILS.pop(key, None)
    if len(hits) >= max_attempts:
        raise AppError(429, "Trop de tentatives. Réessayez plus tard.", "LOGIN_LOCKED")
    if db is not None and _failed_login_count(db, email, ip) >= max_attempts:
        raise AppError(429, "Trop de tentatives. Réessayez plus tard.", "LOGIN_LOCKED")


def _record_login_fail(email: str, ip: str | None) -> None:
    _LOGIN_FAILS[_login_key(email, ip)].append(time.time())


def _clear_login_fail(email: str, ip: str | None) -> None:
    _LOGIN_FAILS.pop(_login_key(email, ip), None)


def _log_login(db: Session, email: str, success: bool, user: User | None, ip: str | None, user_agent: str | None) -> None:
    db.add(
        LoginEvent(
            user_id=user.id if user else None,
            email=(email or "")[:255],
            ip_address=(ip or "")[:64] or None,
            user_agent=(user_agent or "")[:255] or None,
            success=success,
        )
    )


def _user_locale(db: Session, user: User) -> str:
    pref = getattr(user, "preferences", None)
    if pref is None:
        pref = db.scalar(select(UserPreference).where(UserPreference.user_id == user.id))
    locale = (getattr(pref, "locale", None) or "fr-CA").strip() or "fr-CA"
    return locale


def portal_auth_link(db: Session, user: User, purpose: str, token: str | None = None) -> str:
    locale = _user_locale(db, user)
    is_en = locale.lower().startswith("en")
    is_employer = user.role == UserRole.EMPLOYER
    if is_en:
        page = "en/account-employer.html" if is_employer else "en/account.html"
    else:
        page = "espace-employeur.html" if is_employer else "espace.html"
    base = settings.frontend_url.rstrip("/")
    if purpose == "welcome" and not token:
        return f"{base}/{page}"
    suffix = f"#/{purpose}/{token}" if token else ""
    return f"{base}/{page}{suffix}"


def _issue_tokens(db: Session, user: User) -> dict:
    access = create_access_token(user.id, user.role.value, getattr(user, "session_version", 0) or 0)
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


def register(db: Session, data: RegisterIn, ip: str | None = None, user_agent: str | None = None) -> tuple[User, dict]:
    from app.services.spam import reject_honeypot

    reject_honeypot(data.website_url)
    if data.role not in ALLOWED_SELF_ROLES:
        raise AppError(403, "Ce rôle ne peut pas s'inscrire publiquement.", "ROLE_NOT_ALLOWED")
    existing = db.scalar(select(User).where(User.email == data.email.lower()))
    if existing:
        raise AppError(409, "Un compte existe déjà avec ce courriel. Connectez-vous.", "EMAIL_TAKEN")
    try:
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
        locale = "en-CA" if str(getattr(data, "locale", None) or "").lower().startswith("en") else "fr-CA"
        db.add(UserPreference(user_id=user.id, locale=locale))
        if user.role == UserRole.CANDIDATE:
            db.add(Candidate(user_id=user.id, country="Canada", province="Québec"))
        elif user.role == UserRole.EMPLOYER:
            from app.services.employer_claim import claim_or_create_employer_company

            claim_or_create_employer_company(db, user, data.company_name or "")
        elif user.role == UserRole.RECRUITER:
            db.add(Recruiter(user_id=user.id))
        token = _make_email_token(db, user, "verify", 24)
        verify_link = portal_auth_link(db, user, "verify", token)
        send_email(
            db, user.email, EmailType.WELCOME, "welcome",
            name=user.first_name, link=verify_link, locale=locale,
        )
        send_email(
            db, user.email, EmailType.VERIFY_EMAIL, "verify",
            name=user.first_name, link=verify_link, locale=locale,
        )
        notify(db, user, NotificationType.ACCOUNT_CREATED, "Compte créé", "Bienvenue chez Talendus.")
        audit(db, "account.register", user, "user", user.id, ip)
        from app.services.prospects import touch_from_user

        db.flush()
        touch_from_user(db, user, source="inscription", company_name=data.company_name or "")
        tokens = _issue_tokens(db, user)
        _log_login(db, user.email, True, user, ip, user_agent)
        db.commit()
        db.refresh(user)
        return user, tokens
    except IntegrityError:
        db.rollback()
        raise AppError(409, "Un compte existe déjà avec ce courriel. Connectez-vous.", "EMAIL_TAKEN") from None


def login(db: Session, data: LoginIn, ip: str | None = None, user_agent: str | None = None) -> tuple[User, dict]:
    email = data.email.lower()
    _assert_not_locked(email, ip, db)
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(data.password, user.password_hash):
        _record_login_fail(email, ip)
        _log_login(db, email, False, user, ip, user_agent)
        db.commit()
        raise AppError(401, "Identifiants incorrects.", "INVALID_CREDENTIALS")
    if not user.is_active or user.account_status in {AccountStatus.SUSPENDED, AccountStatus.DEACTIVATED}:
        _log_login(db, email, False, user, ip, user_agent)
        db.commit()
        raise AppError(403, "Ce compte est désactivé.", "ACCOUNT_DISABLED")
    if email_gate_enabled(db) and user_needs_email_gate(user) and not user.is_email_verified:
        _log_login(db, email, False, user, ip, user_agent)
        db.commit()
        raise AppError(403, "Vérifiez votre courriel avant de vous connecter.", "EMAIL_NOT_VERIFIED")
    _clear_login_fail(email, ip)
    user.last_login_at = utcnow()
    tokens = _issue_tokens(db, user)
    _log_login(db, email, True, user, ip, user_agent)
    audit(db, "auth.login", user, "user", user.id, ip)
    db.commit()
    return user, tokens


def refresh(db: Session, raw: str) -> dict:
    row = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == hash_token(raw)))
    if not row or row.revoked or token_expired(row.expires_at):
        raise AppError(401, "Session expirée. Reconnectez-vous.", "INVALID_REFRESH")
    user = db.get(User, row.user_id)
    if not user or not user.is_active or user.account_status in {AccountStatus.SUSPENDED, AccountStatus.DEACTIVATED}:
        raise AppError(401, "Compte indisponible.", "ACCOUNT_DISABLED")
    if email_gate_enabled(db) and user_needs_email_gate(user) and not user.is_email_verified:
        raise AppError(403, "Vérifiez votre courriel avant de vous connecter.", "EMAIL_NOT_VERIFIED")
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
        link=portal_auth_link(db, user, "reset", token),
        locale=_user_locale(db, user),
    )
    db.commit()


def reset_password(db: Session, token: str, new_password: str) -> None:
    row = db.scalar(select(EmailToken).where(EmailToken.token_hash == hash_token(token), EmailToken.purpose == "reset"))
    if not row or row.used_at or token_expired(row.expires_at):
        raise AppError(400, "Lien de réinitialisation invalide ou expiré.", "INVALID_TOKEN")
    user = db.get(User, row.user_id)
    if not user:
        raise AppError(400, "Lien de réinitialisation invalide ou expiré.", "INVALID_TOKEN")
    user.password_hash = hash_password(new_password)
    row.used_at = utcnow()
    _revoke_user_sessions(db, user)
    audit(db, "auth.password_reset", user, "user", user.id)
    db.commit()


def change_password(db: Session, user: User, current: str, new: str) -> None:
    if not verify_password(current, user.password_hash):
        raise AppError(400, "Mot de passe actuel incorrect.", "INVALID_PASSWORD")
    user.password_hash = hash_password(new)
    _revoke_user_sessions(db, user)
    audit(db, "auth.password_change", user, "user", user.id)
    db.commit()


def verify_email(db: Session, token: str) -> None:
    row = db.scalar(select(EmailToken).where(EmailToken.token_hash == hash_token(token), EmailToken.purpose == "verify"))
    if not row or row.used_at or token_expired(row.expires_at):
        raise AppError(400, "Lien de vérification invalide ou expiré.", "INVALID_TOKEN")
    user = db.get(User, row.user_id)
    if not user:
        raise AppError(400, "Lien de vérification invalide ou expiré.", "INVALID_TOKEN")
    user.is_email_verified = True
    user.email_verified_at = utcnow()
    row.used_at = utcnow()
    db.commit()


def resend_verification(db: Session, user: User) -> None:
    if user.is_email_verified:
        return
    token = _make_email_token(db, user, "verify", 24)
    locale = _user_locale(db, user)
    send_email(
        db, user.email, EmailType.VERIFY_EMAIL, "verify",
        name=user.first_name, link=portal_auth_link(db, user, "verify", token),
        locale=locale,
    )
    db.commit()


def resend_verification_by_email(db: Session, email: str) -> None:
    user = db.scalar(select(User).where(User.email == (email or "").strip().lower()))
    if user and not user.is_email_verified:
        resend_verification(db, user)


def ensure_candidate(db: Session, user: User) -> Candidate:
    if user.role != UserRole.CANDIDATE:
        raise AppError(403, "Un compte candidat est requis.", "FORBIDDEN")
    profile = db.scalar(select(Candidate).where(Candidate.user_id == user.id))
    if not profile:
        profile = Candidate(user_id=user.id)
        db.add(profile)
        db.flush()
    return profile


def _provision_role(db: Session, user: User, company_name: str | None = None) -> None:
    if user.role == UserRole.CANDIDATE:
        if not db.scalar(select(Candidate).where(Candidate.user_id == user.id)):
            db.add(Candidate(user_id=user.id, country="Canada", province="Québec"))
    elif user.role == UserRole.EMPLOYER:
        from app.services.employer_claim import claim_or_create_employer_company

        claim_or_create_employer_company(db, user, company_name or "")


def auth_providers() -> dict:
    env = get_settings()
    google_client_id = env.google_oauth_client_id or ""
    linkedin_client_id = env.linkedin_oauth_client_id or ""
    linkedin_secret = env.linkedin_oauth_client_secret or env.linkedin_client_secret or ""
    return {
        "password": True,
        "google": bool(google_client_id),
        "google_client_id": google_client_id,
        "linkedin": bool(linkedin_client_id and linkedin_secret),
        "linkedin_client_id": linkedin_client_id if linkedin_secret else "",
    }


def login_with_identity(
    db: Session,
    *,
    email: str,
    first_name: str,
    last_name: str,
    role: UserRole,
    company_name: str | None,
    ip: str | None,
    user_agent: str | None,
    provider: str,
    email_verified: bool = False,
) -> tuple[User, dict]:
    if role not in ALLOWED_SELF_ROLES:
        raise AppError(403, "Ce rôle ne peut pas s'inscrire publiquement.", "ROLE_NOT_ALLOWED")
    email = email.lower()
    user = db.scalar(select(User).where(User.email == email))
    created = False
    if not user:
        created = True
        user = User(
            email=email,
            password_hash=hash_password(random_password(16)),
            first_name=(first_name or "Prénom")[:80],
            last_name=(last_name or "")[:80],
            role=role,
            is_email_verified=True,
            email_verified_at=utcnow(),
        )
        db.add(user)
        db.flush()
        db.add(UserPreference(user_id=user.id))
        _provision_role(db, user, company_name)
        send_email(
            db,
            user.email,
            EmailType.WELCOME,
            "welcome",
            name=user.first_name,
            link=portal_auth_link(db, user, "welcome"),
            locale=_user_locale(db, user),
        )
        notify(db, user, NotificationType.ACCOUNT_CREATED, "Compte créé", "Bienvenue chez Talendus.")
        audit(db, f"account.oauth.{provider}", user, "user", user.id, ip)
        from app.services.prospects import touch_from_user

        db.flush()
        touch_from_user(db, user, source="inscription", company_name=company_name or "")
    elif user.role != role:
        label = _ROLE_ACCOUNT_LABEL.get(user.role, "existant")
        raise AppError(
            409,
            f"Ce courriel a déjà un compte {label}. Connectez-vous.",
            "ACCOUNT_EXISTS",
        )
    if not user.is_active or user.account_status in {AccountStatus.SUSPENDED, AccountStatus.DEACTIVATED}:
        raise AppError(403, "Ce compte est désactivé.", "ACCOUNT_DISABLED")
    if created or (email_verified and not user.is_email_verified):
        user.is_email_verified = True
        user.email_verified_at = user.email_verified_at or utcnow()
    if not created and email_gate_enabled(db) and user_needs_email_gate(user) and not user.is_email_verified:
        _log_login(db, email, False, user, ip, user_agent)
        db.commit()
        raise AppError(403, "Vérifiez votre courriel avant de vous connecter.", "EMAIL_NOT_VERIFIED")
    user.last_login_at = utcnow()
    tokens = _issue_tokens(db, user)
    _log_login(db, email, True, user, ip, user_agent)
    audit(db, f"auth.oauth.{provider}", user, "user", user.id, ip)
    db.commit()
    db.refresh(user)
    return user, tokens


def login_google(db: Session, id_token: str, role: UserRole, company_name: str | None, ip: str | None, user_agent: str | None) -> tuple[User, dict]:
    import httpx

    client_id = get_settings().google_oauth_client_id
    if not client_id:
        raise AppError(503, "La connexion Google n'est pas configurée.", "OAUTH_UNAVAILABLE")
    try:
        res = httpx.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token}, timeout=10)
        payload = res.json()
    except Exception as exc:
        raise AppError(401, "Jeton Google invalide.", "OAUTH_INVALID") from exc
    if res.status_code >= 400 or payload.get("aud") != client_id:
        raise AppError(401, "Jeton Google invalide.", "OAUTH_INVALID")
    if payload.get("email_verified") in {"false", False, "0", 0}:
        raise AppError(401, "Le courriel Google n'est pas vérifié.", "OAUTH_UNVERIFIED")
    email = payload.get("email")
    if not email:
        raise AppError(401, "Jeton Google invalide.", "OAUTH_INVALID")
    return login_with_identity(
        db,
        email=email,
        first_name=payload.get("given_name") or "Prénom",
        last_name=payload.get("family_name") or "",
        role=role,
        company_name=company_name,
        ip=ip,
        user_agent=user_agent,
        provider="google",
        email_verified=True,
    )


def _linkedin_access_token(code: str, redirect_uri: str) -> str:
    import httpx

    env = get_settings()
    client_id = env.linkedin_oauth_client_id
    secret = env.linkedin_oauth_client_secret or env.linkedin_client_secret
    if not client_id or not secret:
        raise AppError(503, "La connexion LinkedIn n'est pas configurée.", "OAUTH_UNAVAILABLE")
    try:
        res = httpx.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": secret,
            },
            timeout=10,
        )
        payload = res.json()
    except Exception as exc:
        raise AppError(401, "Jeton LinkedIn invalide.", "OAUTH_INVALID") from exc
    token = payload.get("access_token")
    if res.status_code >= 400 or not token:
        raise AppError(401, "Jeton LinkedIn invalide.", "OAUTH_INVALID")
    return str(token)


def login_linkedin(
    db: Session,
    access_token: str | None,
    role: UserRole,
    company_name: str | None,
    ip: str | None,
    user_agent: str | None,
    code: str | None = None,
    redirect_uri: str | None = None,
) -> tuple[User, dict]:
    import httpx

    client_id = get_settings().linkedin_oauth_client_id
    if not client_id:
        raise AppError(503, "La connexion LinkedIn n'est pas configurée.", "OAUTH_UNAVAILABLE")
    token = (access_token or "").strip()
    if not token and code:
        token = _linkedin_access_token(code.strip(), (redirect_uri or "").strip())
    if not token:
        raise AppError(400, "Jeton ou code LinkedIn manquant.", "OAUTH_INVALID")
    try:
        res = httpx.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        payload = res.json()
    except Exception as exc:
        raise AppError(401, "Jeton LinkedIn invalide.", "OAUTH_INVALID") from exc
    if res.status_code >= 400:
        raise AppError(401, "Jeton LinkedIn invalide.", "OAUTH_INVALID")
    email = payload.get("email")
    if not email:
        raise AppError(401, "LinkedIn n'a pas fourni de courriel.", "OAUTH_INVALID")
    return login_with_identity(
        db,
        email=email,
        first_name=payload.get("given_name") or payload.get("name") or "Prénom",
        last_name=payload.get("family_name") or "",
        role=role,
        company_name=company_name,
        ip=ip,
        user_agent=user_agent,
        provider="linkedin",
        email_verified=False,
    )


def list_sessions(db: Session, user: User) -> list[dict]:
    rows = list(
        db.scalars(
            select(RefreshToken).where(RefreshToken.user_id == user.id).order_by(RefreshToken.created_at.desc())
        ).all()
    )
    return [
        {
            "id": row.id,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "expires_at": row.expires_at.isoformat() if row.expires_at else None,
            "revoked": bool(row.revoked),
            "active": (not row.revoked) and (not token_expired(row.expires_at)),
        }
        for row in rows[:30]
    ]


def revoke_session(db: Session, user: User, session_id: str) -> None:
    row = db.get(RefreshToken, session_id)
    if not row or row.user_id != user.id:
        raise AppError(404, "Session introuvable.", "SESSION_NOT_FOUND")
    row.revoked = True
    audit(db, "auth.session_revoke", user, "refresh_token", row.id)
    db.commit()


def _revoke_user_sessions(db: Session, user: User) -> int:
    rows = list(db.scalars(select(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.revoked.is_(False))).all())
    for row in rows:
        row.revoked = True
    user.session_version = int(getattr(user, "session_version", 0) or 0) + 1
    return len(rows)


def revoke_all_sessions(db: Session, user: User) -> int:
    count = _revoke_user_sessions(db, user)
    audit(db, "auth.session_revoke_all", user, "user", user.id)
    db.commit()
    return count


def list_login_events(db: Session, user: User, limit: int = 20) -> list[dict]:
    rows = list(
        db.scalars(
            select(LoginEvent).where(LoginEvent.user_id == user.id).order_by(LoginEvent.created_at.desc()).limit(limit)
        ).all()
    )
    return [
        {
            "id": row.id,
            "success": row.success,
            "ip_address": row.ip_address,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
        for row in rows
    ]
