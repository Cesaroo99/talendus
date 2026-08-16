"""Effets de bord optionnels : n'appellent un fournisseur que s'il est réellement actif."""

from __future__ import annotations

import logging

from app.integrations.errors import IntegrationError
from app.integrations.maps.google import GoogleMapsService
from app.integrations.messaging.whatsapp import WhatsAppService
from app.integrations.registry import is_active

logger = logging.getLogger("talendus.integrations.hooks")


def normalize_phone(raw: str | None) -> str | None:
    if not raw:
        return None
    cleaned = "".join(ch for ch in raw.strip() if ch.isdigit() or ch == "+")
    if len(cleaned) < 8:
        return None
    return cleaned


def maybe_send_whatsapp(
    *,
    recipient: str | None,
    template: str,
    variables: dict | None = None,
    message_type: str = "template",
) -> dict | None:
    phone = normalize_phone(recipient)
    if not phone:
        return None
    if not is_active("whatsapp"):
        return None
    try:
        return WhatsAppService().send(
            recipient=phone,
            template=template,
            variables=variables,
            message_type=message_type,
        )
    except IntegrationError as exc:
        logger.warning("whatsapp skipped template=%s code=%s", template, exc.code)
        return None
    except Exception:
        logger.exception("whatsapp optional send failed template=%s", template)
        return None


def company_address(*parts: str | None) -> str | None:
    meaningful = [p.strip() for p in parts if p and str(p).strip()]
    if not meaningful:
        return None
    if len(meaningful) == 1 and meaningful[0].lower() in {"québec", "quebec", "canada"}:
        return None
    return ", ".join(meaningful)


def maybe_geocode(address: str | None) -> dict | None:
    if not address or not address.strip():
        return None
    if not is_active("google_maps"):
        return None
    try:
        return GoogleMapsService().geocode(address.strip())
    except IntegrationError as exc:
        logger.warning("geocode skipped code=%s", exc.code)
        return None
    except Exception:
        logger.exception("geocode optional failed")
        return None


def apply_coordinates(entity, geo: dict | None) -> None:
    if not geo or not hasattr(entity, "lat"):
        return
    entity.lat = geo.get("lat")
    entity.lng = geo.get("lng")
    if hasattr(entity, "place_id"):
        entity.place_id = geo.get("place_id")
