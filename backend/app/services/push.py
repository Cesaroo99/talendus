"""Web Push : les suivis Talendus arrivent dans la barre de notifications du téléphone."""

from __future__ import annotations

import base64
import json
import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import SystemSetting, User, UserPreference
from app.models.push import PushSubscription

logger = logging.getLogger("talendus.push")

VAPID_PUBLIC_KEY = "vapid_public_key"
VAPID_PRIVATE_PEM = "vapid_private_pem"


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def generate_vapid_pair() -> tuple[str, str]:
    private = ec.generate_private_key(ec.SECP256R1())
    pem = private.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("ascii")
    public = private.public_key().public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint,
    )
    return pem, _b64url(public)


def public_from_pem(pem: str) -> str:
    private = serialization.load_pem_private_key(pem.encode("ascii"), password=None)
    public = private.public_key().public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint,
    )
    return _b64url(public)


def vapid_mailto() -> str:
    settings = get_settings()
    raw = (settings.vapid_mailto or settings.public_email or "ivan.p@example.net").strip()
    if raw.startswith("mailto:"):
        return raw
    return "mailto:" + raw


def vapid_keys(db: Session) -> tuple[str, str]:
    settings = get_settings()
    env_pub = (settings.vapid_public_key or "").strip()
    env_priv = (settings.vapid_private_key or "").strip()
    if env_priv and not env_pub and env_priv.startswith("-----BEGIN"):
        env_pub = public_from_pem(env_priv)
    if env_pub and env_priv:
        return env_priv, env_pub
    rows = {
        row.key: row
        for row in db.scalars(
            select(SystemSetting).where(SystemSetting.key.in_([VAPID_PUBLIC_KEY, VAPID_PRIVATE_PEM]))
        ).all()
    }
    pub = (rows.get(VAPID_PUBLIC_KEY).value if rows.get(VAPID_PUBLIC_KEY) else "") or ""
    priv = (rows.get(VAPID_PRIVATE_PEM).value if rows.get(VAPID_PRIVATE_PEM) else "") or ""
    if pub and priv:
        return priv, pub
    priv, pub = generate_vapid_pair()
    if rows.get(VAPID_PUBLIC_KEY):
        rows[VAPID_PUBLIC_KEY].value = pub
    else:
        db.add(SystemSetting(key=VAPID_PUBLIC_KEY, value=pub, label="Clé publique Web Push"))
    if rows.get(VAPID_PRIVATE_PEM):
        rows[VAPID_PRIVATE_PEM].value = priv
    else:
        db.add(SystemSetting(key=VAPID_PRIVATE_PEM, value=priv, label="Clé privée Web Push"))
    db.commit()
    return priv, pub


def public_key(db: Session) -> str:
    return vapid_keys(db)[1]


def app_href(href: str | None) -> str:
    if not href:
        return "/m.html#/notifs"
    hashpart = ""
    if "#" in href:
        hashpart = href.split("#", 1)[1]
    elif href.startswith("/m.html"):
        return href
    else:
        hashpart = href.lstrip("/")
    if hashpart and not hashpart.startswith("/"):
        hashpart = "/" + hashpart
    aliases = {
        "/dashboard": "/home",
        "/documents": "/cv",
        "/application": "/app",
        "/applications": "/apps",
        "/hiring": "/hiring",
        "/jobs": "/jobs",
    }
    for old, new in aliases.items():
        if hashpart == old or hashpart.startswith(old + "/"):
            hashpart = new + hashpart[len(old) :]
            break
    return "/m.html#" + (hashpart or "/notifs")


def subscribe(db: Session, user: User, endpoint: str, p256dh: str, auth: str, user_agent: str | None = None) -> PushSubscription:
    endpoint = (endpoint or "").strip()
    p256dh = (p256dh or "").strip()
    auth = (auth or "").strip()
    row = db.scalar(select(PushSubscription).where(PushSubscription.endpoint == endpoint))
    if row:
        row.user_id = user.id
        row.p256dh = p256dh
        row.auth = auth
        if user_agent:
            row.user_agent = user_agent[:255]
    else:
        row = PushSubscription(
            user_id=user.id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
            user_agent=(user_agent or "")[:255] or None,
        )
        db.add(row)
    pref = user.preferences or db.scalar(select(UserPreference).where(UserPreference.user_id == user.id))
    if pref is not None:
        pref.notify_push = True
    db.commit()
    db.refresh(row)
    return row


def unsubscribe(db: Session, user: User, endpoint: str) -> int:
    row = db.scalar(
        select(PushSubscription).where(
            PushSubscription.endpoint == endpoint.strip(),
            PushSubscription.user_id == user.id,
        )
    )
    if not row:
        return 0
    db.delete(row)
    db.commit()
    return 1


def _deliver(subscription_info: dict, payload: bytes, vapid_private: str, mailto: str) -> None:
    from pywebpush import webpush

    webpush(
        subscription_info=subscription_info,
        data=payload,
        vapid_private_key=vapid_private,
        vapid_claims={"sub": mailto},
        ttl=86400,
    )


def send_to_user(db: Session, user: User, title: str, message: str, href: str | None = None) -> int:
    rows = list(db.scalars(select(PushSubscription).where(PushSubscription.user_id == user.id)).all())
    if not rows:
        return 0
    priv, _pub = vapid_keys(db)
    mailto = vapid_mailto()
    body = json.dumps(
        {
            "title": title,
            "body": message,
            "href": app_href(href),
            "icon": "/assets/img/logo/icon-192.png",
        },
        ensure_ascii=False,
    ).encode("utf-8")
    sent = 0
    stale: list[PushSubscription] = []
    for row in rows:
        info = {"endpoint": row.endpoint, "keys": {"p256dh": row.p256dh, "auth": row.auth}}
        try:
            _deliver(info, body, priv, mailto)
            sent += 1
        except Exception as exc:
            status = getattr(exc, "response", None)
            code = getattr(status, "status_code", None) if status is not None else None
            if code in {404, 410} or "410" in str(exc) or "404" in str(exc):
                stale.append(row)
            else:
                logger.info("push failed user=%s err=%s", user.id, exc)
    for row in stale:
        db.delete(row)
    if stale:
        db.commit()
    return sent
