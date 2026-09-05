from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import client_ip, get_current_user, get_current_user_unverified
from app.errors import ok
from app.models import User
from app.schemas import (
    EmailVerifyIn,
    LoginIn,
    OAuthGoogleIn,
    OAuthLinkedInIn,
    PasswordChangeIn,
    PasswordForgotIn,
    PasswordResetIn,
    RefreshIn,
    RegisterIn,
    UserPublic,
)
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _ua(request: Request) -> str | None:
    return (request.headers.get("user-agent") or "")[:255] or None


def _token_payload(user: User, tokens: dict) -> dict:
    return ok({**tokens, "user": UserPublic.model_validate(user).model_dump(mode="json")})


@router.get("/providers")
def providers():
    return ok(auth_service.auth_providers())


@router.post("/register")
def register(payload: RegisterIn, request: Request, db: Session = Depends(get_db)):
    user, tokens = auth_service.register(db, payload, client_ip(request), _ua(request))
    return _token_payload(user, tokens)


@router.post("/login")
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    user, tokens = auth_service.login(db, payload, client_ip(request), _ua(request))
    return _token_payload(user, tokens)


@router.post("/oauth/google")
def oauth_google(payload: OAuthGoogleIn, request: Request, db: Session = Depends(get_db)):
    user, tokens = auth_service.login_google(
        db, payload.id_token, payload.role, payload.company_name, client_ip(request), _ua(request)
    )
    return _token_payload(user, tokens)


@router.post("/oauth/linkedin")
def oauth_linkedin(payload: OAuthLinkedInIn, request: Request, db: Session = Depends(get_db)):
    user, tokens = auth_service.login_linkedin(
        db, payload.access_token, payload.role, payload.company_name, client_ip(request), _ua(request)
    )
    return _token_payload(user, tokens)


@router.post("/refresh")
def refresh(payload: RefreshIn, db: Session = Depends(get_db)):
    return ok(auth_service.refresh(db, payload.refresh_token))


@router.post("/logout")
def logout(request: Request, payload: RefreshIn | None = None, user: User = Depends(get_current_user_unverified), db: Session = Depends(get_db)):
    auth_service.logout(db, payload.refresh_token if payload else None, user, client_ip(request))
    return ok(message="Déconnexion effectuée.")


@router.post("/forgot-password")
def forgot(payload: PasswordForgotIn, db: Session = Depends(get_db)):
    auth_service.request_password_reset(db, payload.email)
    return ok(message="Si un compte existe, un courriel a été envoyé.")


@router.post("/reset-password")
def reset(payload: PasswordResetIn, db: Session = Depends(get_db)):
    auth_service.reset_password(db, payload.token, payload.new_password)
    return ok(message="Mot de passe mis à jour.")


@router.post("/change-password")
def change(payload: PasswordChangeIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_service.change_password(db, user, payload.current_password, payload.new_password)
    return ok(message="Mot de passe modifié.")


@router.post("/verify-email")
def verify(payload: EmailVerifyIn, db: Session = Depends(get_db)):
    auth_service.verify_email(db, payload.token)
    return ok(message="Adresse courriel vérifiée.")


@router.post("/resend-verification")
def resend_verification(user: User = Depends(get_current_user_unverified), db: Session = Depends(get_db)):
    auth_service.resend_verification(db, user)
    return ok(message="Si le compte n'est pas encore vérifié, un courriel a été envoyé.")


@router.get("/sessions")
def sessions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(auth_service.list_sessions(db, user))


@router.delete("/sessions/{session_id}")
def revoke_session(session_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    auth_service.revoke_session(db, user, session_id)
    return ok(message="Session révoquée.")


@router.post("/sessions/revoke-all")
def revoke_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    count = auth_service.revoke_all_sessions(db, user)
    return ok({"revoked": count}, message="Sessions révoquées.")


@router.get("/login-events")
def login_events(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ok(auth_service.list_login_events(db, user))
